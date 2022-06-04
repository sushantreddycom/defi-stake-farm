from brownie import TokenFarm, CheruToken, network, exceptions
import pytest
from scripts.helpful_scripts import get_account, get_contract, LOCAL_BLOCKCHAIN_ENVIRONMENTS, STARTING_PRICE, DECIMALS
from scripts.deploy import deploy_TokenFarm, KEPT_BALANCE
from scripts.get_weth import get_weth
from conftest import amount_staked, random_ERC20


def test_add_token_farm():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    account = get_account()
    cheru_token = CheruToken.deploy({"from": account})
    TokenFarm.deploy(cheru_token, {"from": account})

    tx = TokenFarm[-1]

    assert tx is not None


def test_can_add_allowed_token():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    cheru_token = CheruToken.deploy({"from": owner_account })
    TokenFarm.deploy(cheru_token, {"from": owner_account})
    tx = TokenFarm[-1]

    # when I add token using non owner account, test should fail
    non_owner_account = get_account(1)

    with pytest.raises(exceptions.VirtualMachineError):
        tx.addAllowedToken(non_owner_account.address, {"from": non_owner_account})
            

''' Objective of this test is to check if addAllowedToken adds a token correctly 
    adds to the allowedTokensToStake list'''

def test_add_allowed_token():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    owner_account = get_account()
    cheru_token = CheruToken.deploy({"from": owner_account })
    TokenFarm.deploy(cheru_token, {"from": owner_account})
    tx = TokenFarm[-1]

    tx.addAllowedToken(owner_account.address, {"from": owner_account})

    assert tx.isAllowedToken(owner_account.address)


''' Objective is to test if a token can be staked or not. We run 2 tests here

1. staking amount should be positive
2. token should be an approved stake token
'''

def test_can_stake_token_zero_amount():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    account = get_account()
    cheru_token = CheruToken.deploy({"from": account })
    TokenFarm.deploy(cheru_token, {"from": account})

    tx = TokenFarm[-1]

    with pytest.raises(exceptions.VirtualMachineError):
        tx.stakeTokens(0, account.address)

# test to check if we can stake a token whose address is not included
def test_can_stake_token_random_address():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    account = get_account()
    account2 = get_account(1)

    cheru_token = CheruToken.deploy({"from": account })
    TokenFarm.deploy(cheru_token, {"from": account})

    tx = TokenFarm[-1]

    tx.addAllowedToken(account2.address, {"from": account})

    # this account is not a valid stake token address
    with pytest.raises(exceptions.VirtualMachineError):
        tx.stakeTokens(0, account.address)


# objective: test if only owner can run setPricefeed function
def test_can_non_owner_set_price_feed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    account = get_account()
    non_owner_account = get_account(index=1)
    token_farm, cheru_token = deploy_TokenFarm()

    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(cheru_token.address, get_contract("eth_usd_address"), {"from": non_owner_account})

# test if price feed contract is properly captured
# for this test, we use the deploy_TokenFarm() method in deploy.py
def test_price_feeds():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    token_farm, cheru_token = deploy_TokenFarm()

    # check if weth_address and fau_address are in the token farm
    weth_token = get_contract("weth_token")
    
    assert token_farm.tokenPriceFeedMapping(weth_token.address) == get_contract("eth_usd_address")

def test_stake_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    token_farm, cheru_token = deploy_TokenFarm()
    account = get_account()


    # ERC20 approve 
    cheru_token.approve(token_farm.address, amount_staked, {"from": account})

    token_farm.stakeTokens(amount_staked, cheru_token.address, {"from": account})

    # assert
    # 1: check if staked balance for the token & account address is equal to amount staked
    assert (
        token_farm.stakedBalances(cheru_token.address, account.address)== amount_staked
        )

    # 2: check if unique tokens staked for our account is 1 (since we staked only one token so far)
    assert (
        token_farm.uniqueTokensStaked(account.address) ==  1
    )
    # 3: check if total stakers is 1 (only one account has staked so far)
    assert(
        token_farm.stakers(0) == account.address
    )   
    return token_farm, cheru_token


# function to test issuance of tokens
def test_issue_token(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    # Arrange
    account = get_account()
    token_farm, cheru_token = test_stake_tokens(amount_staked)

    # Act
    start_tokens = cheru_token.balanceOf(account.address)
    token_farm.issueTokens({"from": account})

    # Assert
    assert (
        cheru_token.balanceOf(account.address) == start_tokens + STARTING_PRICE * 10 ** 18 / 10 ** DECIMALS
    )

    # test staking with unallowed token
def test_stake_with_unallowed_token(amount_staked, random_ERC20):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Arrange
    account = get_account()
    token_farm, cheru_token = test_stake_tokens(amount_staked)

    # approve random ETC20 token to be staked with token_farm address
    random_ERC20.approve(token_farm.address, amount_staked, {"from": account})

    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.stakeTokens(amount_staked, random_ERC20.address, {"from": account})


''' objective: test the unstake function in TokenFarm'''
def test_unstake_tokens(amount_staked):    
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    account = get_account()
    token_farm, cheru_token = test_stake_tokens(amount_staked)

    unstake_tx = token_farm.unstakeTokens(cheru_token.address, {"from": account})

    # check if account is reinstated with entire balance that it began with
    assert (
        cheru_token.balanceOf(account.address) == KEPT_BALANCE 
    )
    # check if token_farm has no staked balances againt cheru_token for given account
    assert (
        token_farm.stakedBalances(cheru_token.address,account.address) == 0
    )

    # check if unique staked tokens for account address has no tokens (since we staked only one token and unstaked it right after)
    assert (
        token_farm.uniqueTokensStaked(account.address) == 0
    )


''' objective: check if total balance is correctly computed'''
def test_user_balance_with_different_tokens_and_amounts(amount_staked, random_ERC20):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    account = get_account()

    token_farm, cheru_token = test_stake_tokens(amount_staked)

    is_token_added = token_farm.addAllowedToken(random_ERC20.address, {"from": account})
    token_farm.setPriceFeedContract(random_ERC20.address, get_contract("eth_usd_address"), {"from": account})
    random_ERC20.approve(token_farm.address, amount_staked * 2, {'from': account})
    token_farm.stakeTokens(amount_staked*2, random_ERC20.address, {"from": account})

    assert (
        token_farm.getTotalTransferValue(account.address) ==  amount_staked * 3 * STARTING_PRICE / 10 ** DECIMALS
    )



''' objective: test if eth price is correct as per tokenfarm price logic'''
def test_get_token_eth_price(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    
    account = get_account()
    token_farm, cheru_token = test_stake_tokens(amount_staked)

    assert (
        token_farm.getPrice(cheru_token.address) == (STARTING_PRICE, DECIMALS)
    )

    


    