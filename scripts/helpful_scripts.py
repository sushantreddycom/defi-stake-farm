from brownie import Contract, interface, accounts, network, config, MockV3Aggregator, VRFCoordinatorMock, MockWETH, MockDAI, LinkToken

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']
FORKED_LOCAL_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']
DECIMALS = 8
STARTING_PRICE = 200000000000
STARTING__BTC_PRICE = 3000000000000

contract_to_mock = {"eth_usd_address": MockV3Aggregator, "dai_usd_address": MockV3Aggregator, "btc_usd_address": MockV3Aggregator, "vrf_coordinator": VRFCoordinatorMock, "link_token": LinkToken, "weth_token": MockWETH, "fau_token": MockDAI }


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


'''
    function to approve use of a ERC token in an account
    amount is amount in wei
    spender is smart contract that wants to access the erc_20 token
    erc20_address - contract Address for generating contract
'''
def approve_erc20_token(amount, spender, erc20_address, account):
    print("approving ERC 20 token")
    erc_20 = interface.IERC20(erc20_address)
    approve = erc_20.approve(spender, amount, {"from": account})
    approve.wait(1)
    print('Approved')
    return True

def deploy_mock_aggregator():
    account = get_account()
    link_token = None
    if len(MockV3Aggregator) <= 0:
        print("Deploying Mock Aggregator...")
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
        print("Mock aggregator deployed")

    if len(LinkToken) <= 0:
        print("Deploy Link Token Mock..")
        link_token = LinkToken.deploy({"from": account})
        print(" Mock Link Token deployed")

    if len(VRFCoordinatorMock) <= 0:
        print("Deploying Mock VRF Coordinator")
        VRFCoordinatorMock.deploy(link_token.address, {"from": account})
        print(" Mock VRF Integrator deployed")

    if len(MockDAI) <= 0:
        print("Deploying Mock DAI contract")
        dai_token = MockDAI.deploy({"from": account})
        print(f" Mock DAI deployed at {dai_token.address}")
    
    if len(MockWETH) <= 0:
        print("Deploying Mock WETH contract")
        weth_token = MockWETH.deploy({"from": account})
        print(f" Mock WETH deployed at {weth_token.address}")


def get_contract_address():
    current_network = network.show_active()
    
    if current_network not in  LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][current_network]["eth_usd_address"]
    else:
        # if ganache development environment (local), then
        # we first deploy mock aggregator contract
        # we then assign address of mock aggregator contract to fund me contract price aggregator
        deploy_mock_aggregator()
        price_feed_address = MockV3Aggregator[-1].address
    
    return price_feed_address

def get_contract(contract_name):
    """
        This function gets the contract address from config file for testnet/mainnet networks
        and mocks a contract for development and ganache-local networks

        Args:
            contract_name: string

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed version of contract
    """
    contract_type = contract_to_mock[contract_name]
    print('current contract')
    print(contract_type)

    current_network = network.show_active()

    if current_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if (len(contract_type) <= 0):
            deploy_mock_aggregator()
        return contract_type[-1]
    else:
        contract_address = config["networks"][current_network][contract_name]
        return Contract.from_abi(contract_type._name, contract_address,contract_type.abi)
