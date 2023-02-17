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

zns_old_iodepth = dict()
zns_old_jobs = dict()
zns_new_iodepth = dict()
zns_new_jobs = dict()
femu_def_conf_iodepth = dict()
femu_def_conf_jobs = dict()
femu_bench = dict()

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

def plot_iodepth():
    xticks = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
    queue_depths = np.arange(11)
    zns_old_iops = [None] * len(queue_depths)
    zns_old_iops_stddev = [None] * len(queue_depths)
    zns_new_iops = [None] * len(queue_depths)
    zns_new_iops_stddev = [None] * len(queue_depths)
    femu_def_conf_iops = [None] * len(queue_depths)
    femu_def_conf_iops_stddev = [None] * len(queue_depths)

    for key, item in zns_old_iodepth.items():
        zns_old_iops[int(math.log2(int(item['jobs'][0]['job options']['iodepth'])))] = item['jobs'][0]['write']['iops']/1000
        zns_old_iops_stddev[int(math.log2(int(item['jobs'][0]['job options']['iodepth'])))] = item['jobs'][0]['write']['iops_stddev']/1000

    for key, item in zns_new_iodepth.items():
        zns_new_iops[int(math.log2(int(item['jobs'][0]['job options']['iodepth'])))] = item['jobs'][0]['write']['iops']/1000
        zns_new_iops_stddev[int(math.log2(int(item['jobs'][0]['job options']['iodepth'])))] = item['jobs'][0]['write']['iops_stddev']/1000

    for key, item in femu_def_conf_iodepth.items():
        femu_def_conf_iops[int(math.log2(int(item['jobs'][0]['job options']['iodepth'])))] = item['jobs'][0]['write']['iops']/1000
        femu_def_conf_iops_stddev[int(math.log2(int(item['jobs'][0]['job options']['iodepth'])))] = item['jobs'][0]['write']['iops_stddev']/1000

    fig, ax = plt.subplots()

    ax.errorbar(queue_depths, zns_old_iops, yerr=zns_old_iops_stddev, markersize=4, capsize=3, marker='x', label='ZNS 1')
    ax.errorbar(queue_depths, zns_new_iops, yerr=zns_new_iops_stddev, markersize=4, capsize=3, marker='o', label='ZNS 2')
    ax.errorbar(queue_depths, femu_def_conf_iops, yerr=femu_def_conf_iops_stddev, markersize=4, capsize=3, marker=',', label='FEMU')

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='lower right', ncol=2)
    ax.xaxis.set_ticks(queue_depths)
    ax.xaxis.set_ticklabels(xticks)
    ax.set_ylim(bottom=0, top=550)
    ax.set_ylabel('Throughput (KIOPS)')
    ax.set_xlabel('Queue Depth')
    plt.savefig(f'figs/zns_iodepth.pdf', bbox_inches='tight')
    plt.savefig(f'figs/zns_iodepth.png', bbox_inches='tight')
    plt.clf()

