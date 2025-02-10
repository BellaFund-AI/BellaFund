// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Price Oracle Aggregator
 * @dev Fetches prices from multiple sources to prevent manipulation
 */
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract PriceOracle {
    struct Source {
        AggregatorV3Interface feed;
        uint8 weight;
    }
    
    Source[] public sources;
    uint256 public maxPriceDeviation = 5; // 5% maximum deviation
    
    function addPriceSource(address feedAddress, uint8 weight) external {
        sources.push(Source({
            feed: AggregatorV3Interface(feedAddress),
            weight: weight
        }));
    }
    
    function getSecurePrice() public view returns (int256) {
        require(sources.length > 0, "No price sources");
        
        int256[] memory prices = new int256[](sources.length);
        uint256 totalWeight;
        
        // Collect prices and validate consistency
        for (uint i=0; i<sources.length; i++) {
            (, int256 price,,,) = sources[i].feed.latestRoundData();
            prices[i] = price;
            totalWeight += sources[i].weight;
            
            if (i > 0) {
                uint256 deviation = uint256(
                    (abs(prices[i] - prices[i-1]) * 100) / prices[i-1]
                );
                require(deviation <= maxPriceDeviation, "Price deviation too high");
            }
        }
        
        // Calculate weighted average
        int256 weightedSum;
        for (uint i=0; i<sources.length; i++) {
            weightedSum += prices[i] * int256(sources[i].weight);
        }
        return weightedSum / int256(totalWeight);
    }
    
    function abs(int256 x) private pure returns (uint256) {
        return x >= 0 ? uint256(x) : uint256(-x);
    }
} 