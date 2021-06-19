
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.6.8;

interface IERC20 {
    event Approval(address indexed owner, address indexed spender, uint value);
    event Transfer(address indexed from, address indexed to, uint value);

    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
    function totalSupply() external view returns (uint);
    function balanceOf(address owner) external view returns (uint);
    function allowance(address owner, address spender) external view returns (uint);

    function approve(address spender, uint value) external returns (bool);
    function transfer(address to, uint value) external returns (bool);
    function transferFrom(address from, address to, uint value) external returns (bool);
}

// File: https://github.com/Uniswap/uniswap-v2-periphery/blob/master/contracts/interfaces/IUniswapV2Router01.sol

interface IUniswapV2Router01 {
    function factory() external pure returns (address);
    function WETH() external pure returns (address);

    function addLiquidity(
        address tokenA,
        address tokenB,
        uint amountADesired,
        uint amountBDesired,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline
    ) external returns (uint amountA, uint amountB, uint liquidity);
    function addLiquidityETH(
        address token,
        uint amountTokenDesired,
        uint amountTokenMin,
        uint amountETHMin,
        address to,
        uint deadline
    ) external payable returns (uint amountToken, uint amountETH, uint liquidity);
    function removeLiquidity(
        address tokenA,
        address tokenB,
        uint liquidity,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline
    ) external returns (uint amountA, uint amountB);
    function removeLiquidityETH(
        address token,
        uint liquidity,
        uint amountTokenMin,
        uint amountETHMin,
        address to,
        uint deadline
    ) external returns (uint amountToken, uint amountETH);
    function removeLiquidityWithPermit(
        address tokenA,
        address tokenB,
        uint liquidity,
        uint amountAMin,
        uint amountBMin,
        address to,
        uint deadline,
        bool approveMax, uint8 v, bytes32 r, bytes32 s
    ) external returns (uint amountA, uint amountB);
    function removeLiquidityETHWithPermit(
        address token,
        uint liquidity,
        uint amountTokenMin,
        uint amountETHMin,
        address to,
        uint deadline,
        bool approveMax, uint8 v, bytes32 r, bytes32 s
    ) external returns (uint amountToken, uint amountETH);
    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
    function swapTokensForExactTokens(
        uint amountOut,
        uint amountInMax,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
    function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts);
    function swapTokensForExactETH(uint amountOut, uint amountInMax, address[] calldata path, address to, uint deadline)
        external
        returns (uint[] memory amounts);
    function swapExactTokensForETH(uint amountIn, uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        returns (uint[] memory amounts);
    function swapETHForExactTokens(uint amountOut, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts);

    function quote(uint amountA, uint reserveA, uint reserveB) external pure returns (uint amountB);
    function getAmountOut(uint amountIn, uint reserveIn, uint reserveOut) external pure returns (uint amountOut);
    function getAmountIn(uint amountOut, uint reserveIn, uint reserveOut) external pure returns (uint amountIn);
    function getAmountsOut(uint amountIn, address[] calldata path) external view returns (uint[] memory amounts);
    function getAmountsIn(uint amountOut, address[] calldata path) external view returns (uint[] memory amounts);
}

// File: https://github.com/Uniswap/uniswap-v2-periphery/blob/master/contracts/interfaces/IUniswapV2Router02.sol

interface IUniswapV2Router02 is IUniswapV2Router01 {
    function removeLiquidityETHSupportingFeeOnTransferTokens(
        address token,
        uint liquidity,
        uint amountTokenMin,
        uint amountETHMin,
        address to,
        uint deadline
    ) external returns (uint amountETH);
    function removeLiquidityETHWithPermitSupportingFeeOnTransferTokens(
        address token,
        uint liquidity,
        uint amountTokenMin,
        uint amountETHMin,
        address to,
        uint deadline,
        bool approveMax, uint8 v, bytes32 r, bytes32 s
    ) external returns (uint amountETH);

