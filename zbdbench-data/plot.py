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

def plot_throughput(f2fs_iops, msf2fs_spf_iops, msf2fs_spf_e_iops, msf2fs_amfs_iops, msf2fs_amfs_2_iops, zenfs_iops, x_labs, name, max, lab):
    x = np.arange(0, len(f2fs_iops))

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - 0.25, f2fs_iops, width=0.08, capsize=3, color="#117733", label="F2FS") 
    rects2 = ax.bar(x - 0.15, msf2fs_spf_iops, width=0.08, capsize=3, color="#88CCEE", label="msF2FS (SPF)") 
    rects3 = ax.bar(x - 0.05, msf2fs_spf_e_iops, width=0.08, capsize=3, color="#CC6677", label="msF2FS (SPF-E)")
    rects4 = ax.bar(x + 0.05, msf2fs_amfs_iops, width=0.08, capsize=3, color="#DDCC77", label="msF2FS (AMFS-1)") 
    rects5 = ax.bar(x + 0.15, msf2fs_amfs_2_iops, width=0.08, capsize=3, color="#AA4499", label="msF2FS (AMFS-2)")
    rects6 = ax.bar(x + 0.25, zenfs_iops, width=0.08, capsize=3, color="#999933", label="ZenFS")

    # For whatever reason we have to force the hatch patterns
    for i in range(len(f2fs_iops)):
        rects1[i].set_edgecolor("black")
        rects1[i].set_hatch("-\\")
    for i in range(len(msf2fs_spf_iops)):
        rects2[i].set_edgecolor("black")
        rects2[i].set_hatch("o")
    for i in range(len(msf2fs_spf_e_iops)):
        rects3[i].set_edgecolor("black")
        rects3[i].set_hatch("/")
    for i in range(len(msf2fs_amfs_iops)):
        rects4[i].set_edgecolor("black")
        rects4[i].set_hatch("xx")
    for i in range(len(zenfs_iops)):
        rects5[i].set_edgecolor("black")
        rects5[i].set_hatch("\\")
    for i in range(len(msf2fs_amfs_2_iops)):
        rects6[i].set_edgecolor("black")
        rects6[i].set_hatch("+")

    fig.tight_layout()
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle='dashed', linewidth='1')
    ax.legend(loc='best', ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(x_labs)
    ax.set_ylim(bottom=0,top=max)
    ax.set_ylabel(lab)
    plt.savefig(f'figs/rocksdb-throughput-{name}.pdf', bbox_inches='tight')
    plt.savefig(f'figs/rocksdb-throughput-{name}.png', bbox_inches='tight')
    plt.clf()

def plot_latency(f2fs_iops, msf2fs_spf_iops, msf2fs_spf_e_iops, msf2fs_amfs_iops, msf2fs_amfs_2_iops, zenfs_iops, x_labs, name, max, log):
    x = np.arange(0, len(f2fs_iops))

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - 0.25, f2fs_iops, width=0.08, capsize=3, color="#117733", label="F2FS") 
    rects2 = ax.bar(x - 0.15, msf2fs_spf_iops, width=0.08, capsize=3, color="#88CCEE", label="msF2FS (SPF)")
    rects3 = ax.bar(x - 0.05, msf2fs_spf_e_iops, width=0.08, capsize=3, color="#CC6677", label="msF2FS (SPF-E)") 
    rects4 = ax.bar(x + 0.05, msf2fs_amfs_iops, width=0.08, capsize=3, color="#DDCC77", label="msF2FS (AMFS-1)")
    rects5 = ax.bar(x + 0.15, msf2fs_amfs_2_iops, width=0.08, capsize=3, color="#AA4499", label="msF2FS (AMFS-2)")
    rects6 = ax.bar(x + 0.25, zenfs_iops, width=0.08, capsize=3, color="#999933", label="ZenFS")

    # For whatever reason we have to force the hatch patterns
    for i in range(len(f2fs_iops)):
        rects1[i].set_edgecolor("black")
        rects1[i].set_hatch("-\\")
    for i in range(len(msf2fs_spf_iops)):
        rects2[i].set_edgecolor("black")
        rects2[i].set_hatch("o")
    for i in range(len(msf2fs_spf_e_iops)):
        rects3[i].set_edgecolor("black")
        rects3[i].set_hatch("/")
    for i in range(len(msf2fs_amfs_iops)):
        rects4[i].set_edgecolor("black")
        rects4[i].set_hatch("xx")
    for i in range(len(zenfs_iops)):
        rects5[i].set_edgecolor("black")
        rects5[i].set_hatch("\\")
    for i in range(len(msf2fs_amfs_2_iops)):
        rects6[i].set_edgecolor("black")
        rects6[i].set_hatch("+")

    fig.tight_layout()
    ax.set_axisbelow(True)
    ax.yaxis.grid(which='major', linestyle='dashed', linewidth='1')
    ax.legend(loc='best', ncol=2)
    ax.xaxis.set_ticks(x)
    if log:
        plt.yscale("log")
        ax.set_ylim(top=max)
    else:
        ax.set_ylim(bottom=0,top=max)
    ax.xaxis.set_ticklabels(x_labs)
    ax.set_ylabel('Latency (usec)')
    plt.savefig(f'figs/rocksdb-latency-{name}.pdf', bbox_inches='tight')
    plt.savefig(f'figs/rocksdb-latency-{name}.png', bbox_inches='tight')
    plt.clf()

