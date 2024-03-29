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

INITAL_SUPPLY = to_uint(1000)
AMOUNT = to_uint(1000)
AMOUNT2 = to_uint(10000)
ZERO_AMOUNT = to_uint(0)

TOKENS_BOB = [to_uint(5042), to_uint(793)]
TOKENS_CHARLIE = [to_uint(0), to_uint(1)]

SECONDS_IN_DAY = 86400
QUARTER_HOUR = int(SECONDS_IN_DAY / 24 / 4)


# @pytest.mark.asyncio
# async def test_negative_accept_maxbid_by_bidder(send_dai_to_bob_and_charlie):
#     """
#     5042 is listed by bob
#     793 is minted to bob
#     0 is minted to charlie
#     1 is minted to charlie
#     """
#     artpedia, tubbycats, dai, ust, alice, bob, charlie = send_dai_to_bob_and_charlie

#     BID_CHARLIE = to_uint(5000)
#     BID_ALICE = to_uint(10000)

#     token_id = TOKENS_BOB[0]

#     await signer.send_transaction(
#         charlie,
#         dai.contract_address,
#         "approve",
#         [artpedia.contract_address, *BID_CHARLIE],
#     )

#     await signer.send_transaction(
#         charlie,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_CHARLIE,
#             QUARTER_HOUR,
#         ],
#     )

#     await signer.send_transaction(
#         alice, dai.contract_address, "approve", [artpedia.contract_address, *BID_ALICE]
#     )

#     await signer.send_transaction(
#         alice,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_ALICE,
#             QUARTER_HOUR,
#         ],
#     )

#     await assert_revert(
#         signer.send_transaction(
#             alice,
#             artpedia.contract_address,
#             "accept_bid",
#             [
#                 tubbycats.contract_address,
#                 *token_id,
#                 dai.contract_address,
#                 *BID_ALICE,
#                 alice.contract_address,
#                 len(DATA),
#                 *DATA,
#             ],
#         ),
#         reverted_with="ArtpediaExchange: caller is not owner nor operators",
#     )

#     await assert_revert(
#         signer.send_transaction(
#             charlie,
#             artpedia.contract_address,
#             "accept_bid",
#             [
#                 tubbycats.contract_address,
#                 *token_id,
#                 dai.contract_address,
#                 *BID_ALICE,
#                 alice.contract_address,
#                 len(DATA),
#                 *DATA,
#             ],
#         ),
#         reverted_with="ArtpediaExchange: caller is not owner nor operators",
#     )


# @pytest.mark.asyncio
# async def test_negative_assert_bid_exists(send_dai_to_bob_and_charlie):
#     """
#     5042 is listed by bob
#     793 is minted to bob
#     0 is minted to charlie
#     1 is minted to charlie
#     """
#     artpedia, tubbycats, dai, ust, alice, bob, charlie = send_dai_to_bob_and_charlie

#     BID_CHARLIE = to_uint(5000)
#     BID_ALICE = to_uint(10000)

#     token_id = TOKENS_BOB[0]

#     await signer.send_transaction(
#         charlie,
#         dai.contract_address,
#         "approve",
#         [artpedia.contract_address, *BID_CHARLIE],
#     )

#     await assert_revert(
#         signer.send_transaction(
#             bob,
#             artpedia.contract_address,
#             "accept_bid",
#             [
#                 tubbycats.contract_address,
#                 *token_id,
#                 dai.contract_address,
#                 *BID_ALICE,
#                 alice.contract_address,
#                 len(DATA),
#                 *DATA,
#             ],
#         ),
#         reverted_with="ArtpediaExchange: no bid for this token_id",
#     )

#     await assert_revert(
#         signer.send_transaction(
#             bob,
#             artpedia.contract_address,
#             "accept_bid",
#             [
#                 tubbycats.contract_address,
#                 *token_id,
#                 dai.contract_address,
#                 *BID_CHARLIE,
#                 charlie.contract_address,
#                 len(DATA),
#                 *DATA,
#             ],
#         ),
#         reverted_with="ArtpediaExchange: no bid for this token_id",
#     )


