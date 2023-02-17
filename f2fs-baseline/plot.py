#!/usr/bin/env python3

import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.patches as mpatches
import os
import glob
import json

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize

data = dict()

def parse_fio_data(data_path, data):
    if not os.path.exists(f'{data_path}') or \
            os.listdir(f'{data_path}') == []: 
        print(f'No data in {data_path}')
        return 0 

    for file in glob.glob(f'{data_path}/*'): 
        with open(file, 'r') as f:
            for index, line in enumerate(f, 1):
                # Removing all fio logs in json file by finding first {
                if line.split()[0] == '{':
                    rows = f.readlines()
                    with open(os.path.join(os.getcwd(), 'temp.json'), 'w+') as temp:
                        temp.write(line)
                        temp.writelines(rows)
                    break
        with open(os.path.join(os.getcwd(), 'temp.json'), 'r') as temp:
            data[file] = dict()
            data[file] = json.load(temp)
            os.remove(os.path.join(os.getcwd(), 'temp.json'))

    return 1

def plot_throughput():
    x = np.arange(0, 5)
    width = 0.2

    single_stream_iops = [None] * 5
    single_stream_stddev = [None] * 5
    two_stream_iops = [None] * 5
    two_stream_stddev = [None] * 5
    three_stream_iops = [None] * 5
    three_stream_stddev = [None] * 5

    for key, item in data.items():
        if 'single_stream-1' in key:
            single_stream_iops[0] = item['jobs'][0]['write']['iops']/1000
            single_stream_stddev[0] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'single_stream-2' in key:
            single_stream_iops[1] = item['jobs'][0]['write']['iops']/1000
            single_stream_stddev[1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'single_stream-3' in key:
            single_stream_iops[2] = item['jobs'][0]['write']['iops']/1000
            single_stream_stddev[2] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'single_stream-4' in key:
            single_stream_iops[3] = item['jobs'][0]['write']['iops']/1000
            single_stream_stddev[3] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'single_stream-5' in key:
            single_stream_iops[4] = item['jobs'][0]['write']['iops']/1000
            single_stream_stddev[4] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_stream-1' in key:
            two_stream_iops[0] = item['jobs'][0]['write']['iops']/1000
            two_stream_stddev[0] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_stream-2' in key:
            two_stream_iops[1] = item['jobs'][0]['write']['iops']/1000
            two_stream_stddev[1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_stream-3' in key:
            two_stream_iops[2] = item['jobs'][0]['write']['iops']/1000
            two_stream_stddev[2] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_stream-4' in key:
            two_stream_iops[3] = item['jobs'][0]['write']['iops']/1000
            two_stream_stddev[3] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_stream-5' in key:
            two_stream_iops[4] = item['jobs'][0]['write']['iops']/1000
            two_stream_stddev[4] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_stream-1' in key:
            three_stream_iops[0] = item['jobs'][0]['write']['iops']/1000
            three_stream_stddev[0] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_stream-2' in key:
            three_stream_iops[1] = item['jobs'][0]['write']['iops']/1000
            three_stream_stddev[1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_stream-3' in key:
            three_stream_iops[2] = item['jobs'][0]['write']['iops']/1000
            three_stream_stddev[2] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_stream-4' in key:
            three_stream_iops[3] = item['jobs'][0]['write']['iops']/1000
            three_stream_stddev[3] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_stream-5' in key:
            three_stream_iops[4] = item['jobs'][0]['write']['iops']/1000
            three_stream_stddev[4] = item['jobs'][0]['write']['iops_stddev']/1000

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width, single_stream_iops, yerr=single_stream_stddev, capsize=3, width=width, hatch='x', label="1 Concurrent Log")
    rects2 = ax.bar(x, two_stream_iops, yerr=two_stream_stddev, capsize=3, width=width, hatch='', label="2 Concurrent Logs")
    rects3 = ax.bar(x + width, three_stream_iops, yerr=three_stream_stddev, capsize=3, width=width, hatch='/', label="3 Concurrent Logs")

    # For whatever reason we have to force the hatch patterns
    for i in range(len(single_stream_iops)):
        rects1[i].set_edgecolor("black")
        rects1[i].set_hatch("xx")
    for i in range(len(two_stream_iops)):
        rects2[i].set_edgecolor("black")
        rects2[i].set_hatch("o")
    for i in range(len(three_stream_iops)):
        rects3[i].set_edgecolor("black")
        rects3[i].set_hatch("/")

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best',ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(np.arange(1,6))
    ax.set_ylim(bottom=0,top=350)
    ax.set_ylabel('KIOPS')
    ax.set_xlabel('Concurrent Files per Log')
    plt.savefig(f'figs/f2fs-baseline.pdf', bbox_inches='tight')
    plt.savefig(f'figs/f2fs-baseline.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    parse_fio_data(f'{file_path}/data/', data)

    plot_throughput()
