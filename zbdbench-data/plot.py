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

def plot_throughput(f2fs_iops, msf2fs_spf_iops, msf2fs_spf_e_iops, msf2fs_amfs_iops, zenfs_iops, x_labs, name, max, lab):
    x = np.arange(0, len(f2fs_iops))

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - 0.2, f2fs_iops, width=0.1, capsize=3, label="F2FS") 
    rects2 = ax.bar(x - 0.1, msf2fs_spf_iops, width=0.1, capsize=3, label="msF2FS (SPF)") 
    rects3 = ax.bar(x, msf2fs_spf_e_iops, width=0.1, capsize=3, label="msF2FS (SPF-E)") 
    rects4 = ax.bar(x + 0.1, msf2fs_amfs_iops, width=0.1, capsize=3, label="msF2FS (AMFS)")
    rects5 = ax.bar(x + 0.2, zenfs_iops, width=0.1, capsize=3, label="zenFS")

    # For whatever reason we have to force the hatch patterns
    for i in range(len(f2fs_iops)):
        rects1[i].set_edgecolor("black")
        rects1[i].set_hatch("xx")
    for i in range(len(msf2fs_spf_iops)):
        rects2[i].set_edgecolor("black")
        rects2[i].set_hatch("o")
    for i in range(len(msf2fs_spf_e_iops)):
        rects3[i].set_edgecolor("black")
        rects3[i].set_hatch("/")
    for i in range(len(msf2fs_amfs_iops)):
        rects4[i].set_edgecolor("black")
        rects4[i].set_hatch("+")
    for i in range(len(zenfs_iops)):
        rects5[i].set_edgecolor("black")
        rects5[i].set_hatch("|")

    fig.tight_layout()
    ax.set_axisbelow(True)
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.legend(loc='best', ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(x_labs)
    ax.set_ylim(bottom=0,top=max)
    ax.set_ylabel(lab)
    plt.savefig(f'figs/rocksdb-throughput-{name}.pdf', bbox_inches='tight')
    plt.savefig(f'figs/rocksdb-throughput-{name}.png', bbox_inches='tight')
    plt.clf()

def plot_latency(f2fs_iops, msf2fs_spf_iops, msf2fs_spf_e_iops, msf2fs_amfs_iops, zenfs_iops, x_labs, name, max):
    x = np.arange(0, len(f2fs_iops))

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - 0.2, f2fs_iops, width=0.1, capsize=3, label="F2FS") 
    rects2 = ax.bar(x - 0.1, msf2fs_spf_iops, width=0.1, capsize=3, label="msF2FS (SPF)") 
    rects3 = ax.bar(x, msf2fs_spf_e_iops, width=0.1, capsize=3, label="msF2FS (SPF-E)") 
    rects4 = ax.bar(x + 0.1, msf2fs_amfs_iops, width=0.1, capsize=3, label="msF2FS (AMFS)")
    rects5 = ax.bar(x + 0.2, zenfs_iops, width=0.1, capsize=3, label="zenFS")

    # For whatever reason we have to force the hatch patterns
    for i in range(len(f2fs_iops)):
        rects1[i].set_edgecolor("black")
        rects1[i].set_hatch("xx")
    for i in range(len(msf2fs_spf_iops)):
        rects2[i].set_edgecolor("black")
        rects2[i].set_hatch("o")
    for i in range(len(msf2fs_spf_e_iops)):
        rects3[i].set_edgecolor("black")
        rects3[i].set_hatch("/")
    for i in range(len(msf2fs_amfs_iops)):
        rects4[i].set_edgecolor("black")
        rects4[i].set_hatch("+")
    for i in range(len(zenfs_iops)):
        rects5[i].set_edgecolor("black")
        rects5[i].set_hatch("|")

    fig.tight_layout()
    ax.set_axisbelow(True)
    ax.grid(which='major', linestyle='dashed', linewidth='1')
    ax.legend(loc='best', ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(x_labs)
    ax.set_ylim(bottom=0,top=max)
    ax.set_ylabel('Latency (usec)')
    plt.savefig(f'figs/rocksdb-latency-{name}.pdf', bbox_inches='tight')
    plt.savefig(f'figs/rocksdb-latency-{name}.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    # Write data
    f2fs_write = [73.795, 51.429]
    msf2fs_spf_write = [70.616, 60.922]
    msf2fs_spf_e_write = [0, 0]
    msf2fs_amfs_write = [0 , 0]
    zenfs_write = [76.853, 69.010]

    plot_throughput(f2fs_write, msf2fs_spf_write, msf2fs_spf_e_write, msf2fs_amfs_write, zenfs_write, ["fillrandom", "overwrite"], "write", 130, "1000 Ops/sec")

    # Read data
    f2fs_read = [623, 610, 616]
    msf2fs_spf_read = [1222, 998, 959]
    msf2fs_spf_e_read = [0, 0, 0]
    msf2fs_amfs_read = [0 , 0, 0]
    zenfs_read = [660, 633, 649]

    plot_throughput(f2fs_read, msf2fs_spf_read, msf2fs_spf_e_read, msf2fs_amfs_read, zenfs_read, ["randread", "readwhilewrite", "readwhilewriting (20MiB)"], "read", 1500, "Ops/sec")

    # Write Lats
    f2fs_lats = [14.738049, 25.977038]
    msf2fs_spf_lats = [16.053960, 29.752540]
    msf2fs_spf_e_lats = [0, 0]
    msf2fs_amfs_lats = [0, 0]
    zenfs_lats = [11.810868, 21.038380]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, zenfs_lats, ["P95", "P99"], "write", 50)

    # overwrite Lats
    f2fs_lats = [17.586594, 35.767433]
    msf2fs_spf_lats = [18.232131, 32.566096]
    msf2fs_spf_e_lats = [0, 0]
    msf2fs_amfs_lats = [0, 0]
    zenfs_lats = [12.380804, 22.905761]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, zenfs_lats, ["P95", "P99"], "overwrite", 50)

    # Read Lats
    f2fs_lats = [416.587603, 2411.761345]
    msf2fs_spf_lats = [417.537183, 12845.643518]
    msf2fs_spf_e_lats = [0, 0]
    msf2fs_amfs_lats = [0, 0]
    zenfs_lats = [361.769158, 10961.3309450]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, zenfs_lats, ["P95", "P99"], "read", 20000)

    # readwhilewriting Lats
    f2fs_lats = [487.962679, 3344.948109]
    msf2fs_spf_lats = [284.704503, 1141.125387]
    msf2fs_spf_e_lats = [0, 0]
    msf2fs_amfs_lats = [0, 0]
    zenfs_lats = [301.114651, 1127.022575]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, zenfs_lats, ["P95", "P99"], "readwhilewriting", 5000)

    # readwhilewriting writelimited Lats
    f2fs_lats = [600.258019, 22344.327214]
    msf2fs_spf_lats = [328.609658, 6111.381415]
    msf2fs_spf_e_lats = [0, 0]
    msf2fs_amfs_lats = [0, 0]
    zenfs_lats = [346.995140, 2725.069089]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, zenfs_lats, ["P95", "P99"], "readwhilewriting-limited", 30000)