# @pytest.mark.asyncio
# async def test_negative_bid_frontrunning_detected(send_dai_to_bob_and_charlie):
#     """
#     5042 is listed by bob
#     793 is minted to bob
#     0 is minted to charlie
#     1 is minted to charlie
#     """
#     artpedia, tubbycats, dai, ust, alice, bob, charlie = send_dai_to_bob_and_charlie

#     BID_CHARLIE = to_uint(5000)
#     BID_ALICE = to_uint(10000)

#     token_id = TOKENS_BOB[0]

#     await signer.send_transaction(
#         charlie,
#         dai.contract_address,
#         "approve",
#         [artpedia.contract_address, *BID_CHARLIE],
#     )

#     await signer.send_transaction(
#         charlie,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_CHARLIE,
#             QUARTER_HOUR,
#         ],
#     )

#     await signer.send_transaction(
#         alice, dai.contract_address, "approve", [artpedia.contract_address, *BID_ALICE]
#     )

#     # alice bid 2 times, overriding the second bid with lower amount after accept_bid had been sent to the mempool
#     # for the sake of simplicity, only the second bid is included in the test
#     BID_ALICE = to_uint(100)

#     await signer.send_transaction(
#         alice,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_ALICE,
#             QUARTER_HOUR,
#         ],
#     )

#     # this was sent before alice changed the bid to 100
#     BID_ALICE = to_uint(10000)

#     await assert_revert(
#         signer.send_transaction(
#             bob,
#             artpedia.contract_address,
#             "accept_bid",
#             [
#                 tubbycats.contract_address,
#                 *token_id,
#                 dai.contract_address,
#                 *BID_ALICE,
#                 alice.contract_address,
#                 len(DATA),
#                 *DATA,
#             ],
#         ),
#         reverted_with="ArtpediaExchange: bid frontrunning detected",
#     )


# @pytest.mark.asyncio
# async def test_negative_exchange_is_not_approved_for_erc721_transfer(
#     send_dai_to_bob_and_charlie,
# ):
#     """
#     5042 is listed by bob
#     793 is minted to bob
#     0 is minted to charlie
#     1 is minted to charlie
#     """
#     artpedia, tubbycats, dai, ust, alice, bob, charlie = send_dai_to_bob_and_charlie

#     token_id = TOKENS_BOB[1]

#     BID_CHARLIE = to_uint(10000)
#     await signer.send_transaction(
#         charlie,
#         dai.contract_address,
#         "approve",
#         [artpedia.contract_address, *BID_CHARLIE],
#     )

#     await signer.send_transaction(
#         charlie,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_CHARLIE,
#             QUARTER_HOUR,
#         ],
#     )

#     BID_ALICE = to_uint(5000)
#     await signer.send_transaction(
#         alice, dai.contract_address, "approve", [artpedia.contract_address, *BID_ALICE]
#     )

#     await signer.send_transaction(
#         alice,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_ALICE,
#             QUARTER_HOUR,
#         ],
#     )

#     await assert_revert(
#         signer.send_transaction(
#             bob,
#             artpedia.contract_address,
#             "accept_bid",
#             [
#                 tubbycats.contract_address,
#                 *token_id,
#                 dai.contract_address,
#                 *BID_CHARLIE,
#                 charlie.contract_address,
#                 len(DATA),
#                 *DATA,
#             ],
#         ),
#         reverted_with="ERC721: either is not approved or the caller is the zero address",
#     )


# @pytest.mark.asyncio
# async def test_positive_accept_maxbid_listed_item_by_owner(send_dai_to_bob_and_charlie):
#     """
#     5042 is listed by bob
#     793 is minted to bob
#     0 is minted to charlie
#     1 is minted to charlie
#     """
#     artpedia, tubbycats, dai, ust, alice, bob, charlie = send_dai_to_bob_and_charlie

#     BID_CHARLIE = to_uint(5000)
#     BID_ALICE = to_uint(10000)

