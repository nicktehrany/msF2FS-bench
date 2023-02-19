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

msf2fs_data = dict()
f2fs_data = dict()

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
    x = np.arange(0, 4)
    width = 0.1

    msf2fs_seq_iops = [None] * 4
    msf2fs_seq_stddev = [None] * 4
    msf2fs_rand_iops = [None] * 4
    msf2fs_rand_stddev = [None] * 4
    f2fs_seq_iops = [None] * 4
    f2fs_seq_stddev = [None] * 4
    f2fs_rand_iops = [None] * 4
    f2fs_rand_stddev = [None] * 4

    for key, item in msf2fs_data.items():
        if '-1' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    msf2fs_seq_iops[0] = job['read']['iops']/1000
                    msf2fs_seq_stddev[0] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    msf2fs_rand_iops[0] = job['read']['iops']/1000
                    msf2fs_rand_stddev[0] = job['read']['iops_stddev']/1000
        if '-10' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    msf2fs_seq_iops[1] = job['read']['iops']/1000
                    msf2fs_seq_stddev[1] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    msf2fs_rand_iops[1] = job['read']['iops']/1000
                    msf2fs_rand_stddev[1] = job['read']['iops_stddev']/1000
        if '-50' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    msf2fs_seq_iops[2] = job['read']['iops']/1000
                    msf2fs_seq_stddev[2] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    msf2fs_rand_iops[2] = job['read']['iops']/1000
                    msf2fs_rand_stddev[2] = job['read']['iops_stddev']/1000
        if '-100' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    msf2fs_seq_iops[3] = job['read']['iops']/1000
                    msf2fs_seq_stddev[3] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    msf2fs_rand_iops[3] = job['read']['iops']/1000
                    msf2fs_rand_stddev[3] = job['read']['iops_stddev']/1000

    for key, item in f2fs_data.items():
        if '-1' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    f2fs_seq_iops[0] = job['read']['iops']/1000
                    f2fs_seq_stddev[0] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    f2fs_rand_iops[0] = job['read']['iops']/1000
                    f2fs_rand_stddev[0] = job['read']['iops_stddev']/1000
        if '-10' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    f2fs_seq_iops[1] = job['read']['iops']/1000
                    f2fs_seq_stddev[1] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    f2fs_rand_iops[1] = job['read']['iops']/1000
                    f2fs_rand_stddev[1] = job['read']['iops_stddev']/1000
        if '-50' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    f2fs_seq_iops[2] = job['read']['iops']/1000
                    f2fs_seq_stddev[2] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    f2fs_rand_iops[2] = job['read']['iops']/1000
                    f2fs_rand_stddev[2] = job['read']['iops_stddev']/1000
        if '-100' in key:
            for job in item['jobs']:
                if 'seq' in job['jobname']:
                    f2fs_seq_iops[3] = job['read']['iops']/1000
                    f2fs_seq_stddev[3] = job['read']['iops_stddev']/1000
                if 'rand' in job['jobname']:
                    f2fs_rand_iops[3] = job['read']['iops']/1000
                    f2fs_rand_stddev[3] = job['read']['iops_stddev']/1000
    fig, ax = plt.subplots()

    rects1 = ax.bar(x - (2 * width), f2fs_seq_iops, yerr=f2fs_seq_stddev, capsize=3, width=width, hatch='x', label="F2FS seqread")
    rects2 = ax.bar(x - width, f2fs_rand_iops, yerr=f2fs_rand_stddev, capsize=3, width=width, hatch='/', label="F2FS randread")
    rects3 = ax.bar(x + width, msf2fs_seq_iops, yerr=msf2fs_seq_stddev, capsize=3, width=width, hatch='x', label="msF2FS seqread")
    rects4 = ax.bar(x + (2 * width), msf2fs_rand_iops, yerr=msf2fs_rand_iops, capsize=3, width=width, hatch='/', label="msF2FS randread")

    # For whatever reason we have to force the hatch patterns
    for i in range(len(f2fs_seq_iops)):
        rects1[i].set_edgecolor("black")
        rects1[i].set_hatch("xx")
    for i in range(len(f2fs_rand_iops)):
        rects2[i].set_edgecolor("black")
        rects2[i].set_hatch("/")
    for i in range(len(msf2fs_seq_iops)):
        rects3[i].set_edgecolor("black")
        rects3[i].set_hatch("o")
    for i in range(len(msf2fs_rand_iops)):
        rects4[i].set_edgecolor("black")
        rects4[i].set_hatch("\\")

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best',ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels([1,10,50,100])
    ax.set_ylim(bottom=0,top=600)
    ax.set_ylabel('KIOPS')
    ax.set_xlabel('Concurrent Files')
    plt.savefig(f'figs/msf2fs-read-throughput.pdf', bbox_inches='tight')
    plt.savefig(f'figs/msf2fs-read-throughput.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    parse_fio_data(f'{file_path}/data-spf/', msf2fs_data)
    parse_fio_data(f'{file_path}/data-f2fs/', f2fs_data)

    plot_throughput()
    # TODO plot tail latency for one of them probably 100 files as line (equal distance and points for 95, 99, 99.9, 99.99)
