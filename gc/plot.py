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

msf2fs_iops_data = []
f2fs_iops_data = []

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

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    # TODO dummy msf2fs for now
    parse_fio_log(f'{file_path}/data-f2fs/overwrite_iops_log_iops.8.log', f2fs_iops_data)
    parse_fio_log(f'{file_path}/data-f2fs/overwrite_iops_log_iops.8.log', msf2fs_iops_data)
    # parse_fio_log(f'{file_path}/data-f2fs/', f2fs_iops_data)

    # throughput over time plot
    plot_iops()

    # tail latency plot
    # latency over time plot