#     token_id = TOKENS_BOB[0]

#     await signer.send_transaction(
#         charlie,
#         dai.contract_address,
#         "approve",
#         [artpedia.contract_address, *BID_CHARLIE],
#     )

#     await signer.send_transaction(
#         charlie,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_CHARLIE,
#             QUARTER_HOUR,
#         ],
#     )

#     await signer.send_transaction(
#         alice, dai.contract_address, "approve", [artpedia.contract_address, *BID_ALICE]
#     )

#     await signer.send_transaction(
#         alice,
#         artpedia.contract_address,
#         "bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_ALICE,
#             QUARTER_HOUR,
#         ],
#     )

#     response = await signer.send_transaction(
#         bob,
#         artpedia.contract_address,
#         "accept_bid",
#         [
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_ALICE,
#             alice.contract_address,
#             len(DATA),
#             *DATA,
#         ],
#     )

#     assert_event_emitted(
#         response,
#         from_address=artpedia.contract_address,
#         name="OrdersMatched",
#         data=[
#             alice.contract_address,
#             bob.contract_address,
#             tubbycats.contract_address,
#             *token_id,
#             dai.contract_address,
#             *BID_ALICE,
#         ],
#     )


# @pytest.mark.asyncio
# async def test_positive_accept_maxbid_listed_item_by_operator(
#     send_dai_to_bob_and_charlie,
# ):
#     """
#     5042 is listed by bob
#     793 is minted to bob
#     0 is minted to charlie
#     1 is minted to charlie
#     """
#     # TODO


@pytest.mark.asyncio
async def test_positive_maxbid_unlisted_item_by_owner(send_dai_to_bob_and_charlie):
    """
    5042 is listed by bob
    793 is minted to bob
    0 is minted to charlie
    1 is minted to charlie
    """
    artpedia, tubbycats, dai, ust, alice, bob, charlie = send_dai_to_bob_and_charlie

    token_id = TOKENS_BOB[1]

    BID_CHARLIE = to_uint(10000)
    await signer.send_transaction(
        charlie,
        dai.contract_address,
        "approve",
        [artpedia.contract_address, *BID_CHARLIE],
    )

    await signer.send_transaction(
        charlie,
        artpedia.contract_address,
        "bid",
        [
            tubbycats.contract_address,
            *token_id,
            dai.contract_address,
            *BID_CHARLIE,
            QUARTER_HOUR,
        ],
    )

    BID_ALICE = to_uint(5000)
    await signer.send_transaction(
        alice, dai.contract_address, "approve", [artpedia.contract_address, *BID_ALICE]
    )

    await signer.send_transaction(
        alice,
        artpedia.contract_address,
        "bid",
        [
            tubbycats.contract_address,
            *token_id,
            dai.contract_address,
            *BID_ALICE,
            QUARTER_HOUR,
        ],
    )

    await signer.send_transaction(
        bob,
        tubbycats.contract_address,
        "approve",
        [artpedia.contract_address, *token_id],
    )

    response = await signer.send_transaction(
        bob,
        artpedia.contract_address,
        "accept_bid",
        [
            tubbycats.contract_address,
            *token_id,
            dai.contract_address,
            *BID_CHARLIE,
            charlie.contract_address,
            len(DATA),
            *DATA,
        ],
    )

    assert_event_emitted(
        response,
        from_address=artpedia.contract_address,
        name="OrdersMatched",
        data=[
            charlie.contract_address,
            bob.contract_address,
            tubbycats.contract_address,
            *token_id,
            dai.contract_address,
            *BID_CHARLIE,
        ],
    )

    response = await tubbycats.ownerOf(token_id).invoke()
    assert response.result == (charlie.contract_address,)

    response = await dai.balanceOf(charlie.contract_address).invoke()
    assert response.result.balance == to_uint(0)

    response = await dai.balanceOf(bob.contract_address).invoke()
    assert response.result.balance == to_uint(19800)

    response = await dai.balanceOf(alice.contract_address).invoke()
    assert response.result.balance == to_uint(10200)
