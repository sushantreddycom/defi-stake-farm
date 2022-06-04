from brownie import config, network, CheruToken, TokenFarm
from scripts.helpful_scripts import get_account, get_contract
from web3 import Web3

'''
    gets the balance of various tokens in account
'''
def get_balance():
    account = get_account()

    