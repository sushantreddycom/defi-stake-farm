# function here converts ETH to wETH
# wETH is an ERC-20 based token

from scripts.helpful_scripts import get_account
from brownie import interface, config, network
from web3 import Web3

''' deposits weth into account

    calls the weth contract to convert eth in our account to weth

    deposit_account: account in which weth needs to be deposited
    eth_amount: amount in 'ether' to be deposited into our account
'''

def get_weth(deposit_account, eth_amount):
    """
        Mints wETH by depositing ETH
    """


    # get weth contract from network
    weth = interface.WethInterface(config["networks"][network.show_active()]["weth_token"])

    tx = weth.deposit({"from": deposit_account, "value": Web3.toWei(eth_amount, "ether")})
    tx.wait(1)

    print(f"Received {eth_amount} weth in our address")

    return weth

def main():
    account = get_account()
    get_weth(0.5, account)
