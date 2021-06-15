// SPDX-License-Identifier: MIT
pragma solidity 0.7.1;

import "https://github.com/Uniswap/uniswap-v2-periphery/blob/master/contracts/interfaces/IUniswapV2Router02.sol";

contract TestTrader {
  address internal constant UNISWAP_ROUTER_ADDRESS = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D ;

  IUniswapV2Router02 public _uniswapRouter;
  address private _token_address = 0xdC5dd8346ECb6D626862f17B3659c814eD4618a4;

  constructor() {
    _uniswapRouter = IUniswapV2Router02(UNISWAP_ROUTER_ADDRESS);
  }

  function convertEthToTTOK(uint tokenAmount) public payable {
    uint deadline = block.timestamp + 15; // using 'now' for convenience, for mainnet pass deadline from frontend!
    _uniswapRouter.swapETHForExactTokens{ value: msg.value }(tokenAmount, getPathForETHtoTTOK(), address(this), deadline);
    
    // refund leftover ETH to user
    (bool success,) = msg.sender.call{ value: address(this).balance }("");
    require(success, "refund failed");
  }

  function swapEthToTTOK(address to, uint tokenAmount) public payable {
    uint deadline = block.timestamp + 15; // using 'now' for convenience, for mainnet pass deadline from frontend!
    // require(getEstimatedTTOKforETH(msg.value) < tokenAmount, "Transaction reverted: Insufficient ETH to get tokens");
    _uniswapRouter.swapETHForExactTokens{ value: msg.value }(tokenAmount, getPathForETHtoTTOK(), to, deadline);
  }
  
  function getEstimatedETHforTTOK(uint tokenAmount) public view returns (uint[] memory) {
    return _uniswapRouter.getAmountsIn(tokenAmount, getPathForETHtoTTOK());
  }

  function getEstimatedTTOKforETH(uint ethAmount) public view returns (uint) {
    return _uniswapRouter.getAmountsOut(ethAmount, getPathForETHtoTTOK())[1];
  }

  function getPathForETHtoTTOK() private view returns (address[] memory) {
    address[] memory path = new address[](2);
    path[0] = _uniswapRouter.WETH();
    path[1] = _token_address;
    
    return path;
  }
  
  // important to receive ETH
  receive() payable external {}
}