def plot_jobs():
    jobs = np.arange(1,15,1)
    zns_old_iops = [None] * len(jobs)
    zns_old_iops_stddev = [None] * len(jobs)
    zns_new_iops = [None] * len(jobs)
    zns_new_iops_stddev = [None] * len(jobs)
    femu_def_conf_iops = [None] * len(jobs)
    femu_def_conf_iops_stddev = [None] * len(jobs)

    for key, item in zns_old_jobs.items():
        zns_old_iops[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
        zns_old_iops_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000

    for key, item in zns_new_jobs.items():
        zns_new_iops[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
        zns_new_iops_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000

    for key, item in femu_def_conf_jobs.items():
        femu_def_conf_iops[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
        femu_def_conf_iops_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000

    fig, ax = plt.subplots()

    ax.errorbar(jobs, zns_old_iops, yerr=zns_old_iops_stddev, markersize=4, capsize=3, marker='x', label='ZNS 1')
    ax.errorbar(jobs, zns_new_iops, yerr=zns_new_iops_stddev, markersize=4, capsize=3, marker='o', label='ZNS 2')
    ax.errorbar(jobs, femu_def_conf_iops, yerr=femu_def_conf_iops_stddev, markersize=4, capsize=3, marker=',', label='FEMU')

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='lower right', ncol=2)
    ax.xaxis.set_ticks(jobs)
    ax.xaxis.set_ticklabels(jobs)
    ax.set_ylim(bottom=0, top=550)
    ax.set_ylabel('Throughput (KIOPS)')
    ax.set_xlabel('Concurrent Jobs')
    plt.savefig(f'figs/zns_jobs.pdf', bbox_inches='tight')
    plt.savefig(f'figs/zns_jobs.png', bbox_inches='tight')
    plt.clf()

def plot_femu_bench():
    jobs = np.arange(1,15,1)
    femu_qd2 = [None] * len(jobs)
    femu_qd2_stddev = [None] * len(jobs)
    femu_qd4 = [None] * len(jobs)
    femu_qd4_stddev = [None] * len(jobs)
    femu_qd8 = [None] * len(jobs)
    femu_qd8_stddev = [None] * len(jobs)
    femu_qd32 = [None] * len(jobs)
    femu_qd32_stddev = [None] * len(jobs)
    femu_qd128 = [None] * len(jobs)
    femu_qd128_stddev = [None] * len(jobs)

    for key, item in femu_bench.items():
        if 'iodepth-2' in key:
            femu_qd2[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
            femu_qd2_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'iodepth-4' in key:
            femu_qd4[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
            femu_qd4_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'iodepth-8' in key:
            femu_qd8[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
            femu_qd8_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'iodepth-32' in key:
            femu_qd32[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
            femu_qd32_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000
        if 'iodepth-128' in key:
            femu_qd128[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops']/1000
            femu_qd128_stddev[int(item['jobs'][0]['job options']['numjobs']) - 1] = item['jobs'][0]['write']['iops_stddev']/1000

    fig, ax = plt.subplots()

    ax.errorbar(jobs, femu_qd2, yerr=femu_qd2_stddev, markersize=4, capsize=3, marker='x', label='QD2')
    ax.errorbar(jobs, femu_qd4, yerr=femu_qd4_stddev, markersize=4, capsize=3, marker='o', label='QD4')
    ax.errorbar(jobs, femu_qd8, yerr=femu_qd8_stddev, markersize=4, capsize=3, marker=',', label='QD8')
    ax.errorbar(jobs, femu_qd32, yerr=femu_qd32_stddev, markersize=4, capsize=3, marker='<', label='QD32')
    ax.errorbar(jobs, femu_qd128, yerr=femu_qd128_stddev, markersize=4, capsize=3, marker='v', label='QD128')

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='lower right', ncol=2)
    ax.xaxis.set_ticks(jobs)
    ax.xaxis.set_ticklabels(jobs)
    ax.set_ylim(bottom=0, top=650)
    ax.set_ylabel('Throughput (KIOPS)')
    ax.set_xlabel('Concurrent Jobs')
    plt.savefig(f'figs/femu-bench-jobs.pdf', bbox_inches='tight')
    plt.savefig(f'figs/femu-bench-jobs.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    zns_old_path = "zns-old"
    zns_new_path = "zns-new"
    femu_def_conf_path = "femu"
    femu_bench_path = "femu-bench"

    parse_fio_data(f'{file_path}/{zns_old_path}/iodepth/', zns_old_iodepth)
    parse_fio_data(f'{file_path}/{zns_old_path}/jobs/', zns_old_jobs)
    parse_fio_data(f'{file_path}/{zns_new_path}/iodepth/', zns_new_iodepth)
    parse_fio_data(f'{file_path}/{zns_new_path}/jobs/', zns_new_jobs)
    parse_fio_data(f'{file_path}/{femu_def_conf_path}/iodepth/', femu_def_conf_iodepth)
    parse_fio_data(f'{file_path}/{femu_def_conf_path}/jobs/', femu_def_conf_jobs)
    parse_fio_data(f'{file_path}/{femu_bench_path}/', femu_bench)

    plot_iodepth()
    plot_jobs()
    plot_femu_bench()
