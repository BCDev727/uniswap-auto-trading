# 6/6/2021
# Created by Lazer
# Trading bot on localhost/ropsten testnet

# ================================================> GUI Window <========================================================= #
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.messagebox import askyesno
import tkinter as tk

from toolz.itertoolz import join
from config import DEFAULT_BUY_IN, DEFAULT_BUY_OUT, DEFAULT_PRICE, DEFAULT_SELL_IN, DEFAULT_SELL_OUT, DEFAULT_GAS_PRICE, DEFAULT_GAS_FEE, DEFAULT_TOKEN

window = Tk()

lblAccountVal        = tk.StringVar()
lblBalanceVal        = tk.DoubleVar()
lblCurPriceVal       = tk.DoubleVar()
lblSigPriceVal       = tk.DoubleVar()
lblGapPriceVal       = tk.DoubleVar()
lblGapPriceLimit     = tk.StringVar()
txtAmountInVal       = tk.DoubleVar()
lblAmountInCurrency  = tk.StringVar()
txtAmountOutVal      = tk.DoubleVar()
lblAmountOutCurrency = tk.StringVar()
lblAmountEst         = tk.StringVar()
txtGasFeeVal         = tk.IntVar()
txtGasPriVal         = tk.IntVar()
lblGasEstVal         = tk.StringVar()
checkAuto            = tk.IntVar()
isAutoStarted = False
isAuto = False


# ==============================================> Trade <===============================================#

import sys
import json
import time
import requests
from decimal import Decimal
from web3 import Web3, contract
from config import CONTRACT_ADDRESS, CONTRACT_ABI, RECIPIENT_ADDRESS, PROVIDER_ADDRESS, PRIVATE_ADDRESS, TOKEN_LIST

