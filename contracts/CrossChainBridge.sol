// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Cross-Chain Asset Bridge
 * @dev Enables asset transfers between BNB Chain and Solana
 */
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract CrossChainBridge is ReentrancyGuard {
    struct BridgeRequest {
        address sender;
        uint256 amount;
        bytes32 targetAddress;
        uint64 targetChain;
    }
    
    mapping(bytes32 => bool) public completedTransactions;
    address public validator;
    
    event BridgeInitiated(
        bytes32 indexed txHash,
        address indexed sender,
        uint256 amount,
        bytes32 targetAddress,
        uint64 targetChain
    );
    
    constructor(address _validator) {
        validator = _validator;
    }
    
    function bridgeAssets(
        IERC20 token,
        uint256 amount,
        bytes32 solanaAddress
    ) external nonReentrant {
        require(token.transferFrom(msg.sender, address(this), amount));
        
        BridgeRequest memory request = BridgeRequest(
            msg.sender,
            amount,
            solanaAddress,
            1 // Chain ID: 1 for Solana
        );
        
        bytes32 txHash = keccak256(abi.encode(request));
        completedTransactions[txHash] = false;
        
        emit BridgeInitiated(
            txHash,
            msg.sender,
            amount,
            solanaAddress,
            1
        );
    }
    
    function completeBridge(
        bytes32 txHash,
        address recipient,
        uint256 amount,
        address tokenAddress
    ) external onlyValidator {
        require(!completedTransactions[txHash]);
        
        IERC20(tokenAddress).transfer(recipient, amount);
        completedTransactions[txHash] = true;
    }
    
    modifier onlyValidator() {
        require(msg.sender == validator);
        _;
    }
} 