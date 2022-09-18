from operator import ge
from scripts.helper import get_account, encode_function_data, upgrade_proxy
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, Boxv2

def deploy_box():
    account = get_account()
    box = Box.deploy({"from": account})
    # box cannot access any function of boxv2
    # I need to create like a proxy mirror of the boxv2, where it will contains all the functions
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address, 
                                               proxy_admin.address, 
                                               box_encoded_initializer, {"from": account, "gas_limit": 1000000})
    print(f"Proxy deployed to {proxy}, you can now upgrade to v2")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi) #assigining proxy to the box abi
    proxy_box.store(1, {"from": account})

    # Now implement the increment function from boxv2 to box
    # I need to cal the upgradeTo function from TransparentUpgradeableProxy

    #upgrade
    boxv2 = Boxv2.deploy({"from": account})
    upgrade_proxy(account, proxy, boxv2.address, proxy_admin=proxy_admin)
    print("proxy has been upgraded")
    proxy_box = Contract.from_abi("Boxv2", proxy.address, Boxv2.abi)
    proxy_box.increment({"from": account})
    print(proxy_box.retrieve())
    

def main():
    deploy_box()
