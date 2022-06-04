
from scripts.helpful_scripts import get_account, get_contract
from brownie import CheruToken, TokenFarm, config, network 
from web3 import Web3
import yaml
import json
import shutil
import os

KEPT_BALANCE = Web3.toWei(100, "ether")

def deploy_TokenFarm(update_front_end = False):
    account = get_account()
    cheru_token = CheruToken.deploy({"from": account})

    token_farm = TokenFarm.deploy(cheru_token, {"from": account})

    # first we transfer cheru_token to token farm
    # so that farm has cheru tokens to distribute when users stake

    tx = cheru_token.transfer(token_farm.address, cheru_token.totalSupply() - KEPT_BALANCE, {"from": account})
    tx.wait(1)

    # add allowed tokens to the Token farm contract
    # we use 3 tokens for staking - cheru_token, weth_token, fau_token/dai (faucet token)
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_allowed_tokens = {cheru_token: get_contract("dai_usd_address"), weth_token: get_contract("eth_usd_address"), fau_token: get_contract("dai_usd_address") }
    add_allowed_tokens(token_farm,dict_allowed_tokens, account )
    if (update_front_end):
        update_front_end()

    return token_farm, cheru_token

def add_allowed_tokens(token_farm, dict_allowed_tokens, account):
    for token in dict_allowed_tokens:
        tx = token_farm.addAllowedToken(token.address, {"from": account})
        tx.wait(1)

        price_feed_tx = token_farm.setPriceFeedContract(token.address, dict_allowed_tokens[token], {"from": account})
        price_feed_tx.wait(1)
    return token_farm    

# dumps brownie config onto the front end in json format
def update_front_end():
    copy_folders_to_front_end('./build', './front-end/src/chain-info')
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)

        with open('./front-end/src/brownie-config.json', 'w') as brownie_config_json:
            json.dump(config_dict, brownie_config_json)

    print('front end brownie config updated')

# copy build folder and push it to front end
def copy_folders_to_front_end(src_folder, dest_folder):
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    shutil.copytree(src_folder, dest_folder)

def main():
    deploy_TokenFarm(update_front_end=True)