// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Bella Governance Token
 * @dev ERC-20 with staking rewards and voting power
 */
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";

contract BGLToken is ERC20Votes {
    address public treasury;
    uint256 public constant MAX_SUPPLY = 1e27; // 1 billion tokens
    
    constructor() ERC20("Bella Governance", "BGL") ERC20Permit("Bella") {
        treasury = msg.sender;
        _mint(treasury, MAX_SUPPLY);
    }
    
    function stake(uint256 amount) public {
        _burn(msg.sender, amount);
        _mint(address(this), amount);
    }
    
    function unstake(uint256 amount) public {
        _burn(address(this), amount);
        _mint(msg.sender, amount);
    }
    
    function votingPower(address account) public view returns (uint256) {
        return getVotes(account);
    }
} 