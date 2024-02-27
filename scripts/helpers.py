from brownie import network, accounts, config

LOCAL_DEVELOPMENT = ['mainnet-fork','development']

def get_account(env_account = True, index:int=0):
    """
    Get an account
    :params : `env_account` set whether to use the account specified in the env or the one in the brownie accounts list
    True for env, False for config List
    :params: `index` The index of the development account you want to use. defaults to index 0
    """
    if network.show_active() in LOCAL_DEVELOPMENT:
        account = accounts[index]
    else:
        if env_account:
            account = accounts.add(config['wallets']['from'])
        else:
            account = accounts.load("mainaddress")
    return account