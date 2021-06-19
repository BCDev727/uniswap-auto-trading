# import PySimpleGUI as sg
from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
import tkinter as tk

window = Tk()

lblAccountVal  = tk.StringVar()
lblBalanceVal  = tk.DoubleVar()
lblCurPriceVal = tk.DoubleVar()
lblSigPriceVal = tk.DoubleVar()
lblGapPriceVal = tk.DoubleVar()
lblGapPriceLimit = tk.StringVar()
lblGapPriceLimit.set(' ( Must be < 25% ) ')
txtAmountInVal  = tk.DoubleVar()
txtAmountOutVal = tk.DoubleVar()
lblGasFeeVal = tk.IntVar()
lblGasEstVal = tk.StringVar()
lblGasEstVal.set(' ( Must be >= Estimated Fee[0] )')

# window
window.title("Uniswap Trading Bot")
window.geometry('550x450')
# tradig type(buy or sell)
combo_type = Combobox(window, width=6)
combo_type['values']= ("Buy", "Sell")
combo_type.current(0) #set default value as 'Buy'
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
combo_currency['values']= ("ETH", "DAI")
combo_currency.current(0) #set default value as 'ETH'
combo_currency.grid(column=2, row=1, sticky="W")
lbl_exchange_sep = Label(window, text=' Swap to =====> ')
lbl_exchange_sep.grid(column=3, row=1)
combo_currency_out = Combobox(window, width=5)
combo_currency_out['values']= ("ETH", "DAI")
combo_currency_out.current(1) #set default value as 'ETH'
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
lbl_gap_price_lim = Label(window, text=lblGapPriceLimit)
lbl_gap_price_lim.grid(column=3, row=4, sticky="W")
# amount In/Out/Estimated
lbl_amount_in_txt = Label(window, text='Amount In: ')
lbl_amount_in_txt.grid(column=0, row=5, padx=20, pady=5, sticky="E")
txt_amount_in_val = Spinbox(window, from_=0, to=10, width=15, textvariable=txtAmountInVal)
txt_amount_in_val.grid(column=1, row=5, sticky="E", columnspan=2)
lbl_amount_out_txt = Label(window, text='Amount Out: ')
lbl_amount_out_txt.grid(column=0, row=6, padx=20, pady=5, sticky="E")
txt_amount_out_val = Spinbox(window, from_=0, to=10, width=15, textvariable=txtAmountOutVal)
txt_amount_out_val.grid(column=1, row=6, sticky="E", columnspan=2)
lbl_amount_est_txt = Label(window, text=' ( Must be <= Estimated MaxOut[0] )')
lbl_amount_est_txt.grid(column=3, row=6, sticky="W", columnspan=2)
# gas fee
lbl_gas_fee_txt = Label(window, text='Gas Fee: ')
lbl_gas_fee_txt.grid(column=0, row=7, padx=20, sticky="E")
lbl_gas_fee_val = Label(window, textvariable=lblGasFeeVal)
lbl_gas_fee_val.grid(column=1, row=7, sticky="E")
lbl_gas_fee_sep = Label(window, text='')
lbl_gas_fee_sep.grid(column=2, row=7)
lbl_gas_est_txt = Label(window, text=lblGasEstVal)
lbl_gas_est_txt.grid(column=3, row=7, sticky="W", columnspan=2)
# runtime lines
lbl_command_txt = Label(window, text='Runtime: ')
lbl_command_txt.grid(column=0, row=8, padx=20, pady=20, sticky="E")
command_textbox = scrolledtext.ScrolledText(window,width=40,height=10)
command_textbox.configure(state ='disabled')
command_textbox.grid(column=1, row=8, sticky="E", columnspan=4)

# start trading
def trade_start():
    print('trade starting')

# stop trading
def trade_stop():
    print('trade stoping')
# close window
def trade_exit():
    window.destroy()

# buttons
btn_trade = Button(window, text="Trade(Buy & Sell)", command=trade_start)
btn_trade.grid(column=0, row=9, pady=20, sticky="E")
btn_stop = Button(window, text="Stop", command=trade_stop)
btn_stop.grid(column=1, row=9, sticky="E")
btn_exit = Button(window, text="Exit", command=trade_exit)
btn_exit.grid(column=2, row=9, sticky="E")
    
window.mainloop()

# # Event Handler
# msg box
def msg_info(title, content):
    messagebox.showinfo(title, content)
def console_log(text):
    print(text)
    command_textbox.insert(INSERT, text)
