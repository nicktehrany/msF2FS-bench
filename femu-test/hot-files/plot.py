#!/usr/bin/env python3

import matplotlib.pyplot as plt
import math
import numpy as np
import matplotlib.patches as mpatches
import os
import glob
import json
import sys
import getopt

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize

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

def plot_throughput(nr_streams, spf_data, f2fs_data):
    x = np.arange(0, nr_streams)

    iops = [None] * nr_streams
    iops_stddev = [None] * nr_streams

    for key, item in spf_data.items():
        if 'single_file' in key:
            iops[0] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[0] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_file' in key:
            iops[1] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_file' in key:
            iops[2] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[2] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'four_file' in key:
            iops[3] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[3] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'five_file' in key:
            iops[4] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[4] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'six_file' in key:
            iops[5] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[5] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'seven_file' in key:
            iops[6] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[6] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'eight_file' in key:
            iops[7] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[7] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'nine_file' in key:
            iops[8] = item['jobs'][0]['write']['iops']/1000
            iops_stddev[8] = item['jobs'][0]['write']['iops_stddev']/1000

    fig, ax = plt.subplots()

    rects1 = ax.bar(x, iops, yerr=iops_stddev, capsize=3, label="SPF")

    ax.bar_label(rects1, padding=3, fmt="%.1f")

    # Plotting horizontal lines for max throughput on ZNS
    # plt.axhline(y = 257364.462305/1000, color = 'r', linestyle = ':', label = "ZNS 1 Zone")
    # plt.axhline(y = 459717.450472/1000, color = 'gray', linestyle = 'dashed', label = "ZNS 2 Zones")
    # plt.axhline(y = 378353.052926/1000, color = 'green', linestyle = 'dashdot', label = "ZNS 3 Zones")

    fig.tight_layout()
    # ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='upper right')
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(np.arange(1,nr_streams + 1))
    ax.set_ylim(bottom=0)
    ax.set_ylabel('KIOPS')
    ax.set_xlabel('Streams')
    plt.savefig(f'figs/msf2fs-hot-streams.pdf', bbox_inches='tight')
    plt.savefig(f'figs/msf2fs-hot-streams.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    """
    Plots the throughput of msF2FS with varying policies and active streams.
    Requires the paths for the data containing the logs for all policies.
    
    Arguments:
        -n: relative path to SPF data
        -z: relative path to SRR data
    """

    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])
    
    spf_path = None
    srr_path = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'n:z:', ['n=', 'z='])
    except getopt.GetoptError:
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-n':
            spf_path = arg
        if opt == '-z':
            srr_path = arg

    if spf_path == None or srr_path == None:
        print(f"Error, missing arguments. < -n spf_data path > < -z srr_data path >")

    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    spf_data = dict()
    srr_data = dict()

    parse_fio_data(f'{file_path}/{spf_path}/', spf_data)
    parse_fio_data(f'{file_path}/{srr_path}/', srr_data)

    # plot_throughput(3)
    # plot_throughput(6)
    plot_throughput(9, spf_data, srr_data)
