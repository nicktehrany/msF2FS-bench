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

def plot_throughput(f2fs_iops, msf2fs_spf_iops, msf2fs_spf_e_iops, msf2fs_amfs_iops, zenfs_iops, x_labs, name):
    x = np.arange(0, 2)

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
    ax.legend(loc='upper right', ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(x_labs)
    ax.set_ylim(bottom=0,top=150)
    ax.set_ylabel('1000 Ops/sec')
    plt.savefig(f'figs/throughput-{name}.pdf', bbox_inches='tight')
    plt.savefig(f'figs/throughput-{name}.png', bbox_inches='tight')
    plt.clf()

def plot_latency(f2fs_iops, msf2fs_spf_iops, msf2fs_spf_e_iops, msf2fs_amfs_iops, zenfs_iops, x_labs, name):
    x = np.arange(0, 2)

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
    ax.legend(loc='upper right', ncol=2)
    ax.xaxis.set_ticks(x)
    ax.xaxis.set_ticklabels(x_labs)
    ax.set_ylim(bottom=0,top=150)
    ax.set_ylabel('Latency (msec)')
    plt.savefig(f'figs/latency-{name}.pdf', bbox_inches='tight')
    plt.savefig(f'figs/latency-{name}.png', bbox_inches='tight')
    plt.clf()
if __name__ == '__main__':
    file_path = '/'.join(os.path.abspath(__file__).split('/')[:-1])

    # Write data
    f2fs_write = [73.226, 47.653]
    msf2fs_spf_write = [70.887, 64.156]
    msf2fs_spf_e_write = [0, 0]
    msf2fs_amfs_write = [0 , 0]
    zenfs_write = [0, 0]

    plot_throughput(f2fs_write, msf2fs_spf_write, msf2fs_spf_e_write, msf2fs_amfs_write, zenfs_write, ["fillrandom", "overwrite"], "write")

    # Read data
    f2fs_read = [0.211, 0.202]
    msf2fs_spf_read = [0.094, 0.116]
    msf2fs_spf_e_read = [0, 0]
    msf2fs_amfs_read = [0 , 0]
    zenfs_read = [0, 0]

    plot_throughput(f2fs_read, msf2fs_spf_read, msf2fs_spf_e_read, msf2fs_amfs_read, zenfs_read, ["randread", "readwhilewrite"], "read")

    # Write and read data for write limited 20% readwhilewriting
    # f2fs_rw = []
    # msf2fs_spf_rw = []
    # msf2fs_spf_e_rw = []
    # msf2fs_amfs_rw = []
    # zenfs_rw = []

    # plot_throughput(f2fs_rw, msf2fs_spf_rw, msf2fs_spf_e_rw, msf2fs_amfs_rw, zenfs_rw, ["read", "write"])

    # Write Lats
    f2fs_lats = [0, 0]
    msf2fs_spf_lats = [0, 0]
    msf2fs_spf_e_lats = [0, 0]
    msf2fs_amfs_lats = [0, 0]
    zenfs_lats = [0, 0]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, zenfs_lats, ["99", "99.99"], "write")

    # Read Lats
    f2fs_lats = [0, 0]
    msf2fs_spf_lats = [0, 0]
    msf2fs_spf_e_lats = [0, 0]
    msf2fs_amfs_lats = [0, 0]
    zenfs_lats = [0, 0]

    plot_latency(f2fs_lats, msf2fs_spf_lats, msf2fs_spf_e_lats, msf2fs_amfs_lats, zenfs_lats, ["99", "99.99"], "read")

    # possible readwhilewriting lats
