# 6/6/2021
# Created by Lazer
# Trading bot on localhost/ropsten testnet

import json
from web3 import Web3, contract
import config as Config

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/bb12f60463e14f6ea9257284fac7e3b7'))
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Set default account
w3.eth.default_account = w3.eth.accounts[0]
print('Currnet Account: ' + str(Config.PROVIDER_ADDRESS))
print('Current Balance: ' + str(w3.fromWei(w3.eth.get_balance(Config.PROVIDER_ADDRESS), 'ether')) + ' ETH')

# Get the contract 
conJson = open('../build/contracts/Trader.json','r')
conJson = json.load(conJson)
abi      = conJson['abi']
bytecode = conJson['bytecode']
Trader = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = Trader.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print('Contract Address: ' + tx_receipt.contractAddress)
contract = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi,
)
# Call functions in contract
print('DAI/ETH Price : ' + str(contract.functions.getEstimatedTKforETH(Config.TOKEN_ADDRESS, 1).call()))

nonce = w3.eth.get_transaction_count(Config.PROVIDER_ADDRESS)

transaction = contract.functions.buy(
    Config.RECIPIENT_ADDRESS,
    550000000000000000 ).buildTransaction({
    'gas': 70000,
    'gasPrice': w3.toWei('1', 'gwei'),
    'from': Config.PROVIDER_ADDRESS,
    'nonce': nonce
}) 
signed_txn = w3.eth.account.signTransaction(transaction, private_key=Config.PRIVATE_ADDRESS)
# w3.eth.sendRawTransaction(signed_txn.rawTransaction)

print(w3.toHex(w3.keccak(signed_txn.rawTransaction)))