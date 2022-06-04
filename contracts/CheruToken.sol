// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract CheruToken is ERC20 {

    constructor() public ERC20 ("CheruToken", "CHE"){
        _mint(msg.sender, 1000000000000000000000000); // 1 million tokens
    }
}