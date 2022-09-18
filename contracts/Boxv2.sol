//SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Boxv2{

    uint private value;
    event requestValue(uint newValue);

    function store(uint newValue) public{
        value = newValue;
        emit requestValue(newValue);
    }

    function retrieve() public view returns(uint){
        return value;
    }

    function increment() public {
        value = value + 1;
        emit requestValue(value);
    }
}