class Trader:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/bb12f60463e14f6ea9257284fac7e3b7'))
        # Get the contract 
        abi = json.loads(CONTRACT_ABI)
        self.traderContract = self.w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)
        abi = json.loads(TOKEN_LIST[DEFAULT_TOKEN]['abi'])
        self.tokenContract = self.w3.eth.contract(address=TOKEN_LIST[DEFAULT_TOKEN]['address'], abi=abi)

    def resetToken(self, token=DEFAULT_TOKEN):
        abi = json.loads(TOKEN_LIST[token]['abi'])
        self.tokenContract = self.w3.eth.contract(address=TOKEN_LIST[token]['address'], abi=abi)
    
    def setCurPrice(self, token=DEFAULT_TOKEN):
        tokenAddress = TOKEN_LIST[token]['address']
        # tokenAddress = '0x6b175474e89094c44da98b954eedeac495271d0f' # if mainnet
        response = requests.get('https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses='+ tokenAddress +'&vs_currencies=usd')
        response_json = json.loads(response.content)
        if tokenAddress in response_json:
            lblCurPriceVal.set(response_json[tokenAddress]['usd'])
        else:
            lblCurPriceVal.set(DEFAULT_PRICE)


    def validateForm(self):
        amountIn  = txtAmountInVal.get()
        amountOut = txtAmountOutVal.get()
        gasPrice  = txtGasPriVal.get()
        gasFee    = txtGasFeeVal.get()
        if amountIn == '' or amountIn <= 0:
            messagebox.showwarning("Warning","Please input Amount In ( Value > 0 )")
            return 0
        if amountOut == '' or amountOut <= 0:
            messagebox.showwarning("Warning","Please input Amount Out ( Value > 0 )")
            return 0
        if gasPrice == '' or gasPrice <= 0:
            messagebox.showwarning("Warning","Please input Gas Price ( Value > 0 )")
            return 0
        if gasFee == '' or gasFee <= 0:
            messagebox.showwarning("Warning","Please input Gas Fee ( Value > 0 )")
            return 0
        return 1

    def initUI(self):
        # Show Account & Balance
        console_log('Current Account: ' + str(PROVIDER_ADDRESS))
        # show current balance of connected wallet
        console_log('Current Balance: ' + str(self.w3.fromWei(self.w3.eth.get_balance(PROVIDER_ADDRESS), 'ether')) + ' ETH')
        lblBalanceVal.set(self.w3.fromWei(self.w3.eth.get_balance(PROVIDER_ADDRESS), 'ether'))
        # show the current price between ETH and Token
        console_log('ETH/'+ DEFAULT_TOKEN +' Price : ' + str(self.traderContract.functions.getEstimatedETHforToken(TOKEN_LIST[DEFAULT_TOKEN]['address'], 1).call()))

        # default settings
        lblAccountVal.set(PROVIDER_ADDRESS)
        lblCurPriceVal.set(DEFAULT_PRICE)
        lblSigPriceVal.set(DEFAULT_PRICE)
        lblGapPriceVal.set(0.0)
        lblGapPriceLimit.set(' ( Must be < 25% ) ')
        txtAmountInVal.set(DEFAULT_BUY_IN)
        txtAmountOutVal.set(DEFAULT_BUY_OUT)
        lblAmountInCurrency.set('(ETH)')
        lblAmountOutCurrency.set('(DAI)')
        lblAmountEst.set(' ( Must be <= Estimated Max[0.0])')
        txtGasPriVal.set(DEFAULT_GAS_PRICE)
        txtGasFeeVal.set(DEFAULT_GAS_FEE)
        lblGasEstVal.set(' ( Must be >= Estimated Fee[0] )')
        checkAuto.set(0)

        window.mainloop()

    def updateUI(self, tradeType='BUY', token='DAI', sigPrice=0, amountIn=0, amountOut=0, gasFee=0, gasPrice=0):
        # Show Account & Balance
        console_log('Current Account: ' + str(PROVIDER_ADDRESS))
        self.resetToken(token)
        if tradeType == 'BUY':
            combo_type.current(0)
            console_log('Current Balance: ' + str(self.w3.fromWei(self.w3.eth.get_balance(PROVIDER_ADDRESS), 'ether')) + ' ETH')
            console_log('ETH/'+ token +' : ' + str(self.traderContract.functions.getEstimatedETHforToken(TOKEN_LIST[token]['address'], 1).call()))
            lblBalanceVal.set(self.w3.fromWei(self.w3.eth.get_balance(PROVIDER_ADDRESS), 'ether'))
            combo_currency['values'] = ('ETH')
            combo_currency.current(0)
            combo_currency['state'] = 'disable'
            combo_currency_out['state'] = 'readonly'
            combo_currency_out['values'] = list(TOKEN_LIST.keys())
            combo_currency_out.current(list(TOKEN_LIST.keys()).index(token))
            lblAmountInCurrency.set('(ETH)')
            lblAmountOutCurrency.set('('+ token +')')
        else:
            combo_type.current(1)
            console_log('Current Balance: ' + str(self.w3.fromWei(self.tokenContract.functions.balanceOf(PROVIDER_ADDRESS).call(), 'ether')) + ' ' +token)
            console_log(token +'/ETH : ' + str(self.traderContract.functions.getEstimatedTokenforETH(TOKEN_LIST[token]['address'], 1).call()))
            lblBalanceVal.set(self.w3.fromWei(self.tokenContract.functions.balanceOf(PROVIDER_ADDRESS).call(), 'ether'))
            combo_currency['state'] = 'readonly'
            combo_currency['values'] = list(TOKEN_LIST.keys())
            combo_currency.current(list(TOKEN_LIST.keys()).index(token))
            combo_currency_out['values'] = ('ETH')
            combo_currency_out.current(0)
            combo_currency_out['state'] = 'disable'
            lblAmountInCurrency.set('('+ token +')')
            lblAmountOutCurrency.set('(ETH)')
        # update settings
        if sigPrice > 0:
            self.setCurPrice()
            lblSigPriceVal.set(sigPrice)
            lblGapPriceVal.set(abs(lblCurPriceVal.get() - lblSigPriceVal.get()) * 100 / lblCurPriceVal.get())
        if gasPrice > 0:
            txtGasPriVal.set(gasPrice)
        if gasFee > 0:
            txtGasFeeVal.set(gasFee)
        if amountIn > 0:
            txtAmountInVal.set(amountIn)
        if amountOut > 0:
            txtAmountOutVal.set(amountOut)

    def buy(self, amountIn, amountOut, token, gasFee, gasPrice, isAuto):
        console_log('Buy start ==========>')
        # convert amounts
        _token     = self.w3.toChecksumAddress(token)
        # _token = token
        _amountIn  = self.w3.toWei(Decimal(amountIn), 'ether')
        _amountOut = self.w3.toWei(Decimal(amountOut), 'ether')
        _gasPrice    = self.w3.toWei(Decimal(gasPrice), 'gwei')
        # Get Estimated Amount Out
        estimatedAmount = self.traderContract.functions.getEstimatedETHforToken(_token, _amountIn).call()
        if isAuto:
            _amountOut = estimatedAmount - 100
            txtAmountOutVal.set(self.w3.fromWei(estimatedAmount, 'ether'))
        else:
            estimatedAmount = self.w3.fromWei(estimatedAmount, 'ether')
            if estimatedAmount < amountOut:
                console_log(' > Too high amount(estimated: ' + str(estimatedAmount) + ' )')
                lblAmountEst.set(' ( Must be <= Estimated Max['+ str(estimatedAmount) +'])')
                return
        nonce = self.w3.eth.get_transaction_count(PROVIDER_ADDRESS)
        transaction = self.traderContract.functions.Buy(
            _amountOut,
            _token,
            RECIPIENT_ADDRESS).buildTransaction({
                'gas': gasFee,
                'gasPrice': _gasPrice,
                'from': PROVIDER_ADDRESS,
                'value': _amountIn,
                'nonce': nonce
            })
        estimateFee = self.w3.eth.estimateGas(transaction={'to':CONTRACT_ADDRESS, 'from':PROVIDER_ADDRESS, 'value':_amountIn, 'data':transaction["data"]})
        if isAuto:
            gasFee = estimateFee + 100
            txtGasFeeVal.set(gasFee)
        else:    
            if estimateFee > gasFee:
                console_log(' > Too low gas(estimated: ' + str(estimateFee) + ')')
                lblGasEstVal.set(' ( Must be >= Estimated Fee['+ str(estimateFee) +'] )')
                return
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=PRIVATE_ADDRESS)
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_hash = self.w3.toHex(self.w3.keccak(signed_txn.rawTransaction))
        console_log(' > tx: ' + tx_hash)
        status = self.w3.eth.wait_for_transaction_receipt(tx_hash)['status']
        if status == True:
            console_log(' > Success !!!')
        else:
            console_log(' > Failed ~')
        console_log('Buy finished ==========>')

    def sell(self, amountIn, amountOut, token, gasFee, gasPrice, isAuto):
        print('Sell start ==========>')
        # convert amounts
        _token     = self.w3.toChecksumAddress(token)
        _amountIn  = self.w3.toWei(Decimal(amountIn), 'ether')
        _amountOut = self.w3.toWei(Decimal(amountOut), 'ether')
        _gasPrice    = self.w3.toWei(str(gasPrice), 'gwei')
        # Get Estimated Amount Out
        estimatedAmount = self.traderContract.functions.getEstimatedTokenforETH(_token, _amountIn).call()
        if isAuto:
            _amountOut = estimatedAmount - 100
            txtAmountOutVal.set(self.w3.fromWei(estimatedAmount, 'ether'))
        else:
            estimatedAmount = self.w3.fromWei(estimatedAmount, 'ether')
            if estimatedAmount < amountOut:
                console_log(' > Too high amount(estimated: ' + str(estimatedAmount) + ' )')
                lblAmountEst.set(' ( Must be <= Estimated Max['+ str(estimatedAmount) +'])')
                return
        # Approve provider to trader contract
        curAllowance = self.tokenContract.functions.allowance(PROVIDER_ADDRESS, CONTRACT_ADDRESS).call()
        if curAllowance < _amountIn:
            if _amountIn > self.approve(_amountIn, gasFee, _gasPrice, 30):
                print(' > Sorry, Insufficient allowances to trade')
                return
        else:
            print(' > Allowance: ' + str(curAllowance))
        # Swap token to ETH 
        nonce = self.w3.eth.get_transaction_count(PROVIDER_ADDRESS)
        transaction = self.traderContract.functions.Sell(
            _amountIn,
            _amountOut,
            _token,
            PROVIDER_ADDRESS).buildTransaction({
                'gas': gasFee,
                'gasPrice': _gasPrice,
                'from': PROVIDER_ADDRESS,
                'nonce': nonce
            })
        estimateFee = self.w3.eth.estimateGas(transaction={'to':CONTRACT_ADDRESS, 'from':PROVIDER_ADDRESS, 'value':0, 'data':transaction["data"]})
        if isAuto:
            gasFee = estimateFee + 100
            txtGasFeeVal.set(gasFee)
        else:
            if estimateFee > gasFee:
                print(' > Too low gas (estimated: ' + str(estimateFee) + ')')
                lblGasEstVal.set(' ( Must be >= Estimated Fee['+ str(estimateFee) +'] )')
                return
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=PRIVATE_ADDRESS)
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_hash = self.w3.toHex(self.w3.keccak(signed_txn.rawTransaction))
        print(' > tx: ' + str(tx_hash))
        status = self.w3.eth.wait_for_transaction_receipt(tx_hash)['status']
        if status:
            print(' > Success !!!')
        else:
            print(' > Failed ~')

        print('Sell finished <==========')

    def approve(self, amountIn, gasFee, gasPrice, delay):
        console_log(' > Approving now... ')
        nonce = self.w3.eth.get_transaction_count(PROVIDER_ADDRESS)
        transaction = self.tokenContract.functions.approve(CONTRACT_ADDRESS, amountIn).buildTransaction({
            'gas': gasFee,
            'gasPrice': gasPrice,
            'from': PROVIDER_ADDRESS,
            'nonce': nonce
        })
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=PRIVATE_ADDRESS)
        self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        for i in range(delay, 0, -1):
            sys.stdout.write("\r")
            sys.stdout.write("   (please wait for {:2d}s)".format(i))
            sys.stdout.flush()
            time.sleep(1)
        curAllowance = self.tokenContract.functions.allowance(PROVIDER_ADDRESS, CONTRACT_ADDRESS).call()
        console_log('\n')
        console_log(' > Current Allowance : ' + str(curAllowance))
        return curAllowance