if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    # Write data
    f2fs_write = [73.795, 51.429]
    msf2fs_spf_write = [70.616, 60.922]
    msf2fs_spf_e_write = [72.195, 63.357]
    msf2fs_amfs_write = [69.910 , 58.985]
    msf2fs_amfs_2_write = [72.624, 61.213]
    zenfs_write = [76.853, 69.010]

    plot_throughput(f2fs_write, msf2fs_spf_write, msf2fs_spf_e_write, msf2fs_amfs_write, msf2fs_amfs_2_write, zenfs_write, ["fillrandom", "overwrite"], "write", 110, "1000 Ops/sec")

    # Read data
    f2fs_read = [623, 610, 616]
    msf2fs_spf_read = [1222, 998, 959]
    msf2fs_spf_e_read = [1134, 863, 1029]
    msf2fs_amfs_read = [1238 , 892, 965]
    msf2fs_amfs_2_read = [607, 610, 632]
    zenfs_read = [660, 633, 649]

    plot_throughput(f2fs_read, msf2fs_spf_read, msf2fs_spf_e_read, msf2fs_amfs_read, msf2fs_amfs_2_read, zenfs_read, ["randread", "readwhilewrite", "readwhilewriting (20MiB)"], "read", 1600, "Ops/sec")

    # Write Lats
    f2fs_lats = [14.738049, 25.977038]
    msf2fs_spf_lats = [16.053960, 29.752540]
    msf2fs_spf_e_lats = [14.788194, 26.626169]
    msf2fs_amfs_lats = [16.530214, 30.273536]
    msf2fs_amfs_2_lats = [14.794708, 26.753575]
    zenfs_lats = [11.810868, 21.038380]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, msf2fs_amfs_2_lats, zenfs_lats, ["P95", "P99"], "write", 50, False)

    # overwrite Lats
    f2fs_lats = [17.586594, 35.767433]
    msf2fs_spf_lats = [18.232131, 32.566096]
    msf2fs_spf_e_lats = [15.724927, 30.529997]
    msf2fs_amfs_lats = [18.506720, 33.022910]
    msf2fs_amfs_2_lats = [16.239443, 31.420705]
    zenfs_lats = [12.380804, 22.905761]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, msf2fs_amfs_2_lats, zenfs_lats, ["P95", "P99"], "overwrite", 50, False)

    # Read Lats
    f2fs_lats = [416.587603, 2411.761345]
    msf2fs_spf_lats = [417.537183, 12845.643518]
    msf2fs_spf_e_lats = [484.398275, 16009.673558]
    msf2fs_amfs_lats = [354.073745, 10595.708534]
    msf2fs_amfs_2_lats = [369.250516, 1615.725613]
    zenfs_lats = [361.769158, 10961.3309450]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, msf2fs_amfs_2_lats, zenfs_lats, ["P95", "P99"], "read", 10**5, True)

    # readwhilewriting Lats
    f2fs_lats = [487.962679, 3344.948109]
    msf2fs_spf_lats = [284.704503, 1141.125387]
    msf2fs_spf_e_lats = [293.424281, 1306.767882]
    msf2fs_amfs_lats = [300.303559, 1277.891397]
    msf2fs_amfs_2_lats = [428.024368, 1736.942585]
    zenfs_lats = [301.114651, 1127.022575]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, msf2fs_amfs_2_lats, zenfs_lats, ["P95", "P99"], "readwhilewriting", 10**4, True)

    # readwhilewriting writelimited Lats
    f2fs_lats = [600.258019, 22344.327214]
    msf2fs_spf_lats = [328.609658, 6111.381415]
    msf2fs_spf_e_lats = [331.991439, 6530.699213]
    msf2fs_amfs_lats = [395.710518, 10509.244370]
    msf2fs_amfs_2_lats = [567.552920, 21702.167793]
    zenfs_lats = [346.995140, 2725.069089]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, msf2fs_amfs_2_lats, zenfs_lats, ["P95", "P99"], "readwhilewriting-limited", 10**5, True)
