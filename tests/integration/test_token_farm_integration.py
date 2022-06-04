from brownie import TokenFarm, CheruToken, exceptions, network, accounts, config, interface
from web3 import Web3
from scripts.helpful_scripts import get_account, get_contract, approve_erc20_token, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_TokenFarm, KEPT_BALANCE
from scripts.get_weth import get_weth
from scripts.get_dai import get_dai
import pytest


''' objective: Test entire staking, unstaking on Rinkeby

    arrange:
        1. create cheru_token and token_farm on rinkeby
        2. allowed tokens are eth, dai, cheru
    act:
        3. account 1 - stake 100 cheru
        4. account 2 - stakes 1 eth, 100 dai
        5. account 3 - stakes 100 dai
    assert:
        6. check staking balance for each account
        7. check total staked value of all accounts together

    act:    
        8. unkstake tokens for account 1
    
    assert:
        9. check staking balance for account 1 = 0
'''

def test_token_farm_integration(amount_staked):
    # ARRANGE

    # run test only in non development environment
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # account 1
    account1 = get_account()

    # # account 2
    # account2 = get_account(index=1)

    # # account 3
    # account3 = get_account(index=2)

    # create token farm and cheru token
    # created cheru_token
    # transfered 999,900 cheru_tokens to token_farm for distributing to stakers
    # balance cheru_tokens are 100 with account1
    # allowed tokens are weth_token, fau_token (mockDAI), cheru_token

    token_farm, cheru_token = deploy_TokenFarm()

    # ACT
    weth_address = get_contract("eth_usd_address")
    (weth_price, weth_decimals) = token_farm.getPrice(weth_address)

    fau_address = get_contract("dai_usd_address")
    (fau_price, fau_decimals) = token_farm.getPrice(fau_address)


    weth_amt =  amount_staked * weth_price / (10 ** weth_decimals)
    fau_amt =  amount_staked * fau_price / (10 ** fau_decimals)
    cheru_amt = amount_staked * fau_price / (10 ** fau_decimals)


    # stake cheru from account 1
    cheru_token.approve(token_farm.address, amount_staked, {"from": account1})
    token_farm.stakeTokens(cheru_amt, cheru_token.address, {"from": account1})

    # get dai and weth from account2
    # weth_token = get_weth(account2, weth_amt)
    # dai_token = get_dai(account2, 100*fau_amt)

    # approve_erc20_token(weth_amt, token_farm.address, weth_token.address, account2)
    # approve_erc20_token(100*fau_amt, token_farm.address, dai_token.address, account2)

    # stake dai and weth from account2
    # token_farm.stakeTokens(weth_amt, weth_token.address, {"from": account2})
    # token_farm.stakeTokens(100*fau_amt, dai_token.address, {"from": account2})

    # get dai from account3 
    # dai_token = get_dai(account3, 100*fau_amt)
    # approve_erc20_token(100*fau_amt, token_farm.address, dai_token.address, account2)
    
    
    # ASSERT
    assert(
        token_farm.getTotalTransferValue(account1.address) == cheru_amt       
    )

    # assert(
    #     token_farm.getTotalTransferValue(account2.address) == fau_amt * 100 + weth_amt
    # )

    # assert(
    #     token_farm.getTotalTransferValue(account3.address) == fau_amt * 100 
    # )