# ================================================> GUI Details <========================================================= #

trader = Trader()

# Event Handler
def onTradeTypeChanged(e):
    trader.updateUI(combo_type.get())
def onCurrencyInChanged(e):
    trader.updateUI(combo_type.get(), combo_currency.get())
def onCurrencyOutChanged(e):
    trader.updateUI(combo_type.get(), combo_currency_out.get())
# window
window.title("Uniswap Trading Bot")
window.geometry('650x500')
window.resizable(False, False)
# tradig type(buy or sell)
combo_type = Combobox(window, width=6, state='readonly')
combo_type['values']= ("BUY", "SELL")
combo_type.current(0) #set default value as 'Buy'
combo_type['state'] = 'readonly'
combo_type.bind("<<ComboboxSelected>>", onTradeTypeChanged)
combo_type.grid(column=0, row=0, padx=20, pady=20, sticky="W")
# linked account
lbl_account_txt = Label(window, text='Account: ', width=15)
lbl_account_txt.grid(column=1, row=0, sticky="E")
lbl_account_val = Label(window, textvariable=lblAccountVal)
lbl_account_val.grid(column=2, row=0, sticky="W", columnspan=3)
# current balance
lbl_balance_txt = Label(window, text='Current Balance: ')
lbl_balance_txt.grid(column=0, row=1, padx=20, sticky="E")
lbl_balance_val = Label(window, textvariable=lblBalanceVal)
lbl_balance_val.grid(column=1, row=1, sticky="E")
combo_currency = Combobox(window, width=5)
combo_currency['values']= ("ETH")
combo_currency.current(0) #set default value as 'ETH'
combo_currency['state'] = 'disable'
combo_currency.bind("<<ComboboxSelected>>", onCurrencyInChanged)
combo_currency.grid(column=2, row=1, sticky="E")
lbl_exchange_sep = Label(window, text=' Swap to =====> ')
lbl_exchange_sep.grid(column=3, row=1)
combo_currency_out = Combobox(window, width=5)
combo_currency_out['values']= list(TOKEN_LIST.keys())
combo_currency_out.current(0) #set default value as 'ETH'
combo_currency_out['state'] = 'readonly'
combo_currency_out.bind("<<ComboboxSelected>>", onCurrencyOutChanged)
combo_currency_out.grid(column=4, row=1, sticky="W")
# current price
lbl_cur_price_txt = Label(window, text='Current Price: ')
lbl_cur_price_txt.grid(column=0, row=2, padx=20, sticky="E")
lbl_cur_price_val = Label(window, textvariable=lblCurPriceVal)
lbl_cur_price_val.grid(column=1, row=2, sticky="E")
lbl_cur_price_usd = Label(window, text='(USD)')
lbl_cur_price_usd.grid(column=2, row=2, sticky="W")
# signal price
lbl_sig_price_txt = Label(window, text='Signal Price: ')
lbl_sig_price_txt.grid(column=0, row=3, padx=20, sticky="E")
lbl_sig_price_val = Label(window, textvariable=lblSigPriceVal)
lbl_sig_price_val.grid(column=1, row=3, sticky="E")
lbl_sig_price_usd = Label(window, text='(USD)')
lbl_sig_price_usd.grid(column=2, row=3, sticky="W")
# gap price(%)
lbl_gap_price_txt = Label(window, text='Gap of Prices: ')
lbl_gap_price_txt.grid(column=0, row=4, padx=20, sticky="E")
lbl_gap_price_val = Label(window, textvariable=lblGapPriceVal)
lbl_gap_price_val.grid(column=1, row=4, sticky="E")
lbl_gap_price_usd = Label(window, text='(%)')
lbl_gap_price_usd.grid(column=2, row=4, sticky="W")
lbl_gap_price_lim = Label(window, textvariable=lblGapPriceLimit)
lbl_gap_price_lim.grid(column=3, row=4, sticky="W")
# amount In/Out/Estimated
lbl_amount_in_txt = Label(window, text='Amount In: ')
lbl_amount_in_txt.grid(column=0, row=5, padx=20, pady=10, sticky="E")
txt_amount_in_val = Spinbox(window, from_=0, to=10, width=25, textvariable=txtAmountInVal)
txt_amount_in_val.grid(column=1, row=5, sticky="E")
lbl_amount_in_usd = Label(window, textvariable=lblAmountInCurrency)
lbl_amount_in_usd.grid(column=2, row=5, sticky="W")
lbl_amount_out_txt = Label(window, text='Amount Out: ')
lbl_amount_out_txt.grid(column=0, row=6, padx=20, sticky="E")
txt_amount_out_val = Spinbox(window, from_=0, to=10, width=25, textvariable=txtAmountOutVal)
txt_amount_out_val.grid(column=1, row=6, sticky="E")
lbl_amount_out_usd = Label(window, textvariable=lblAmountOutCurrency)
lbl_amount_out_usd.grid(column=2, row=6, sticky="W")
lbl_amount_est_txt = Label(window, textvariable=lblAmountEst)
lbl_amount_est_txt.grid(column=3, row=6, sticky="W", columnspan=2)
# gas price
lbl_gas_price_txt = Label(window, text='Gas Price: ')
lbl_gas_price_txt.grid(column=0, row=7, padx=20, pady=10, sticky="E")
txt_gas_price_val = Spinbox(window, from_=0, to=50000, width=15, textvariable=txtGasPriVal)
txt_gas_price_val.grid(column=1, row=7, sticky="E")
lbl_gas_price_usd = Label(window, text='(GWI)')
lbl_gas_price_usd.grid(column=2, row=7, sticky="W", columnspan=2)
# gas fee
lbl_gas_fee_txt = Label(window, text='Gas Fee: ')
lbl_gas_fee_txt.grid(column=0, row=8, padx=20, sticky="E")
txt_gas_fee_val = Spinbox(window, from_=0, to=50000, width=15, textvariable=txtGasFeeVal)
txt_gas_fee_val.grid(column=1, row=8, sticky="E")
lbl_gas_est_txt = Label(window, textvariable=lblGasEstVal)
lbl_gas_est_txt.grid(column=3, row=8, sticky="W", columnspan=2)
# runtime lines
lbl_command_txt = Label(window, text='Runtime: ')
lbl_command_txt.grid(column=0, row=9, padx=20, sticky="E")
command_textbox = scrolledtext.ScrolledText(window,width=60,height=10)
command_textbox.config(background='#333', foreground='#fff')
command_textbox.grid(column=1, row=9, pady=10, sticky="E", columnspan=4)
# check auto
chk_auto = Checkbutton(window, text='Auto',variable=checkAuto, onvalue=1, offvalue=0)
chk_auto.grid(column=0, row=10, pady=10, sticky="E")

