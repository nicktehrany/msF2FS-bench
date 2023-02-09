
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
    xticks = [1, 2, 4, 8, 16, 32, 64, 128]
    queue_depths = np.arange(8)
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
    ax.errorbar(queue_depths, femu_def_conf_iops, yerr=femu_def_conf_iops_stddev, markersize=4, capsize=3, marker=',', label='FEMU-Default')
    # ax.errorbar(queue_depths, zns_fourzd, yerr=zns_fourzd_stdev, markersize=4, capsize=3, marker='.', label='ZNS 4 Zone')
    # ax.errorbar(queue_depths, zns_fivezd, yerr=zns_fivezd_stdev, markersize=4, capsize=3, marker='v', label='ZNS 5 Zones')
    # ax.errorbar(queue_depths, zns_sixzd, yerr=zns_sixzd_stdev, markersize=4, capsize=3, marker='<', label='ZNS 6 Zones')
    # ax.errorbar(queue_depths, zns_sevenzd, yerr=zns_sevenzd_stdev, markersize=4, capsize=3, marker='>', label='ZNS 7 Zone')
    # ax.errorbar(queue_depths, zns_eightzd, yerr=zns_eightzd_stdev, markersize=4, capsize=3, marker=1, label='ZNS 8 Zones')
    # ax.errorbar(queue_depths, zns_ninezd, yerr=zns_ninezd_stdev, markersize=4, capsize=3, marker=2, label='ZNS 9 Zones')
    # ax.errorbar(queue_depths, zns_tenzd, yerr=zns_tenzd_stdev, markersize=4, capsize=3, marker=3, label='ZNS 10 Zone')
    # ax.errorbar(queue_depths, zns_elevenzd, yerr=zns_elevenzd_stdev, markersize=4, capsize=3, marker=4, label='ZNS 11 Zones')
    # ax.errorbar(queue_depths, zns_twelvezd, yerr=zns_twelvezd_stdev, markersize=4, capsize=3, marker=5, label='ZNS 12 Zones')
    # ax.errorbar(queue_depths, zns_thirteenzd, yerr=zns_thirteenzd_stdev, markersize=4, capsize=3, marker=6, label='ZNS 13 Zone')
    # ax.errorbar(queue_depths, zns_fourteenzd, yerr=zns_fourteenzd_stdev, markersize=4, capsize=3, marker=7, label='ZNS 14 Zones')

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='lower right', ncol=2)
    ax.xaxis.set_ticks(queue_depths)
    ax.xaxis.set_ticklabels(xticks)
    ax.set_ylim(bottom=0)
    ax.set_ylabel('KIOPS')
    ax.set_xlabel('Queue Depth')
    plt.savefig(f'figs/zns_iodepth.pdf', bbox_inches='tight')
    plt.savefig(f'figs/zns_iodepth.png', bbox_inches='tight')
    plt.clf()

def plot_jobs():
    jobs = np.arange(8)
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
    ax.errorbar(jobs, femu_def_conf_iops, yerr=femu_def_conf_iops_stddev, markersize=4, capsize=3, marker=',', label='FEMU-Default')
    # ax.errorbar(queue_depths, zns_fourzd, yerr=zns_fourzd_stdev, markersize=4, capsize=3, marker='.', label='ZNS 4 Zone')
    # ax.errorbar(queue_depths, zns_fivezd, yerr=zns_fivezd_stdev, markersize=4, capsize=3, marker='v', label='ZNS 5 Zones')
    # ax.errorbar(queue_depths, zns_sixzd, yerr=zns_sixzd_stdev, markersize=4, capsize=3, marker='<', label='ZNS 6 Zones')
    # ax.errorbar(queue_depths, zns_sevenzd, yerr=zns_sevenzd_stdev, markersize=4, capsize=3, marker='>', label='ZNS 7 Zone')
    # ax.errorbar(queue_depths, zns_eightzd, yerr=zns_eightzd_stdev, markersize=4, capsize=3, marker=1, label='ZNS 8 Zones')
    # ax.errorbar(queue_depths, zns_ninezd, yerr=zns_ninezd_stdev, markersize=4, capsize=3, marker=2, label='ZNS 9 Zones')
    # ax.errorbar(queue_depths, zns_tenzd, yerr=zns_tenzd_stdev, markersize=4, capsize=3, marker=3, label='ZNS 10 Zone')
    # ax.errorbar(queue_depths, zns_elevenzd, yerr=zns_elevenzd_stdev, markersize=4, capsize=3, marker=4, label='ZNS 11 Zones')
    # ax.errorbar(queue_depths, zns_twelvezd, yerr=zns_twelvezd_stdev, markersize=4, capsize=3, marker=5, label='ZNS 12 Zones')
    # ax.errorbar(queue_depths, zns_thirteenzd, yerr=zns_thirteenzd_stdev, markersize=4, capsize=3, marker=6, label='ZNS 13 Zone')
    # ax.errorbar(queue_depths, zns_fourteenzd, yerr=zns_fourteenzd_stdev, markersize=4, capsize=3, marker=7, label='ZNS 14 Zones')

    fig.tight_layout()
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.set_axisbelow(True)
    ax.legend(loc='lower right', ncol=2)
    ax.xaxis.set_ticks(jobs)
    ax.xaxis.set_ticklabels(jobs)
    ax.set_ylim(bottom=0)
    ax.set_ylabel('KIOPS')
    ax.set_xlabel('Concurrent Jobs')
    plt.savefig(f'figs/zns_jobs.pdf', bbox_inches='tight')
    plt.savefig(f'figs/zns_jobs.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    zns_old_path = "zns-old"
    zns_new_path = "zns-new"
    femu_def_conf_path = "femu-def-conf"

    parse_fio_data(f'{file_path}/{zns_old_path}/iodepth/', zns_old_iodepth)
    parse_fio_data(f'{file_path}/{zns_old_path}/jobs/', zns_old_jobs)
    parse_fio_data(f'{file_path}/{zns_new_path}/iodepth/', zns_new_iodepth)
    parse_fio_data(f'{file_path}/{zns_new_path}/jobs/', zns_new_jobs)
    parse_fio_data(f'{file_path}/{femu_def_conf_path}/iodepth/', femu_def_conf_iodepth)
    parse_fio_data(f'{file_path}/{femu_def_conf_path}/jobs/', femu_def_conf_jobs)

    plot_iodepth()
    plot_jobs()
