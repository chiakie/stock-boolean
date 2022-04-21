import backtrader as bt
import yfinance as yf
import sys

# Create a Stratey
class TestStrategy000(bt.Strategy):
  def __init__(self):
    self.dataclose = self.datas[0].close
    self.EMA20 = bt.indicators.EMA(self.datas[0], period=20)
    self.BBand = bt.indicators.BollingerBandsPct(self.datas[0]).pctb
  def next(self):
    self.log("{} Close {}".format(len(self), self.dataclose[0]))
    self.log("{} BBand {}".format(len(self), self.BBand[0]))
    if self.BBand[0] < .05:
        self.buy()
    elif self.BBand[0] > .95:
        self.close() # sell()
  def log(self, txt):
    dt = self.datas[0].datetime.date(0)
    print("{} {}".format(dt.isoformat(), txt))
# Create a cerebro entity
cerebro = bt.Cerebro()
# Add a strategy
cerebro.addstrategy(TestStrategy000)

#stockid = sys.argv[1] + ".TW"
n = len(sys.argv)
if n > 1 and sys.argv[1] == "-two":
    stockid = input() + ".TWO"
else:
    stockid = input() + ".TW"

# Add the Data Feed to Cerebro
cerebro.adddata(bt.feeds.PandasData(dataname=yf.download(stockid, start="2021-03-01")))
# Set our desired cash start
cerebro.broker.setcash(1000000.0)
# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=1000)
# Set the commission0.001425
cerebro.broker.setcommission(commission=0.001425)
# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
# Run over everything
results = cerebro.run()
# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
### pip install matplotlib==3.2.2
cerebro.plot(style='candlestick', barup='red', bardown='green')