# ============================================> Events & Auto Trading <==============================================

from threading import Timer
import random
import config
from signals import TEST_SIGNALS

# # Event Handler
def isEnoughBalance(token):
    trader.updateUI(combo_type.get(), token)
    if txtAmountInVal.get() > lblBalanceVal.get():
        messagebox.showwarning("Warning","Insufficient Balance !!! ( Must be more than AmountIn: "+ str(txtAmountInVal.get()) +")")
        return 0
    return 1

def trade_start():
    if checkAuto.get() == 1: # auto trading
        auto_start()
    else: # manual trading
        if trader.validateForm():
            amountIn  = txtAmountInVal.get()
            amountOut = txtAmountOutVal.get()
            gasPrice  = txtGasPriVal.get()
            gasFee    = txtGasFeeVal.get()
            if combo_type.get() == 'BUY':
                token = combo_currency_out.get()
                if isEnoughBalance(token):
                    trader.buy(amountIn, amountOut, TOKEN_LIST[token]['address'], gasFee, gasPrice, False)
            else:
                token = combo_currency.get()
                if isEnoughBalance(token):
                    trader.sell(amountIn, amountOut, TOKEN_LIST[token]['address'], gasFee, gasPrice, False)
# Close window
def trade_exit():
    window.destroy()
    
