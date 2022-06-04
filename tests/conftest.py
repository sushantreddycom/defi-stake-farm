import pytest

from brownie import MockERC20
from web3 import Web3
from scripts.helpful_scripts import get_account
import pytest

@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")

@pytest.fixture
def random_ERC20():
    account = get_account()
    random_erc20 = MockERC20.deploy({"from": account})
    return random_erc20