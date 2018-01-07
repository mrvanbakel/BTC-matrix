#!/usr/bin/python

import json
import requests
import time
from rgbmatrix import Adafruit_RGBmatrix


# Rows and chain length are both required parameters:
matrix = Adafruit_RGBmatrix(32, 1)

# Variabelen voor scherm en dus maximale aantal datapunten
matrixwidth = 32
matrixheight = 32

def main(): 
   req = requests.get("https://blockchain.info/charts/market-price?timespan="+str(matrixwidth)+"days&format=json")
   btc = json.loads(req.text)

   btcvalue = [btc['values'][i]['y'] for i in range(0, matrixwidth)]

   limmax = max(btcvalue)
   limmin =  min(btcvalue)
   scale = int(round((limmax - limmin) / matrixheight))

   btcgraph = [int(round((btcvalue[i]-limmin)/scale)) for i in range(0, matrixwidth)]

   for x in range(0,matrixwidth):
         if (x==0) or (btcgraph[x] == btcgraph[x-1]):
            matrix.SetPixel(x,(matrixheight-btcgraph[x]-1),0,255,0)
         elif btcgraph[x] < btcgraph[x-1]:
            [matrix.SetPixel(x,(matrixheight-y-1),255,0,0) for y in range(btcgraph[x], btcgraph[x-1])]
         else:
            [matrix.SetPixel(x,(matrixheight-y-1),0,255,0) for y in range(btcgraph[x-1], btcgraph[x])]
         time.sleep(.05)


try:
   while True:
      main()
      time.sleep(900)
      matrix.Clear()
except KeyboardInterrupt:
   time.sleep(1)
   matrix.Clear()
