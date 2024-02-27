
# Aave Borrow brownie

This is program use for interacting with aave protocol for borrowing and lending.

## Prerequisites
Please install or have installed the below program:

- [Python and pip](https://nodejs.org/en/download/)
- [nodejs and npm](https://nodejs.org/en/download/)

## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html), if you haven't already. Here is a simple way to install brownie.

```bash
pip install eth-brownie
```
Or, if that doesn't work, via pipx
```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```
2. Clone this repo
```
# open your terminal
git clone https://github.com/codebestia/TokenFarm.git
cd tokenfarm
cd contract
```

3. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```
If you want to be able to deploy to testnets, do the following. 

4. Set your environment variables

Set your `PRIVATE_KEY` [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). 

You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 


Create a .env file in the contract directory and add your environment variables to the `.env` file:

```
export PRIVATE_KEY=<PRIVATE_KEY>
```
> DO NOT SEND YOUR KEY TO GITHUB
> If you do that, people can steal all your funds. Ideally use an account with no real money in it. 


Then, make sure your `brownie-config.yaml` has:

```
dotenv: .env
```



## Usage/Examples

1. Get test weth to your account
```
brownie run scripts/get_weth.py --network goerli
```
you will need the weth as collateral for borrowing.

2. Deposit Weth, Borrow Dai, Repay Dai and Withdraw Weth.
```
brownie run scripts/get_weth.py --network goerli
```
This program will run all this interaction to the aave contract respectively

With this, you can now interact with the aave contract



## Future Improvements
- Get the repayment amount from AAVE
- Set the Token to borrow as a parameter
