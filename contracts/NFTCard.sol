// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Cross-chain Compatible Rating NFT
 * @dev Stores token rating with expiration and chain context
 */
import "@openzeppelin/contracts/utils/Address.sol";

contract RatingCard is ERC721URIStorage {
    enum ChainType { 
        BNB,    // BNB Smart Chain (BEP-20)
        Solana  // Solana SPL tokens
    }
    
    struct CardData {
        ChainType chain;       // Blockchain network identifier
        uint256 score;         // AI-generated rating score (0-100 scale)
        bytes32 tokenAddress;  // Cross-chain compatible address storage
        uint256 expiration;    // Score validity expiration timestamp
    }
    
    mapping(uint256 => CardData) public cardData;
    uint256 public tokenCounter;
    
    constructor() ERC721("BellaFundCard", "BFC") {
        tokenCounter = 0;
    }
    
    /// @notice Mint new NFT card with provided metadata
    /// @param chainType 0 for BNB, 1 for Solana
    /// @param tokenAddress Packed token address (32 bytes for cross-chain)
    function mintCard(
        address owner,
        string memory tokenURI,
        uint256 score,
        ChainType chainType,
        bytes32 tokenAddress
    ) public returns (uint256) {
        uint256 newId = tokenCounter++;
        _mint(owner, newId);
        _setTokenURI(newId, tokenURI);
        
        cardData[newId] = CardData({
            chain: chainType,
            score: score,
            tokenAddress: tokenAddress,
            expiration: block.timestamp + 30 days
        });
        return newId;
    }

    /// @notice Check if rating is still valid
    function isRatingValid(uint256 tokenId) public view returns (bool) {
        return cardData[tokenId].expiration > block.timestamp;
    }

    /// @notice Update card metadata (restricted to owner)
    function updateScore(
        uint256 tokenId, 
        uint256 newScore, 
        uint256 newExpiration
    ) public onlyOwner {
        require(_exists(tokenId), "Nonexistent token");
        cardData[tokenId].score = newScore;
        cardData[tokenId].expiration = newExpiration;
    }
} 