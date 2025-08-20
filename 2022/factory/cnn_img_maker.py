# -*- coding:utf-8 -*-
import numpy as np
import cv2
import os
import Utils


def ohlcv2img(tohlcv):
    result = []
    for data in tohlcv:
        result.append(data[1:-1])
    max_data, min_data = max(sum(result, [])), min(sum(result, []))
    for i in range(len(result)):
        result[i] = list(
            map(lambda x: (x - min_data) / (max_data - min_data), result[i])
        )

    size = 100
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

    save_file_name = f"{os.getcwd()}/result.png"
    cv2.imwrite(save_file_name, img)

    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyALLWindows()

    # return result


if __name__ == "__main__":
    # BNB_ohlcv = [[1642291200000, 494.5, 506.0, 488.6, 498.6, 507042.332], [1642377600000, 498.6, 499.1, 466.9, 475.2, 757806.035], [1642464000000, 475.1, 479.6, 457.2, 471.4, 707501.577]]
    binance = Utils.use_binance()

    BNB_ohlcv = binance.fetch_ohlcv("BTC/USDT", "1w")[-2:]

    ohlcv2img(BNB_ohlcv)
