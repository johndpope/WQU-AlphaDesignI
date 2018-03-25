from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt


class MyIndicator(bt.indicators.SimpleMovingAverage):
    plotlines = dict(
        sma = dict(color="green")
    )

class St(bt.SignalStrategy):
    lines = ('signal', )

    def __init__(self):
        #self.sma = bt.indicators.SimpleMovingAverage(self.data)
        self.sma = MyIndicator(self.data)
        self.bbands = bt.indicators.BBands(self.data, period=10, devfactor=1.5)
        self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(self.data, self.bbands.top))
        self.signal_add(bt.SIGNAL_LONGEXIT, bt.ind.CrossOver(self.sma, self.data))

class MACrossOver(bt.SignalStrategy):
    params = (('ma', bt.ind.MovAv.SMA), ('p1', 30), ('p2', 50),)

    def __init__(self):
        ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        self.signal_add(bt.SIGNAL_LONGSHORT, bt.ind.CrossOver(ma1, ma2))


#data = bt.feeds.BacktraderCSVData(dataname="/Users/thanhuwe8/Quantitative Finance Project/WQU-AlphaDesignI/data/2006-day-001.txt")
data = bt.feeds.BacktraderCSVData(dataname="C:/Code/WQU-AlphaDesignI/data/2006-day-001.txt")
cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(St)
#cerebro.addstrategy(St)

cerebro.run()
cerebro.plot(style="candlestick", barup="green", bardown="red")
