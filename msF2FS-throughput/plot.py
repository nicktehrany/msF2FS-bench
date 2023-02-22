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

msf2fs_spf_data = dict()
msf2fs_srr_data = dict()
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
    x = np.arange(0, 9)
    width = 0.25

    msf2fs_spf_iops = [None] * 9
    msf2fs_spf_stddev = [None] * 9
    msf2fs_srr_iops = [None] * 9
    msf2fs_srr_stddev = [None] * 9
    f2fs_iops = [None] * 9
    f2fs_stddev = [None] * 9

    for key, item in msf2fs_spf_data.items():
        if 'single_file' in key:
            msf2fs_spf_iops[0] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[0] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_file' in key:
            msf2fs_spf_iops[1] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_file' in key:
            msf2fs_spf_iops[2] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[2] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'four_file' in key:
            msf2fs_spf_iops[3] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[3] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'five_file' in key:
            msf2fs_spf_iops[4] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[4] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'six_file' in key:
            msf2fs_spf_iops[5] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[5] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'seven_file' in key:
            msf2fs_spf_iops[6] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[6] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'eight_file' in key:
            msf2fs_spf_iops[7] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[7] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'nine_file' in key:
            msf2fs_spf_iops[8] = item['jobs'][0]['write']['iops']/1000
            msf2fs_spf_stddev[8] = item['jobs'][0]['write']['iops_stddev']/1000

    for key, item in msf2fs_srr_data.items():
        if 'single_file' in key:
            msf2fs_srr_iops[0] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[0] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_file' in key:
            msf2fs_srr_iops[1] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_file' in key:
            msf2fs_srr_iops[2] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[2] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'four_file' in key:
            msf2fs_srr_iops[3] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[3] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'five_file' in key:
            msf2fs_srr_iops[4] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[4] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'six_file' in key:
            msf2fs_srr_iops[5] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[5] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'seven_file' in key:
            msf2fs_srr_iops[6] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[6] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'eight_file' in key:
            msf2fs_srr_iops[7] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[7] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'nine_file' in key:
            msf2fs_srr_iops[8] = item['jobs'][0]['write']['iops']/1000
            msf2fs_srr_stddev[8] = item['jobs'][0]['write']['iops_stddev']/1000

    for key, item in f2fs_data.items():
        if 'single_file' in key:
            f2fs_iops[0] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[0] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'two_file' in key:
            f2fs_iops[1] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'three_file' in key:
            f2fs_iops[2] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[2] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'four_file' in key:
            f2fs_iops[3] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[3] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'five_file' in key:
            f2fs_iops[4] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[4] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'six_file' in key:
            f2fs_iops[5] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[5] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'seven_file' in key:
            f2fs_iops[6] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[6] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'eight_file' in key:
            f2fs_iops[7] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[7] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'nine_file' in key:
            f2fs_iops[8] = item['jobs'][0]['write']['iops']/1000
            f2fs_stddev[8] = item['jobs'][0]['write']['iops_stddev']/1000

    fig, ax = plt.subplots()

    rects3 = ax.bar(x - width, f2fs_iops, yerr=f2fs_stddev, capsize=3, width=width, hatch='/', label="F2FS")
    rects2 = ax.bar(x, msf2fs_srr_iops, yerr=msf2fs_srr_stddev, capsize=3, width=width, hatch='', label="msF2FS (SRR)")
    rects1 = ax.bar(x + width, msf2fs_spf_iops, yerr=msf2fs_spf_stddev,capsize=3, width=width, hatch='x', label="msF2FS (SPF)")

    # For whatever reason we have to force the hatch patterns
    for i in range(len(msf2fs_spf_iops)):
        rects1[i].set_edgecolor("black")
        rects1[i].set_hatch("xx")
    for i in range(len(msf2fs_srr_iops)):
        rects2[i].set_edgecolor("black")
        rects2[i].set_hatch("o")
    for i in range(len(f2fs_iops)):
        rects3[i].set_edgecolor("black")
        rects3[i].set_hatch("/")

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='best',ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(np.arange(1,10))
    ax.set_ylim(bottom=0,top=400)
    ax.set_ylabel('KIOPS')
    ax.set_xlabel('Concurrent Files')
    plt.savefig(f'figs/msf2fs-throughput.pdf', bbox_inches='tight')
    plt.savefig(f'figs/msf2fs-throughput.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    parse_fio_data(f'{file_path}/data-spf/', msf2fs_spf_data)
    parse_fio_data(f'{file_path}/data-srr/', msf2fs_srr_data)
    parse_fio_data(f'{file_path}/data-f2fs/', f2fs_data)

    plot_throughput()