def setInterval(timer, task):
    if task():
        Timer(timer, setInterval, [timer, task]).start()
        return True
    return False

# Auto Trading  
def auto_trade():
    # Check if balance is more than amountIn
    index = random.randint(0, len(TEST_SIGNALS) - 1)
    type  = TEST_SIGNALS[index]['type']
    token = TEST_SIGNALS[index]['token']
    price = TEST_SIGNALS[index]['price']
    console_log('[Signal'+ str(index + 1) +'] ===========================')
    if type == 'BUY':
        console_log('>>> ' + type + ' ETH => ' + token + ', Price: ' + str(price) + '$')
        amountIn = DEFAULT_BUY_IN
    else:
        console_log('>>> ' + type + ' '+ token +' => ETH, Price: ' + str(price) + '$')
        amountIn = DEFAULT_SELL_IN   
    trader.updateUI(type, token, price, amountIn)
    if not isEnoughBalance(token):
        global isAutoStarted
        isAutoStarted = False
        return 0
    if lblGapPriceVal.get() > 25:
        console_log(' > Too much price gap ('+ str(lblGapPriceVal.get()) +'%)')
        confirm_start('Gas Warning', 'Too much price gap ('+ str(lblGapPriceVal.get()) +'%) \n Are you try to trade again?')
        return
    gasPrice = txtGasPriVal.get()
    gasFee   = txtGasFeeVal.get()
    if type == 'BUY': 
        trader.buy(amountIn, DEFAULT_BUY_OUT, TOKEN_LIST[token]['address'], gasFee, gasPrice, True)
    else:
        trader.sell(amountIn, DEFAULT_SELL_OUT, TOKEN_LIST[token]['address'], gasFee, gasPrice, True)
    return isAutoStarted

