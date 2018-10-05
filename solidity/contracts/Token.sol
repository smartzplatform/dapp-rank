pragma solidity ^0.4.23;

import 'zeppelin-solidity/contracts/token/ERC20/PausableToken.sol';


contract Token is PausableToken {
    string public constant tokenName = "CurationToken";
    string public constant symbol = "CRN";
    uint8 public constant decimals = 18;

    uint256 public constant INITIAL_SUPPLY = 1000000 * (10 ** uint256(decimals));

    constructor() public {
        totalSupply_ = INITIAL_SUPPLY;
        balances[msg.sender] = INITIAL_SUPPLY;
        emit Transfer(address(0), msg.sender, INITIAL_SUPPLY);
    }
}
