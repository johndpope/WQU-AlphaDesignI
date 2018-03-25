from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt


class St(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data)


class MyBuySell(bt.observers.BuySell):
    plotlines = dict(
        buy=dict(marker='$\u21E7$', markersize=12.0),
        sell=dict(marker='$\u21E9$', markersize=12.0)
    )

class MyObs(bt.observers.DrawDown):
    lines = ('drawdown', 'maxdrawdown',)
    #plotlines = dict(maxdrawdown=dict(_plotskip='False',),
    #                 drawdown=dict())
    plotlines = dict(maxdrawdown=dict(_plotskip=False, _name='maxdrawdown',
                                      color='red'),
                     drawdown=dict(_name='drawdown', color='blue'))


class MyObs2(bt.observers.TimeReturn):
    lines = ('timereturn',)
    plotlines = dict(timereturn=dict(color='red'))

class MyObs3(bt.observers.Benchmark):
    lines = ('benchmark',)
    plotlines = dict()



class MACrossOver(bt.SignalStrategy):
    params = (('ma', bt.ind.MovAv.SMA), ('p1', 30), ('p2', 50),)

    def __init__(self):
        ma1, ma2 = self.p.ma(period=self.p.p1), self.p.ma(period=self.p.p2)
        self.signal_add(bt.SIGNAL_LONGSHORT, bt.ind.CrossOver(ma1, ma2))


data = bt.feeds.BacktraderCSVData(dataname="/Users/thanhuwe8/Quantitative Finance Project/WQU-AlphaDesignI/data/2006-day-001.txt")

cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(MACrossOver)

cerebro.addobserver(MyBuySell, barplot=True)
cerebro.addobserver(MyObs)
cerebro.addobserver(MyObs2)
cerebro.addobserver(MyObs3, data=data)


cerebro.run()

cerebro.plot()
