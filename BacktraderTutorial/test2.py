from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
from datetime import datetime

import backtrader as bt
import backtrader.indicators as btind
import backtrader.feeds as btfeeds


class MyStrategy(bt.Strategy):
    params = dict(period=20,
                  period1=20,
                  period2=25,
                  period3=10,
                  period4=2,
                  perc1=3,
                  perc2=1,
                  valid=4,
                  smaperiod=15,
                  exectype='Market')
    # self.params = self.p

    def __init__(self):

        sma = btind.SimpleMovingAverage(period=self.p.smaperiod)
        sma1 = btind.SimpleMovingAverage(self.data, period=self.params.period1)
        sma2 = btind.SimpleMovingAverage(period=self.params.period2)

        myindicator = sma2-sma1 + self.datas[0].close

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

        self.buysell = btind.CrossOver(self.data.close, sma, plot=True)

        self.order = None

    def start(self):
        print("Trading Strategy Simulation starts")

    def stop(self):
        print("Trading Strategy Simulation ends")

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.date(0)
        print('%s, %s,' %(dt.isoformat(),txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            self.log('Order accepted/Submitted', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log['BUY EXPIRED']

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'Buy Executed, Price: %.2f, Cost: %.2f, Comm: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:
                self.log(
                    'Sell Executed, Price: %.2f, Cost: %.2f, Comm: %.2f'%
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

        self.order = None


    def next(self):
        if self.order:
            return

        if self.position:
            if self.buysell < 0:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                self.sell()

        elif self.buysell > 1:
            if self.p.valid:
                valid = self.data.datetime.date(0) + datetime.timedelta(days=self.p.value)
            else:
                value = None

            if self.p.execute == "Market":
                self.buy(exectype=bt.Order.Market)
                self.log('BUY CREATE, exectyoe Market, price %.2f' %self.data.close[0])


            elif self.p.execute == "Close":
                self.buy(exectype=bt.Order.Close)
                self.log('BUY CREATE, exectype Close, price %.2f'%
                         self.data.close[0])

            elif self.p.execute == "Limit":
                price = self.data.close*(1.0 - self.p.perc1/100.0)
                self.buy(exectype=bt.Order.Limit, price=price, valid=value)

                if self.p.valid:
                    txt = 'BUY CREATE, exectype Limit, price %.2f, value %s'
                    self.log(txt %(price, value.strftime('%Y-%m-%d')))
                else:
                    txt = 'BUY CREATE, exectype Limit, price %.2f, value %s'
                    self.log(txt % price)





def runstrat():
    args = parse_args()

    cerebro = bt.Cerebro()

    data = getdata(args)
    cerebro.adddata(data)

    cerebro.addstrategy(
        MyStrategy,
        exectype=args.exectype,
        perc1=args.perc1,
        perc2=args.perc2,
        valid=args.valid,
        smaperiod=args.smaperiod
    )

    cerebro.run()

    if args.plot:
        cerebro.plot(numfigs=args.numfigs, style=args.plotstyle)

def getdata(args):

    dataformat = dict(
        bt=btfeeds.BacktraderCSVData,
        visualchart=btfeeds.VChartCSVData,
        sierrachart=btfeeds.SierraChartCSVData,
        yahoo=btfeeds.YahooFinanceCSVData,
        yahoo_unreversed=btfeeds.YahooFinanceCSVData
    )

    dfkwargs = dict()
    if args.csvformat == 'yahoo_unreversed':
        dfkwargs['reverse'] = True

    if args.fromdate:
        fromdate = datetime.datetime.strptime(args.fromdate, '%Y-%m-%d')
        dfkwargs['fromdate'] = fromdate

    if args.todate:
        fromdate = datetime.datetime.strptime(args.todate, '%Y-%m-%d')
        dfkwargs['todate'] = todate

    dfkwargs['dataname'] = args.infile

    dfcls = dataformat[args.csvformat]

    return dfcls(**dfkwargs)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Showcase for Order Execution Types')

    parser.add_argument('--infile', '-i', required=False,
                        default="/Users/thanhuwe8/Quantitative Finance Project/WQU-AlphaDesignI/data/2006-day-001.txt",
                        help='File to be read in')

    parser.add_argument('--csvformat', '-c', required=False, default='bt',
                        choices=['bt', 'visualchart', 'sierrachart',
                                 'yahoo', 'yahoo_unreversed'],
                        help='CSV Format')

    parser.add_argument('--fromdate', '-f', required=False, default=None,
                        help='Starting date in YYYY-MM-DD format')

    parser.add_argument('--todate', '-t', required=False, default=None,
                        help='Ending date in YYYY-MM-DD format')

    parser.add_argument('--plot', '-p', action='store_false', required=False,
                        help='Plot the read data')

    parser.add_argument('--plotstyle', '-ps', required=False, default='bar',
                        choices=['bar', 'line', 'candle'],
                        help='Plot the read data')

    parser.add_argument('--numfigs', '-n', required=False, default=1,
                        help='Plot using n figures')

    parser.add_argument('--smaperiod', '-s', required=False, default=15,
                        help='Simple Moving Average Period')

    parser.add_argument('--exectype', '-e', required=False, default='Market',
                        help=('Execution Type: Market (default), Close, Limit,'
                              ' Stop, StopLimit'))

    parser.add_argument('--valid', '-v', required=False, default=0, type=int,
                        help='Validity for Limit sample: default 0 days')

    parser.add_argument('--perc1', '-p1', required=False, default=0.0,
                        type=float,
                        help=('%% distance from close price at order creation'
                              ' time for the limit/trigger price in Limit/Stop'
                              ' orders'))

    parser.add_argument('--perc2', '-p2', required=False, default=0.0,
                        type=float,
                        help=('%% distance from close price at order creation'
                              ' time for the limit price in StopLimit orders'))

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()


    #
    # def next(self):
    #     if self.mova.lines.sma[0] > self.data.lines.close[0]:
    #         print('Simple Moving Average is greater than the closing price')
    #     #xxx.lines could be shortened to xxx.l
    #      if self.data.close[0] > self.data.close[-1]:
    #          if self.data.close[-1] > self.data.close[-2]:
    #              print('It is bullish 3-day close')
    #
    #     if self.cmpval[0]:
    #         print('Previous close is higher than the moving average')
