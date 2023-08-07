from plotter import plotter

fig = plotter('C:/Users/Public/B12TLOG/log_20230807113019.csv')
fig.plot(['voltage1', 'voltage2'], 10*60)