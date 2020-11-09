#!/usr/bin/python
from __future__ import division
import sys
import os
import time
import datetime
import re

import pandas as pd

from bokeh.plotting import figure, output_file, show
from bokeh.models import CustomJS, Dropdown, ColumnDataSource, CheckboxGroup, Select, Button, Slider
from bokeh.layouts import column, row, widgetbox
from bokeh.models import HoverTool


bcache_stats = {}

start_time = 0

block_size = 512

def print_bcache_stats(bcache_stats, bdev):
    fv = bcache_stats[bdev]
    x = []
    y_riops = []
    y_wiops = []
    for k in fv.keys():
        x.append(k)
        y_riops.append(fv[k]["riops"])
        y_wiops.append(fv[k]["wiops"])
    print x
    print y_riops
    print y_wiops
    output_file(bdev)
    p = figure(plot_width=800, plot_height=600, active_scroll = 'wheel_zoom', x_axis_label='time', y_axis_label='iops')
    p.circle(x = x, y = y_riops, legend_label="bcache read iops", size=5, color='red')
    p.circle(x = x, y = y_wiops, legend_label="bcache write iops", size=5, color='blue')
    show(p)

def main():
  filepath = sys.argv[1]
  if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()
  with open(filepath) as fp:
       #import pdb
       #pdb.set_trace()
       for line in fp:
           global start_time
           words = line.strip().split()
           time = words[2].strip().split(".")
           time = time[0]
           if start_time == 0:
              start_time = int(time)
           sec = int(time) - start_time
           read = True
           if words[5] != "R":
              read = False
           bdev = words[4]
           if not bcache_stats.has_key(bdev):
              bcache_stats[bdev] = {}
           if not bcache_stats[bdev].has_key(sec):
              bcache_stats[bdev][sec] = {"iops":0, "riops":0, "wiops":0, "wbps":0, "rbps":0}

           bcache_stats[bdev][sec]["iops"] += 1
           if read:
              bcache_stats[bdev][sec]["riops"] += 1
              bcache_stats[bdev][sec]["rbps"] += int(words[8]) * block_size
           else:
              bcache_stats[bdev][sec]["wiops"] += 1
              bcache_stats[bdev][sec]["wbps"] += int(words[8]) * block_size
       for bdev in bcache_stats.keys():
	   print_bcache_stats(bcache_stats, bdev) 
 



if __name__ == '__main__':
   main()
