from brownie import network, accounts, config

import eth_utils

LOCAL_TEST = ["development", "ganache-local"]

def get_account():
    if(network.show_active() in LOCAL_TEST):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def encode_function_data():
    return eth_utils.to_bytes(hexstr="0x") #low level os solidity and evm

def upgrade_proxy(account, proxy, new_implementation_address, proxy_admin):
    transaction = proxy_admin.upgrade(proxy.address,
                                      new_implementation_address,
                                      {"from": account}) # this function comes from ProxyAdmin file
    return transaction