    function swapExactTokensForTokensSupportingFeeOnTransferTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external;
    function swapExactETHForTokensSupportingFeeOnTransferTokens(
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external payable;
    function swapExactTokensForETHSupportingFeeOnTransferTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external;
}

// File: contracts/Trader.sol

abstract contract WETH9_ 
{
    mapping (address => uint)                       public  balanceOf;
    mapping (address => mapping (address => uint))  public  allowance;
    
    function deposit() virtual external payable;
    function withdraw(uint wad) virtual external;
    function totalSupply() virtual external view returns (uint);
    
    function approve(address guy, uint wad) virtual external returns (bool) ;
    function transfer(address dst, uint wad) virtual external returns (bool) ;
    function transferFrom(address src, address dst, uint wad) virtual external returns (bool);
}

contract Trader {
    address payable manager;
    address internal constant UNISWAP_ROUTER_ADDRESS = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D; //  Uniswap Router Address
    address internal constant WETH_ADDRESS = 0xc778417E063141139Fce010982780140Aa0cD5Ab; //  WETH Ropsten Address !! TO CHANGE
    WETH9_ internal WETH;
    IUniswapV2Router02 public uniswapRouter;
    // constructor
    constructor() public {
        uniswapRouter = IUniswapV2Router02(UNISWAP_ROUTER_ADDRESS);
        WETH = WETH9_(WETH_ADDRESS);
        manager = msg.sender;
    }
    // modifier
    modifier restricted() {
        require(msg.sender == manager, "manager allowed only");
        _;
    }
    // kill
    function kill() external restricted {
        selfdestruct(manager);
    }
    // trade - Buy
    function Buy(uint amountOutMin, address tokenAddress, address to) public payable restricted {
        uint deadline = block.timestamp + 30; // using 'now' for convenience, for mainnet pass deadline from frontend!
        uniswapRouter.swapExactETHForTokens{ value: msg.value }(amountOutMin, getPathForETHtoToken(tokenAddress), to, deadline);
    }
    // trade - Sell
    function Sell(uint amountIn, uint amountOutMin, address tokenAddress, address to) public payable restricted {
        IERC20 token = IERC20(tokenAddress);
        require(token.transferFrom(msg.sender, address(this), amountIn), "TransferFrom(sender, contract) Failed");
        require(token.approve(UNISWAP_ROUTER_ADDRESS, amountIn), "Approve to RouterV2 Failed");
        
        uint deadline = block.timestamp + 30; // using 'now' for convenience, for mainnet pass deadline from frontend!
        uniswapRouter.swapExactTokensForETH(amountIn, amountOutMin, getPathForTokentoETH(tokenAddress), to, deadline);
    }
    // Path(ETH-Token)
    function getPathForETHtoToken(address tokenAddress) private view returns (address[] memory) {
        address[] memory path = new address[](2);
        path[0] = uniswapRouter.WETH();
        path[1] = tokenAddress;
        
        return path;
    }
    // Path(Token-ETH)
    function getPathForTokentoETH(address tokenAddress) private view returns (address[] memory) {
        address[] memory path = new address[](2);
        path[0] = tokenAddress;
        path[1] = uniswapRouter.WETH();
        
        return path;
    }
    // Max Output of Token from ETH
    function getEstimatedETHforToken(address tokenAddress, uint tokenAmount) public view returns (uint256) {
        return uniswapRouter.getAmountsOut(tokenAmount, getPathForETHtoToken(tokenAddress))[1];
    }
    // Max Output of ETH from Token
    function getEstimatedTokenforETH(address tokenAddress, uint etherAmount) public view returns (uint256) {
        return uniswapRouter.getAmountsOut(etherAmount, getPathForTokentoETH(tokenAddress))[1];
    }
    function getAddress() public view returns (address) {
        return address(this);
    }
    // Approve for contract
    function approve(uint tokenAmount, address tokenAddress) external restricted {
        IERC20 token = IERC20(tokenAddress);
        token.transferFrom(msg.sender, address(this), tokenAmount);
        token.approve(address(this), tokenAmount);
    }
    // Balance of Token in contract
    function balanceOf(address tokenAddress) view public returns (uint) {
        return IERC20(tokenAddress).balanceOf(address(this));
    }
    // ETH => WETH
    function wrap() public payable restricted {
        if (msg.value != 0) {
            WETH.deposit{value : msg.value}();
            WETH.transfer(address(this), msg.value);
        }
    }
    // WETH => ETH
    function unwrap(uint amount) public payable restricted {
        if (amount != 0) {
            WETH.withdraw(amount);
            msg.sender.transfer(address(this).balance);
        }
    }
    // important to receive ETH
    receive() payable external {}
}