# Start Auto
def auto_start():
    # Trading automatically every 60s
    global isAutoStarted
    isAutoStarted = True
    setInterval(60, auto_trade)
# Stop Auto
def auto_stop():
    if checkAuto.get() == 0:
        messagebox.showwarning("Warning","Trading Stop is available on Only Auto Trading")
        return
    global isAutoStarted
    if isAutoStarted:
        console_log(' > Auto Trade Stopping...')
        console_log('Stoped Auto Trading')
        isAutoStarted = False
    else:
        messagebox.showwarning("Warning","Auto Trading didn't start yet")
  
# Insert Console Log
def console_log(text):
    print(text)
    if command_textbox.get(INSERT) != '':
        text += '\n'
    command_textbox.insert(INSERT, text)
# Confirm Dialog
def confirm_start(title, content):
        answer = askyesno(title=title, message=content)
        if answer:
            trade_start()

# buttons
btn_trade = Button(window, text="Trade(Buy & Sell)", command=trade_start)
btn_trade.grid(column=1, row=10, pady=10, sticky="W")
btn_stop = Button(window, text="Stop", command=auto_stop)
btn_stop.grid(column=3, row=10, sticky="E")
btn_exit = Button(window, text="Exit", command=trade_exit)
btn_exit.grid(column=4, row=10, sticky="W")

if __name__ == '__main__':
    trader.initUI()