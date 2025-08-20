# -*- coding:utf-8 -*-
import numpy as np
import cv2
import os

from torch import save
import Utils
import time


def get_pixel_color(data):
    red = [0, 0, 255]
    green = [0, 255, 0]
    shadow_red = [0, 0, 120]
    shadow_green = [0, 120, 0]

    if red == list(data):
        return "R"
    elif green == list(data):
        return "G"
    elif shadow_green == list(data):
        return "SG"
    elif shadow_red == list(data):
        return "SR"
    else:
        return "B"


def ohlcv2img(tohlcv):
    result = []
    for data in tohlcv:
        result.append(data[1:-1])
    max_data, min_data = max(sum(result, [])), min(sum(result, []))
    for i in range(len(result)):
        result[i] = list(
            map(lambda x: (x - min_data) / (max_data - min_data), result[i])
        )

    # size = 100
    size = 2
    half_size = int(size / 2)
    img = np.zeros((size, size, 3), np.uint8)

    _1st_O, _1st_H, _1st_L, _1st_C = (
        result[0][0],
        result[0][1],
        result[0][2],
        result[0][3],
    )
    _2nd_O, _2nd_H, _2nd_L, _2nd_C = (
        result[1][0],
        result[1][1],
        result[1][2],
        result[1][3],
    )

    red = (0, 0, 255)
    green = (0, 255, 0)
    shadow_red = (0, 0, 120)
    shadow_green = (0, 120, 0)

    if _1st_O > _1st_C:
        _1st_color = [red, shadow_red]
    else:
        _1st_color = [green, shadow_green]

    if _2nd_O > _2nd_C:
        _2nd_color = [red, shadow_red]
    else:
        _2nd_color = [green, shadow_green]

    for i in range(half_size):
        cv2.line(
            img,
            (i, int(size * (1 - _1st_H))),
            (i, int(size * (1 - _1st_L))),
            _1st_color[1],
        )
        cv2.line(
            img,
            (i + half_size, int(size * (1 - _2nd_H))),
            (i + half_size, int(size * (1 - _2nd_L))),
            _2nd_color[1],
        )

    for i in range(half_size):
        cv2.line(
            img,
            (i, int(size * (1 - _1st_O))),
            (i, int(size * (1 - _1st_C))),
            _1st_color[0],
        )
        cv2.line(
            img,
            (i + half_size, int(size * (1 - _2nd_O))),
            (i + half_size, int(size * (1 - _2nd_C))),
            _2nd_color[0],
        )

    pixel = f"{get_pixel_color(img[0][0])}{get_pixel_color(img[0][1])}{get_pixel_color(img[1][0])}{get_pixel_color(img[1][1])}"

    # save_file_name = f'{os.getcwd()}/img_save/result.png'

    save_dir = f"{os.getcwd()}/img_save/{pixel}"

    # save_file_name = f'{os.getcwd()}/img_save/{pixel}'

    if os.path.isdir(save_dir) == False:
        os.mkdir(save_dir)
        time.sleep(1)
        os.mkdir(save_dir + "/True")
        time.sleep(1)
        os.mkdir(save_dir + "/False")

    save_file_name = f"{save_dir}/{GT}/{ticker[:-5]}{tohlcv[0][0]}.png"

    cv2.imwrite(save_file_name, img)


def main(ticker):
    timeframe = "5m"
    global GT
    GT = None  # ground_truth
    day = -3
    while 1:
        try:

            temp_time = Utils.timestamp_to_datetime(
                binance.fetch_ohlcv("BTC/USDT", "1d")[day][0]
            )[
                2
            ]  # 1h 기준 40의 배수
            convert = temp_time[:10] + "T" + temp_time[11:19] + "Z"
            timestamp = binance.parse8601(convert)

            ohlcvs = binance.fetch_ohlcv(ticker, timeframe, timestamp, 865)

            i = 0
            while 1:
                try:
                    target = ohlcvs[i : i + 3]
                    if target[-1][1] > target[-1][4]:
                        GT = False
                    else:
                        GT = True
                    ohlcv2img(target[:-1])
                except:
                    time.sleep(0.1)
                    print("Done")
                    break
                i += 3

            day = day - 3

        except:
            time.sleep(0.1)
            print("all_done")
            return None


