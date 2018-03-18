

class MyStrategy(bt.Strategy):
    params = dict(period=20)
    def __init__(self):
        self.movav = btind.SimpleMovingAverage(self.data, period=self.p.period)
    def next(self):
        if self.movav.lines.sma[0] > self.data.lines.close[0]:
            print('Simple moving average is greater than the closing price')
    def next(self):
        