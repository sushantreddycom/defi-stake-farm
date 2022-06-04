

// unstake tokens


// burn tokens

// add Allowed tokens

// get eth value

// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";


contract TokenFarm is Ownable{ 

    address[] public allowedTokensToStake;
    // mapping token address -> staker address -> amount
    mapping (address => mapping(address => uint256)) public stakedBalances;
    mapping (address => uint256) public uniqueTokensStaked;
    address[] public stakers;
    mapping(address => address) public tokenPriceFeedMapping;
    IERC20 public cheruToken;

    // stake tokens
    function stakeTokens(uint256 _amount, address _stakedToken) public{
        require (_amount >0, "Failed: Staked amount should be non zero");

        require(isAllowedToken(_stakedToken), "Failed: Token is not in list of allowed tokens");


        IERC20(_stakedToken).transferFrom(msg.sender, address(this), _amount);
        
        updateUniqueTokensStaked(msg.sender, _stakedToken);
        stakedBalances[_stakedToken][msg.sender] += _amount;

        if (uniqueTokensStaked[msg.sender] == 1){
            stakers.push(msg.sender);
        }
    }

    // set price feed contracts
    function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    function updateUniqueTokensStaked(address sender, address token) internal {
        if(stakedBalances[token][sender] <= 0){
            uniqueTokensStaked[sender] += 1;
        }
    }

    // define a constructor with CheruToken
    constructor (address _cheruToken) public {
        cheruToken = IERC20(_cheruToken);
    }

    // issue tokens - we issue tokens as reward for users who stake their tokens o
    // on our platform
    function issueTokens() public onlyOwner{
        for(uint256 stakeIndx=0; stakeIndx <stakers.length; stakeIndx++){
            address recepient = stakers[stakeIndx];
            uint256 transferValue = getTotalTransferValue(recepient);
            cheruToken.transfer(recepient, transferValue);
        }   
    }

    function tokenBalance(address _token, address _staker) public returns(uint256) {
        require(isAllowedToken(_token), "Not a valid token for staking");

        require (isValidStaker(_staker), "Not a valid staker");

        return stakedBalances[_token][_staker];

    }

    // unstake token
    // return balance to sender
    // remove the balance from stakedBalances
    // reduce uniqueStakedTokens by one
    
    function unstakeTokens(address _token) public {
        uint256 balance = stakedBalances[_token][msg.sender];
        require(balance > 0 , "No balance");

        IERC20(_token).transfer(msg.sender, balance);
        stakedBalances[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender] -= 1;

    }

    // get total transfer value for a particular staken
    // this is sum total of all tokens staked by user multiplied by their current prices

    function getTotalTransferValue(address _staker) public view returns(uint256){
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_staker] > 0, "No tokens staked by current user");

        // loop over all allowed tokens
        for (uint256 allowedTokenIndx = 0; allowedTokenIndx < allowedTokensToStake.length; allowedTokenIndx++){
            totalValue += getTransferValuePerToken(_staker, allowedTokensToStake[allowedTokenIndx]);
        }    

        return totalValue;
    }

    // total amount to transfer per toekn per user
    function getTransferValuePerToken(address _staker, address _token) public view returns(uint256){
        // no tokens staked by a user
        if(uniqueTokensStaked[_staker] <= 0){
            return 0;
        }

        // 
        if(stakedBalances[_token][_staker]==0){
            return 0;
        }
        (uint256 price, uint256 decimals) = getPrice(_token);
        return stakedBalances[_token][_staker] * price / 10**decimals;

    }

    //get Price for a given token
    function getPrice(address _token) public view returns(uint256, uint256){
        address priceFeedAddress = tokenPriceFeedMapping[_token];


        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        (,int256 price,,,)= priceFeed.latestRoundData();

        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function isValidStaker(address _staker) internal returns(bool) {
        for(uint256 indx=0; indx < stakers.length; indx++){
            if(_staker == stakers[indx]){
                 return true;   
            }
        }
        return false;
    }

    // is token allowed to stake
    function isAllowedToken(address _token) public returns(bool) {
        for (uint256 indx = 0; indx < allowedTokensToStake.length; indx++){
            if(_token == allowedTokensToStake[indx]){
                return true;
            }
        }
        return false;
    }

    // add allowed token
    // function only owner can perform, add onlyOwner modifier
    function addAllowedToken(address _token) onlyOwner public returns(bool) {
        bool isAllowed = isAllowedToken(_token);
        if(!isAllowed){
            // add only if address does not exist already
            allowedTokensToStake.push(_token);
            return true;
        }

        // if already exists, simply skip
        return false;
    }

}