if __name__ == "__main__":
    # BNB_ohlcv = [[1642291200000, 494.5, 506.0, 488.6, 498.6, 507042.332], [1642377600000, 498.6, 499.1, 466.9, 475.2, 757806.035], [1642464000000, 475.1, 479.6, 457.2, 471.4, 707501.577]]
    binance = Utils.use_binance()

    # ticker = 'DOT/USDT'

    ticker_list = [
        "BTC/USDT",
        "ETH/USDT",
        "BCH/USDT",
        "XRP/USDT",
        "EOS/USDT",
        "LTC/USDT",
        "TRX/USDT",
        "ETC/USDT",
        "LINK/USDT",
        "XLM/USDT",
        "ADA/USDT",
        "XMR/USDT",
        "DASH/USDT",
        "ZEC/USDT",
        "XTZ/USDT",
        "BNB/USDT",
        "ATOM/USDT",
        "ONT/USDT",
        "IOTA/USDT",
        "BAT/USDT",
        "VET/USDT",
        "NEO/USDT",
        "QTUM/USDT",
        "IOST/USDT",
        "THETA/USDT",
        "ALGO/USDT",
        "ZIL/USDT",
        "KNC/USDT",
        "ZRX/USDT",
        "COMP/USDT",
        "OMG/USDT",
        "DOGE/USDT",
        "SXP/USDT",
        "KAVA/USDT",
        "BAND/USDT",
        "RLC/USDT",
        "WAVES/USDT",
        "MKR/USDT",
        "SNX/USDT",
        "DOT/USDT",
        "YFI/USDT",
        "BAL/USDT",
        "CRV/USDT",
        "TRB/USDT",
        "YFII/USDT",
        "RUNE/USDT",
        "SUSHI/USDT",
        "SRM/USDT",
        "BZRX/USDT",
        "EGLD/USDT",
        "SOL/USDT",
        "ICX/USDT",
        "STORJ/USDT",
        "BLZ/USDT",
        "UNI/USDT",
        "AVAX/USDT",
        "FTM/USDT",
        "HNT/USDT",
        "ENJ/USDT",
        "FLM/USDT",
        "TOMO/USDT",
        "REN/USDT",
        "KSM/USDT",
        "NEAR/USDT",
        "AAVE/USDT",
        "FIL/USDT",
        "RSR/USDT",
        "LRC/USDT",
        "MATIC/USDT",
        "OCEAN/USDT",
        "CVC/USDT",
        "BEL/USDT",
        "CTK/USDT",
        "AXS/USDT",
        "ALPHA/USDT",
        "ZEN/USDT",
        "SKL/USDT",
        "GRT/USDT",
        "1INCH/USDT",
        "AKRO/USDT",
        "CHZ/USDT",
        "SAND/USDT",
        "ANKR/USDT",
        "LUNA/USDT",
        "BTS/USDT",
        "LIT/USDT",
        "UNFI/USDT",
        "DODO/USDT",
        "REEF/USDT",
        "RVN/USDT",
        "SFP/USDT",
        "XEM/USDT",
        "COTI/USDT",
        "CHR/USDT",
        "MANA/USDT",
        "ALICE/USDT",
        "HBAR/USDT",
        "ONE/USDT",
        "LINA/USDT",
        "STMX/USDT",
        "DENT/USDT",
        "CELR/USDT",
        "HOT/USDT",
        "MTL/USDT",
        "OGN/USDT",
        "BTT/USDT",
        "NKN/USDT",
        "SC/USDT",
        "DGB/USDT",
        "ICP/USDT",
        "BAKE/USDT",
        "GTC/USDT",
        "KEEP/USDT",
    ]

    for ticker in ticker_list:
        main(ticker)
