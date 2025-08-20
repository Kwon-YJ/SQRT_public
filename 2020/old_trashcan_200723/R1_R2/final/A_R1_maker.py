# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import pyautogui


# pyautogui.hotkey('ctrl', 'n')
# pyautogui.press('space')


def tab_press():
    pyautogui.press("space")
    pyautogui.press("space")
    pyautogui.press("space")
    pyautogui.press("space")


def str_write(string_data):
    pyautogui.typewrite(string_data)
    pyautogui.press("enter")
    time.sleep(1)


ticker_list = [
    "BTC",
    "ETH",
    "DASH",
    "LTC",
    "ETC",
    "XRP",
    "BCH",
    "ZEC",
    "QTUM",
    "BTG",
    "EOS",
    "ICX",
    "TRX",
    "ELF",
    "MCO",
    "OMG",
    "KNC",
    "GNT",
    "ZIL",
    "WAXP",
    "POWR",
    "LRC",
    "STEEM",
    "STRAT",
    "AE",
    "ZRX",
    "REP",
    "XEM",
    "SNT",
    "ADA",
    "CTXC",
    "BAT",
    "WTC",
    "THETA",
    "LOOM",
    "WAVES",
    "ITC",
    "TRUE",
    "LINK",
    "RNT",
    "ENJ",
    "PLX",
    "VET",
    "MTL",
    "INS",
    "IOST",
    "TMTG",
    "QKC",
    "BZNT",
    "HDAC",
    "NPXS",
    "LBA",
    "WET",
    "AMO",
    "BSV",
    "DAC",
    "ORBS",
    "VALOR",
    "CON",
    "ANKR",
    "MIX",
    "LAMB",
    "CRO",
    "FX",
    "CHR",
    "MBL",
    "MXC",
    "FAB",
    "OGO",
    "DVP",
    "FCT",
    "FNB",
    "TRV",
    "PCM",
    "DAD",
    "AOA",
    "XSR",
    "WOM",
    "SOC",
    "EM",
    "QBZ",
    "BOA",
    "FLETA",
    "SXP",
    "COS",
    "APIX",
    "EL",
    "BASIC",
    "XPR",
    "EGG",
    "ARPA",
    "BCD",
    "XLM",
    "PIVX",
    "GXC",
    "BTT",
    "HYC",
    "VSYS",
    "IPX",
    "WICC",
    "LUNA",
    "AION",
    "META",
    "COSM",
]

for i in range(len(ticker_list)):
    pyautogui.hotkey("ctrl", "n")
    time.sleep(1)

    str_write("# -*- coding: utf-8 -*- ")
    str_write("from R1_prototype import *")
    str_write("standby()")
    str_write("buy_side(" + '"' + ticker_list[i] + '"' + ")")
    str_write("sell_side(" + '"' + ticker_list[i] + '"' + ")")

    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)

    str_write(ticker_list[i] + ".py")

    pyautogui.hotkey("ctrl", "w")
    time.sleep(1)
