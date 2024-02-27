from brownie import network, accounts, interface, config
from web3 import Web3
from scripts.helpers import get_account


def main():
    get_weth()

def get_weth(amount = 0.1):
    account = get_account()
    eth_amount = Web3.toWei(amount,'ether')
    weth_config = config['networks'][network.show_active()]['weth-token']
    print(network.show_active())
    print(weth_config)
    weth_token = interface.IWeth(weth_config)
    tx = weth_token.deposit({'from':account,'value':eth_amount})
    tx.wait(1) # wait 1 block confirmation
    print(f"Recieved Weth Token of {Web3.fromWei(eth_amount,'ether')}")


