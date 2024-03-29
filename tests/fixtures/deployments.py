import pytest
from starkware.starknet.testing.starknet import Starknet
from utils import (
    Signer,
    str_to_felt,
    ZERO_ADDRESS,
    TRUE,
    FALSE,
    assert_revert,
    INVALID_UINT256,
    assert_event_emitted,
    get_contract_def,
    cached_contract,
    to_uint,
    sub_uint,
    add_uint,
)


signer = Signer(123456789987654321)

NONEXISTENT_TOKEN = to_uint(999)
# random token IDs
TOKENS_BOB = [to_uint(5042), to_uint(793)]
# test token
TOKEN = TOKENS_BOB[0]
# test token 1
TOKEN1 = TOKENS_BOB[1]

TOKENS_CHARLIE = [to_uint(0), to_uint(1)]


# random user address
RECIPIENT = 555
# random data (mimicking bytes in Solidity)
DATA = [0x42, 0x89, 0x55]
# random URIs
SAMPLE_URI_1 = str_to_felt("mock://mytoken.v1")
SAMPLE_URI_2 = str_to_felt("mock://mytoken.v2")

# selector ids
IERC165_ID = 0x01FFC9A7
IERC721_ID = 0x80AC58CD
IERC721_METADATA_ID = 0x5B5E139F
INVALID_ID = 0xFFFFFFFF
UNSUPPORTED_ID = 0xABCD1234

INITAL_SUPPLY = to_uint(30000)
AMOUNT = to_uint(1000)
AMOUNT2 = to_uint(10000)
ZERO_AMOUNT = to_uint(0)
PLATFORM_FEE = to_uint(2000)
MULTIPLIER = to_uint(1000)


@pytest.fixture(scope="module", autouse=True)
async def deployer():
    starknet = await Starknet.empty()

    account_def = get_contract_def("openzeppelin/account/Account.cairo")

    alice = await starknet.deploy(
        contract_def=account_def, constructor_calldata=[signer.public_key]
    )
    bob = await starknet.deploy(
        contract_def=account_def, constructor_calldata=[signer.public_key]
    )

    charlie = await starknet.deploy(
        contract_def=account_def, constructor_calldata=[signer.public_key]
    )

    erc20_def = get_contract_def("openzeppelin/token/erc20/ERC20_Mintable.cairo")
    dai = await starknet.deploy(
        contract_def=erc20_def,
        constructor_calldata=[
            str_to_felt("DAI"),
            str_to_felt("DAI"),
            18,
            *INITAL_SUPPLY,
            alice.contract_address,
            alice.contract_address,
        ],
    )

    ust = await starknet.deploy(
        contract_def=erc20_def,
        constructor_calldata=[
            str_to_felt("UST"),
            str_to_felt("UST"),
            18,
            *INITAL_SUPPLY,
            alice.contract_address,
            alice.contract_address,
        ],
    )

    erc721_def = get_contract_def(
        "openzeppelin/token/erc721/ERC721_Mintable_Burnable.cairo"
    )

    tubbycats = await starknet.deploy(
        contract_def=erc721_def,
        constructor_calldata=[
            str_to_felt("0xratwell"),  # name
            str_to_felt("tubbycats"),  # ticker
            bob.contract_address,  # owner
        ],
    )

    exchange_def = get_contract_def("exchange/Exchange.cairo")
    artpedia = await starknet.deploy(
        contract_def=exchange_def,
        constructor_calldata=[
            alice.contract_address,
            dai.contract_address,
            alice.contract_address,
            *PLATFORM_FEE,
            *MULTIPLIER,
        ],
    )

    return [starknet.state, artpedia, tubbycats, dai, ust, alice, bob, charlie], [
        exchange_def,
        erc721_def,
        erc20_def,
        account_def,
    ]


@pytest.fixture
def factory(deployer):
    [starknet_state, artpedia, tubbycats, dai, ust, alice, bob, charlie], [
        exchange_def,
        erc721_def,
        erc20_def,
        account_def,
    ] = deployer

    _state = starknet_state.copy()
    alice = cached_contract(_state, account_def, alice)
    bob = cached_contract(_state, account_def, bob)
    charlie = cached_contract(_state, account_def, charlie)
    artpedia = cached_contract(_state, exchange_def, artpedia)
    tubbycats = cached_contract(_state, erc721_def, tubbycats)
    dai = cached_contract(_state, erc20_def, dai)
    ust = cached_contract(_state, erc20_def, ust)
    return artpedia, tubbycats, dai, ust, alice, bob, charlie


@pytest.fixture
async def tubbycats_minted_to_bob(factory):
    artpedia, tubbycats, dai, ust, alice, bob, charlie = factory
    for token in TOKENS_BOB:
        await signer.send_transaction(
            bob, tubbycats.contract_address, "mint", [bob.contract_address, *token]
        )

    return artpedia, tubbycats, dai, ust, alice, bob, charlie


@pytest.fixture
async def tubbycats_0_is_listed_by_bob(factory):
    artpedia, tubbycats, dai, ust, alice, bob, charlie = factory

    for token in TOKENS_BOB:
        await signer.send_transaction(
            bob, tubbycats.contract_address, "mint", [bob.contract_address, *token]
        )

    # bob delegate TOKEN to Artpedia Exchange
    await signer.send_transaction(
        bob, tubbycats.contract_address, "approve", [artpedia.contract_address, *TOKEN]
    )

    # list tubbycats 0
    await signer.send_transaction(
        bob,
        artpedia.contract_address,
        "listing",
        [tubbycats.contract_address, *TOKEN, dai.contract_address, *AMOUNT],
    )

    return artpedia, tubbycats, dai, ust, alice, bob, charlie


@pytest.fixture
async def tubbycats_minted_to_charlie(tubbycats_0_is_listed_by_bob):
    artpedia, tubbycats, dai, ust, alice, bob, charlie = tubbycats_0_is_listed_by_bob
    for token in TOKENS_CHARLIE:
        await signer.send_transaction(
            bob,
            tubbycats.contract_address,
            "mint",
            [charlie.contract_address, *token],
        )

    return artpedia, tubbycats, dai, ust, alice, bob, charlie


@pytest.fixture
async def send_dai_to_bob_and_charlie(tubbycats_0_is_listed_by_bob):
    artpedia, tubbycats, dai, ust, alice, bob, charlie = tubbycats_0_is_listed_by_bob

    # send to bob
    await signer.send_transaction(
        alice,
        dai.contract_address,
        "transfer",
        [
            bob.contract_address,
            *AMOUNT2,
        ],
    )

    # send to charlie
    await signer.send_transaction(
        alice,
        dai.contract_address,
        "transfer",
        [
            charlie.contract_address,
            *AMOUNT2,
        ],
    )

    return artpedia, tubbycats, dai, ust, alice, bob, charlie


# @pytest.fixture(autouse=True)
# def isolation(fn_isolation):
#     pass
