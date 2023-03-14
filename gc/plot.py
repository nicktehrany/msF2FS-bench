#!/usr/bin/env python3

import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker
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

msf2fs_iops_data = []
f2fs_iops_data = []

f2fs_global_data = dict()
msf2fs_global_data = dict()

msf2fs_lat_data = []
f2fs_lat_data = []

def parse_fio_log(data_path, data):

    with open(data_path, 'r') as f:
        for index, line in enumerate(f, 1):
            newline = line.split()
            if len(newline) < 1:
                break
            else:
                data.append(int(newline[1][:-1]))

    return 1

def parse_fio_data(data_path, data):
    if not os.path.exists(f'{data_path}') or \
            os.listdir(f'{data_path}') == []: 
        print(f'No data in {data_path}')
        return 0 

    for file in glob.glob(f'{data_path}/*.json'): 
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

def plot_iops():
    f2fs_iops = [] 
    f2fs_iops_x = []
    msf2fs_iops = [] 
    msf2fs_iops_x = []

    total_bw = 0
    bw_iter_tracker = 0

    for iter in range(len(f2fs_iops_data)):
        total_bw += f2fs_iops_data[iter]*4096
        f2fs_iops.append(f2fs_iops_data[iter]/1000)
        bw_iter_tracker += total_bw/1024/1024/1024
        f2fs_iops_x.append(bw_iter_tracker)
        total_bw = 0

    total_bw = 0
    bw_iter_tracker = 0

    for iter in range(len(msf2fs_iops_data)):
        total_bw += msf2fs_iops_data[iter]*4096
        msf2fs_iops.append(msf2fs_iops_data[iter]/1000)
        bw_iter_tracker += total_bw/1024/1024/1024
        msf2fs_iops_x.append(bw_iter_tracker)
        total_bw = 0

    # With 3 down-sampling
    f2fs_iops_np = np.asarray(f2fs_iops)
    f2fs_iops_fmt = np.nanmean(np.pad(f2fs_iops_np.astype(float), (0, 3 - f2fs_iops_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)
    f2fs_x_np = np.asarray(f2fs_iops_x)
    f2fs_x_fmt = np.nanmean(np.pad(f2fs_x_np.astype(float), (0, 3 - f2fs_x_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)
    msf2fs_iops_np = np.asarray(msf2fs_iops)
    msf2fs_iops_fmt = np.nanmean(np.pad(msf2fs_iops_np.astype(float), (0, 3 - msf2fs_iops_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)
    msf2fs_x_np = np.asarray(msf2fs_iops_x)
    msf2fs_x_fmt = np.nanmean(np.pad(msf2fs_x_np.astype(float), (0, 3 - msf2fs_x_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)

    print(f"F2FS Avg. KIOPS: {np.mean(f2fs_iops_np)}")
    print(f"msF2FS  Avg. KIOPS: {np.mean(msf2fs_iops_np)}")

    fig, ax = plt.subplots()
    
    # With downsampling
    ax.errorbar(f2fs_x_fmt, f2fs_iops_fmt, label="F2FS", fmt="-", linewidth=1)
    ax.errorbar(msf2fs_x_fmt, msf2fs_iops_fmt, label="msF2FS", fmt="-", linewidth=1)

    # Without down-sampling
    # ax.errorbar(f2fs_iops_x, f2fs_iops, label="F2FS", fmt="-", linewidth=0.5)
    # ax.errorbar(msf2fs_iops_x, msf2fs_iops, label="msF2FS", fmt="-", linewidth=0.5)
    
    fig.tight_layout()
    plt.rcParams['figure.figsize'] = [7, 5]
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='upper right')
    ax.set_xlabel("Data Written (GiB)")
    ax.set_ylabel("KIOPS")
    ax.set_ylim(0, 200)
    ax.set_xlim(0, 500)
    plt.savefig(f'figs/gc-throughput.pdf', bbox_inches='tight')
    plt.savefig(f'figs/gc-throughput.png', bbox_inches='tight')
    plt.clf()

def plot_tail_latency():
    
    f2fs_lats = []
    msf2fs_lats = []

    for key, item in f2fs_global_data.items():
        # f2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['95.000000'])/1000)
        f2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.000000'])/1000)
        f2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.900000'])/1000)
        f2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.990000'])/1000)
        f2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.999000'])/1000)
        f2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['100.000000'])/1000)

    for key, item in msf2fs_global_data.items():
        # msf2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['95.000000'])/1000)
        msf2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.000000'])/1000)
        msf2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.900000'])/1000)
        msf2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.990000'])/1000)
        msf2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['99.999000'])/1000)
        msf2fs_lats.append(int(item['jobs'][1]['write']['clat_ns']['percentile']['100.000000'])/1000)

    fig, ax = plt.subplots()
    
    ax.errorbar([1,2,3,4,5], f2fs_lats, label="F2FS", fmt="-", linewidth=1)
    ax.errorbar([1,2,3,4,5], msf2fs_lats, label="msF2FS", fmt="-", linewidth=1)

    fig.tight_layout()
    plt.rcParams['figure.figsize'] = [7, 5]
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    plt.yscale("log")
    ax.xaxis.set_ticks([1,2,3,4,5])
    ax.xaxis.set_ticklabels(["P99", "P99.9", "P99.99", "P99.999", "P100"])
    ax.legend(loc='best')
    ax.set_xlabel("Percentile")
    ax.set_ylabel("Latency (usec)")
    # ax.set_ylim(1, 100000)
    plt.savefig(f'figs/gc-tail_lat.pdf', bbox_inches='tight')
    plt.savefig(f'figs/gc-tail_lat.png', bbox_inches='tight')
    plt.clf()

def plot_latency():
    f2fs_lat = [] 
    f2fs_lat_x = []
    msf2fs_lat = [] 
    msf2fs_lat_x = []

    total_bw = 0
    bw_iter_tracker = 0

    min = 0
    if len(f2fs_lat_data) > len(f2fs_iops_data):
        min = len(f2fs_iops_data) - 1
    else:
        min = len(f2fs_lat_data) - 1
    
    for iter in range(min):
        total_bw += f2fs_iops_data[iter]*4096
        f2fs_lat.append(f2fs_lat_data[iter]/1000)
        bw_iter_tracker += total_bw/1024/1024/1024
        f2fs_lat_x.append(bw_iter_tracker)
        total_bw = 0

    total_bw = 0
    bw_iter_tracker = 0

    min = 0
    if len(msf2fs_lat_data) > len(msf2fs_iops_data):
        min = len(msf2fs_iops_data) - 1
    else:
        min = len(msf2fs_lat_data) - 1

    for iter in range(min):
        total_bw += msf2fs_iops_data[iter]*4096
        msf2fs_lat.append(msf2fs_lat_data[iter]/1000)
        bw_iter_tracker += total_bw/1024/1024/1024
        msf2fs_lat_x.append(bw_iter_tracker)
        total_bw = 0

    # With 3 down-sampling
    f2fs_lat_np = np.asarray(f2fs_lat)
    f2fs_lat_fmt = np.nanmean(np.pad(f2fs_lat_np.astype(float), (0, 3 - f2fs_lat_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)
    f2fs_x_np = np.asarray(f2fs_lat_x)
    f2fs_x_fmt = np.nanmean(np.pad(f2fs_x_np.astype(float), (0, 3 - f2fs_x_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)
    msf2fs_lat_np = np.asarray(msf2fs_lat)
    msf2fs_lat_fmt = np.nanmean(np.pad(msf2fs_lat_np.astype(float), (0, 3 - msf2fs_lat_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)
    msf2fs_x_np = np.asarray(msf2fs_lat_x)
    msf2fs_x_fmt = np.nanmean(np.pad(msf2fs_x_np.astype(float), (0, 3 - msf2fs_x_np.size%3), mode='constant', constant_values=np.NaN).reshape(-1, 3), axis=1)

    print(f"F2FS Avg. lat: {np.mean(f2fs_lat_np)}")
    print(f"msF2FS  Avg. lat: {np.mean(msf2fs_lat_np)}")

    fig, ax = plt.subplots()
    
    # With downsampling
    # ax.errorbar(f2fs_x_fmt, f2fs_lat_fmt, label="F2FS", fmt="-", linewidth=1)
    # ax.errorbar(msf2fs_x_fmt, msf2fs_lat_fmt, label="msF2FS", fmt="-", linewidth=1)

    # Without down-sampling
    ax.errorbar(f2fs_lat_x, f2fs_lat, label="F2FS", fmt="-", linewidth=0.5)
    ax.errorbar(msf2fs_lat_x, msf2fs_lat, label="msF2FS", fmt="-", linewidth=0.5)
    
    fig.tight_layout()
    plt.rcParams['figure.figsize'] = [7, 5]
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='upper right')
    ax.set_xlabel("Data Written (GiB)")
    ax.set_ylabel("Average Latency (usec)")
    ax.set_ylim(0, 15)
    ax.set_xlim(0, 500)
    plt.savefig(f'figs/gc-latency.pdf', bbox_inches='tight')
    plt.savefig(f'figs/gc-latency.png', bbox_inches='tight')
    plt.clf()

def plot_reverse_cdf():
    rcdf_f2fs = []
    rcdf_msf2fs = []

    sorted_f2fs_data = np.sort(f2fs_lat_data)
    x_f2fs = [val / 1000 for val in sorted_f2fs_data]

    for item in sorted_f2fs_data:
        rcdf_f2fs.append(sum(x > item for x in f2fs_lat_data)/len(sorted_f2fs_data))

    sorted_msf2fs_data = np.sort(msf2fs_lat_data)
    x_msf2fs = [val / 1000 for val in sorted_msf2fs_data]

    for item in sorted_msf2fs_data:
        rcdf_msf2fs.append(sum(x > item for x in msf2fs_lat_data)/len(sorted_msf2fs_data))
    fig, ax = plt.subplots()
    
    ax.errorbar(x_f2fs, rcdf_f2fs, label="F2FS", fmt="-", linewidth=1)
    ax.errorbar(x_msf2fs, rcdf_msf2fs, label="msF2FS", fmt="-", linewidth=1)

    print(x_f2fs[-1])
    print(x_msf2fs[-1])
    
    fig.tight_layout()
    plt.rcParams['figure.figsize'] = [7, 5]
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    # plt.yscale("log")
    plt.xscale("log")
    plt.yscale('symlog', linthresh=1e-4)
    ax.set_yticks([1, 0.1, 0.01, 0.001, 0.0001 , 0])
    ax.set_yticklabels([1, 0.1, 0.01, 0.001, 0.0001, 0])
    ax.set_ylim(-0.00001, 1.3)
    ax.set_xticks([10, 100])
    ax.set_xticklabels([10, 100])
    # ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(y),0)))).format(y)))
    # ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x,pos: ('{{:.{:1d}f}}'.format(int(np.maximum(-np.log10(x),0)))).format(x)))
    # ax.set_ylim(0.000001, 1)
    # ax.set_xlim(0.000001)
    ax.legend(loc='upper right')
    ax.set_ylabel("Fraction of Writes")
    ax.set_xlabel("Average Latency (usec)")
    plt.savefig(f'figs/gc-latency-rcdf.pdf', bbox_inches='tight')
    plt.savefig(f'figs/gc-latency-rcdf.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    parse_fio_log(f'{file_path}/data-f2fs/overwrite_iops_log_iops.8.log', f2fs_iops_data)
    parse_fio_log(f'{file_path}/data-spf/overwrite_iops_log_iops.8.log', msf2fs_iops_data)

    # throughput over time plot
    plot_iops()

    parse_fio_data(f'{file_path}/data-f2fs/', f2fs_global_data)
    parse_fio_data(f'{file_path}/data-spf/', msf2fs_global_data)

    # tail latency plot
    plot_tail_latency()

    parse_fio_log(f'{file_path}/data-f2fs/overwrite_lat_log_clat.8.log', f2fs_lat_data)
    parse_fio_log(f'{file_path}/data-spf/overwrite_lat_log_clat.8.log', msf2fs_lat_data)

    # latency over time plot
    plot_latency()

    # plotting the average latency as a reverse cumulative distribution function
    plot_reverse_cdf()
