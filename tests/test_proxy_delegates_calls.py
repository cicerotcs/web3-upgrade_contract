from scripts.helper import get_account, encode_function_data, upgrade_proxy
from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract, Boxv2, exceptions
import pytest

def test_proxy_delegates_calls():
    #integration testing
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(box.address, proxy_admin.address, box_encoded_initializer, {"from": account})
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(1, {"from": account})
    assert proxy_box.retrieve() == 1
    # testing if i can call the inrement function before deploying the boxv2
    # with pytest.raises(exceptions.VirtualMachineError):
    #     proxy_box.increment({"from": account})
    boxv2 = Boxv2.deploy({"from": account})
    proxy_box = Contract.from_abi("Boxv2", proxy.address, boxv2.abi)
    upgrade_proxy(account, proxy, boxv2.address, proxy_admin=proxy_admin)
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 2
