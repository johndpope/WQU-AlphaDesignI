from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
from datetime import datetime

import backtrader as bt
import backtrader.indicators as btind

class MyStrategy(bt.Strategy):
    params = dict(period=20, period1=20, period2=25, period3=10, period4=2)
    # self.params = self.p

    def __init__(self):

        sma = btind.SimpleMovingAverage(period=self.p.period)
        sma1 = btind.SimpleMovingAverage(self.data, period=self.params.period1)
        sma2 = btind.SimpleMovingAverage(period=self.params.period2)

        myindicator = sma2-sm1 + self.datas[0].close
        self.mova = btind.SimpleMovingAverage(self.data, period=self.p.period1)

        self.sma = btind.SimpleMovingAverage(period=self.p.period)


        # see the (delay) notation
        self.cmpval = self.data.close(-1) > self.sma

        datasum = btind.SumN(self.data, period=self.p.period1)

        # using operators /
        av = datasum/self.p.period1
        self.line.sma = av

        # cannot use "and" operators, backtrader provides several methods
        close_over_sma = self.data.close > sma
        self.sma_dist_to_high = self.data.high - sma
        sma_dist_small = self.sma_dist_to_high < 3.5

        sell_sig = bt.And(close_over_sma, sma_dist_small)

        high_or_low = bt.If(sma1 > self.data.close, self.data.low, self.data.high)

    def start(self):
        print("Trading Strategy Simulation starts")

    def stop(self):
        print("Trading Strategy Simulation ends")




    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print('%s, %s,' %(dt.isoformat(),txt))


    def next(self):
        if self.mova.lines.sma[0] > self.data.lines.close[0]:
            print('Simple Moving Average is greater than the closing price')
        #xxx.lines could be shortened to xxx.l
         if self.data.close[0] > self.data.close[-1]:
             if self.data.close[-1] > self.data.close[-2]:
                 print('It is bullish 3-day close')

        if self.cmpval[0]:
            print('Previous close is higher than the moving average')
