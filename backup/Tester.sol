// SPDX-License-Identifier: MIT
pragma solidity 0.7.1;

import "https://github.com/Uniswap/uniswap-v2-periphery/blob/master/contracts/interfaces/IUniswapV2Router02.sol";

contract TestTrader {
  address internal constant UNISWAP_ROUTER_ADDRESS = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D ;

  IUniswapV2Router02 public _uniswapRouter;

  constructor() {
    _uniswapRouter = IUniswapV2Router02(UNISWAP_ROUTER_ADDRESS);
  }

  function buy(address to, address tokenAddress, uint tokenAmount) public payable {
    uint deadline = block.timestamp + 15; // using 'now' for convenience, for mainnet pass deadline from frontend!
    require(getEstimatedTKforETH(msg.value)[0] < tokenAmount, "Transaction reverted: Insufficient ETH to get Tokens");
    _uniswapRouter.swapETHForExactTokens{ value: msg.value }(tokenAmount, getPathForETHtoTK(tokenAddress), to, deadline);
  }
  
  function sell(address to, address tokenAddress, uint tokenAmount, uint etherAmount) public payable {
    uint deadline = block.timestamp + 15; // using 'now' for convenience, for mainnet pass deadline from frontend!
    require(getEstimatedETHforTK(tokenAmount)[0] < etherAmount, "Transaction reverted: Insufficient Tokens to get ETH");
    _uniswapRouter.swapTokensForExactETH(tokenAmount, etherAmount, getPathForTKtoETH(tokenAddress), to, deadline);
  }
  
  function getEstimatedETHforTK(address tokenAddress, uint tokenAmount) public view returns (uint[] memory) {
    return _uniswapRouter.getAmountsIn(tokenAmount, getPathForETHtoTK(tokenAddress));
  }

  function getEstimatedTKforETH(address tokenAddress, uint etherAmount) public view returns (uint[] memory) {
    return _uniswapRouter.getAmountsIn(etherAmount, getPathForTKtoETH(tokenAddress));
  }

  function getPathForETHtoTK(address tokenAddress) private view returns (address[] memory) {
    address[] memory path = new address[](2);
    path[0] = _uniswapRouter.WETH();
    path[1] = tokenAddress;  
    return path;
  }

  function getPathForTKtoETH(address tokenAddress) private view returns (address[] memory) {
    address[] memory path = new address[](2);
    path[0] = tokenAddress;
    path[1] = _uniswapRouter.WETH();
    return path;
  }
  
  // important to receive ETH
  receive() payable external {}
}