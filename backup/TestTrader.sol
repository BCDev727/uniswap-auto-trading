// SPDX-License-Identifier: MIT
pragma solidity ^0.7.1;

// import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v3.0.0/contracts/token/ERC20/IERC20.sol";
import "https://github.com/Uniswap/uniswap-v2-periphery/blob/master/contracts/interfaces/IUniswapV2Router02.sol";

contract TestTrader {
  address internal constant UNISWAP_ROUTER_ADDRESS = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D ;

  IUniswapV2Router02 public _uisRouter;
  address private _weth;

  constructor() {
    _uisRouter = IUniswapV2Router02(UNISWAP_ROUTER_ADDRESS);
    _weth = _uisRouter.WETH();
  }

  // function buy(address to, uint tkQty) public payable returns(uint256){
  //   uint deadline = block.timestamp + 15; // using 'now' for convenience, for mainnet pass deadline from frontend!
  //   // require(getEstimatedTTOKforETH(msg.value) < tokenAmount, "Transaction reverted: Insufficient ETH to get tokens");
  //   // _uisRouter.swapETHForExactTokens{ value: msg.value }(tokenAmount, getPathForETHtoTTOK(), to, deadline);

  //   _uisRouter.swapETHForExactTokens(tkQty, getPathForETHtoTK(_tk1), to, deadline);

  //   return tkQty;
  // }

  function sell(address to, address tkAddr, uint tkQty, uint ethQty) public payable returns(uint256){
    uint deadline = block.timestamp + 15; // using 'now' for convenience, for mainnet pass deadline from frontend!
    // require(getEstimatedTTOKforETH(msg.value) < tokenAmount, "Transaction reverted: Insufficient ETH to get tokens");

    // uint estimatedEthQty = getEstimatedTKforETH(tkQty, tkAddr)[1];

    _uisRouter.swapExactTokensForETH(tkQty, ethQty, getPathForTKtoETH(tkAddr), to, deadline);

    return ethQty;
  }
  
  // function getEstimatedETHforTK(uint ethQty, address ethAddr) public view returns (uint[] memory) {
  //   return _uisRouter.getAmountsIn(ethQty, getPathForETHtoTK(ethAddr));
  // }

  function getEstimatedTKforETH(uint tkQty, address tkAddr) public view returns (uint[] memory) {
    return _uisRouter.getAmountsOut(tkQty, getPathForTKtoETH(tkAddr));
  }
  // ETH/TOKEN pair
  function getPathForETHtoTK(address tkAddr) private view returns (address[] memory) {
    address[] memory path = new address[](2);
    path[0] = _weth;
    path[1] = tkAddr;
    
    return path;
  }
  // TOKEN/ETH pair
  function getPathForTKtoETH(address tkAddr) private view returns (address[] memory) {
    address[] memory path = new address[](2);
    path[0] = tkAddr;
    path[1] = _weth;
    
    return path;
  }
  
  // important to receive ETH
  receive() payable external {}
}