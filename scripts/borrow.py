from brownie import config, network, interface
from scripts.get_weth import get_weth
from scripts.helpers import get_account, LOCAL_DEVELOPMENT
from web3 import Web3

AMOUNT = Web3.toWei(0.01,'ether') # Amount that i will be dealing with for this program
RATE_MODE = 2.43 # interest rate mode. this changes from time to time, check the aave governance page for the new value before running the program 

def main():
    """
    Steps to achieve with program
    - Get weth if network is mainnet-fork
    - Approve Erc20 deposit for token
    - Deposit into Lending Pool
    - View amount of eth i can borrow
    - Borrow from Lending Pool (DAI in USD conversion)
    - 
    """
    if network.show_active == LOCAL_DEVELOPMENT[0]:
        get_weth()
    account =  get_account()
    lending_pool = get_lending_pool()
    weth_token_address = config['networks'][network.show_active()]['weth-token']
    print("Approving ERC20")
    approve_tx = approve_erc20(AMOUNT,lending_pool.address,weth_token_address,account)
    print("ERC20 Amount Approved")
    print("Deposit to Lending Pool")
    tx = lending_pool.deposit(
        weth_token_address,
        AMOUNT,
        account.address,
        0,
        {'from':account}
    )
    tx.wait(1)
    print("Deposited")
    print("Viewing Borrowable Amount")
    get_borrowable_data(lending_pool,account)
    print("Borrowing DAI from pool")
    asset_to_borrow = config['networks'][network.show_active()]['dai-token']
    asset_price = get_asset_price(config['networks'][network.show_active()]['dai-price-feed'])
    print(asset_price)
    borrowable_amount  = Web3.toWei(0.02,"ether")
    tx = lending_pool.borrow(
        asset_to_borrow,
        borrowable_amount,
        RATE_MODE,
        0,
        account.address,
        {'from':account,'gas_limit':1000000, 'allow_revert':True}
    )
    tx.wait(1)
    print("DAI borrowed")
    print("Viewing Borrowable Amount")
    get_borrowable_data(lending_pool,account)
    print("Repaying Assets")
    repay_all(borrowable_amount,lending_pool,account)
    withdraw_deposit(AMOUNT,lending_pool,account)
    print("All Program steps have been completed. you have successfully interacted with the aave contract 🎉");


def withdraw_deposit(amount,lending_pool, account):
    """
    Withdraw the amount you lended
    steps:
    - Approve the funds from the lending pool
    - Withdraw the funds (fails if no funds exist)
    """
    print("Approving Withdrawal")
    approve_erc20(amount, account.address, config['networks'][network.show_active()]['weth-token'],account)
    print("Making Withdrawal")
    lending_pool.withdraw(
        config['networks'][network.show_active()]['weth-token'],
        amount,
        account.address,
        {'from':account}
    )
    print("Withdrawal successful")



def repay_all(amount, lending_pool, account):
    """
    Approve the erc20 token transfer and repay the debt of the token.
    
    """
    approve_erc20(
        amount,
        lending_pool,
        config["networks"][network.show_active()]["dai-token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai-token"],
        amount,
        RATE_MODE, # 
        account.address, 
        {"from": account},
    )
    repay_tx.wait(1)

    print("Repaid!")


def get_asset_price(price_feed_address):
    dai_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_price_feed.latestRoundData()[1]
    # converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/USD price is {latest_price}")
    return float(latest_price)


def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth), float(total_collateral_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


def get_lending_pool():
    print("Getting Lending Pool")
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_provider"]
    )
    # print(lending_pool_addresses_provider.address)
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    print(f"Lending Pool Address: {lending_pool_address}")
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
