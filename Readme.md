# msF2FS-bench

This repo contains the benchmarking scripts, collected data, and plot generation scripts on the evaluation of [msf2fs](https://github.com/nicktehrany/msF2FS). We now detail the contents of this repository and the run instructions for each of the benchmarks.
This work is a result of my thesis at the TUDelft, the full thesis is available [here](). Consult it for further details on msF2FS and evaluation setup/results. /////TODO LINK

## Requirements

The required software requires the different kernels for msF2FS and F2FS

- Running Linux with F2FS Kernel (default Kernel)
- Running Linux with msF2FS Kernel (Kernel available [here](https://github.com/nicktehrany/msF2FS))
- A ZNS device to evaluate on

Benchmarking Software (other version may also work):

- [qemu](https://download.qemu.org/qemu-7.1.0.tar.xz) (version 7.1.0)
- fio (version 3.32, git commit: `6b6f52b`)
- nvme-cli tools (version 2.2.1, git commit: `b7ac8e4`)
- f2fs-tools (version 1.15.0)
- RocksDB and db\_bench (version 7.3, git commit: `01fdec2`) from our build with msF2FS hints (available [here](https://github.com/nicktehrany/rocksdb)) - checkout respective branch for the different hint integrations
- ZenFS (version `on master-branch`, git commit: `b04ca0c`)
- bpftrace (version 0.16, git commit: `ed06d87`)
- FEMU (version 7.0.0, git commit `ad786ad`)

The last requirements are `zbdbench` and `zns-tools`, which are added as submodules.

```bash
git submodule update --init --recursive
```

### Code modifications

Fio requires a minor patch to pass valid write hints to 5.17+ Kernels.

```bash
user@stosys:~/src/fio$ git diff ioengines.c
diff --git a/ioengines.c b/ioengines.c
index e2316ee4..525cbcd1 100644
--- a/ioengines.c
    +++ b/ioengines.c
@@ -587,9 +587,6 @@ int td_io_open_file(struct thread_data *td, struct fio_file *f)
    * the file descriptor. For buffered IO, we need to set
    * it on the inode.                                                                                                  10                  */
-               if (td->o.odirect)
    -                       cmd = F_SET_FILE_RW_HINT;
    -               else
    cmd = F_SET_RW_HINT;

    if (fcntl(f->fd, cmd, &hint) < 0) {
```

## Information on our Setup

We detail the setup used during our evaluation.

- CPU: 
    - Host: Dual socket Intel(R) Xeon(R) Silver 4210 CPU @ 2.20GHz, 10 cores/socket, hyper-threading enabled, with Spectre and       Meltdown patches
    - qemu VM: 34 cores
- DRAM: 
    - Host: 256 GiB, DDR4 
    - qemu VM (micro-benchmarks): 25GiB
    - qemu VM (macro-benchmarks): 64GiB
- ZNS Device:
    - Western Digital PCIe 3.0 Ultrastar DC 8,192 GiB ZN540 ([product link](\href{https://www.westerndigital.com/products/internal-drives/data-center-drives/ultrastar-dc-zn540-nvme-ssd#0TS2097))
    - zone size: 2,048 MiB
    - zone capacity: 1,077 MiB
    - number of zones: 3,688
    - Max. active zones: 14

**Note,** all benchmarks are setup to match the size requirements of the ZNS device we use. For the file systems it always creates a 19GiB `nullblk` device to store metadata, as this is the minimum size required. If a smaller device is used, simply align the size of the `nullblk` device in each of the scripts inside a function call for creating the device, replace the following (the last number `19456` in MiB) to match your setup:

```bash
DEV=$(sudo ../nullblk_create 512 19456) 
```

## Directory Structure

This repo contains numerous benchmarks, which each focus on evaluating a different aspect. We detail each of the benchmarks, what purpose they serve and how to run them. **Note,** there are different benchmarks for msF2FS and F2FS, therefore always have the valid Kernel running for F2FS or msF2FS.

### femu-test

The `femu-test/femu-baseline/` dir contains the evaluation of intra- and inter-zone scalability of FEMU, compared to real ZNS hardware. The benchmark is run as follows:

```bash
$ cd femu-test/femu-baseline/

# Run bench on FEMU
$ ./bench nvme0n2 femu-bench

# Run bench on ZNS
$ ./bench nvme0n2 zns-new 

# Plot results
$ python3 plot.py
```

Note, we utilize 2 real ZNS devices and FEMU. To reduce it to 2, simply modify the plotting script.

### zns-baseline

The `zns-baseline/` dir contains the evaluation of the LBAF choice for the selected ZNS device. The benchmark is run as follows:

```bash
$ cd zns-baseline/
$ ./bench nvme0n2
$ python3 plot.py
```

### msF2FS-throughput

The `msF2FS-throughput/` dir contains the benchmark to evaluate the performance of msF2FS allocation policies under concurrent file writes, compared to F2FS. The benchmark is run with:

```bash
$ cd msF2FS-throughput/

# Run bench on F2FS
$ ./bench-f2fs nvme0n2

# Run bench on msF2FS
$ ./bench-msf2fs nvme0n2

# Plot results
$ python3 plot.py
```

### gc-concurrent

The `gc-concurrent/` dir contains the benchmark that triggers heavy GC traffic on F2FS, whereas the improved data allocation in msF2FS avoids GC. The benchmark is run with:

```bash
$ cd gc-concurrent/

# Run F2FS bench
$ ./bench-f2fs nvme0n2

# Run msF2FS bench
$ ./bench-msf2fs nvme0n2

# Plot results
$ python3 plot.y
```

### gc

The `gc/` dir contains the benchmark that triggers less GC than the `gc-concurrent` benchmark, and instead overwrites just a single file. The benchmark is run with:

```bash
$ cd gc/

# Run F2FS bench
$ ./bench-f2fs nvme0n2

# Run msF2FS bench
$ ./bench-msf2fs nvme0n2

# Plot results
$ python3 plot.y
```

### zone-resets

The `zone-resets/` dir contains the benchmark to characterize the zone reset commands issued to the device. It requires to utilize the `zns-tools` to trace the zone management activity. The benchmark is run as follows (**Note,** the tracing requires be interrupted manually once the benchmark is finished):

```bash
$ cd zone-resets/

# For F2FS
$ ./bench-f2fs nvme0n2 

# In a new shell
$ cd submodules/zns-tools/zns.trace
$ ./zns.trace nvme0n2
# INTERRUPT the trace once benchmark is finished

# Plot the resulting trace data [-s zone size, -z number of zones]
$ python3 plot.py -s 4194304 -z 3688

# For msF2FS
$ ./bench-msf2fs nvme0n2 

# In a new shell
$ cd submodules/zns-tools/zns.trace
$ ./zns.trace nvme0n2
# INTERRUPT the trace once benchmark is finished

# Plot the resulting trace data [-s zone size, -z number of zones]
$ python3 plot.py -s 4194304 -z 3688
```

### zbdbench

For evaluating the macro-level performance we utilize the [`zbdbench`](https://github.com/westerndigitalcorporation/zbdbench) framework to generate the RocksDB workload. We make several modifications, which we detail here (modify the mount options for F2FS, depending on if msF2FS or F2FS is running, and adapt the `-o stream_policy=` accordingly). The modifications we make are shown in the diff below (we also modify the size of the `nullblk` device to be 19GiB):

```bash
user@stosys:~/src/msF2FS-bench/submodules/zbdbench$ git diff
diff --git a/benchs/usenix_atc_2021_zns_eval.py b/benchs/usenix_atc_2021_zns_eval.py
index 3fce92d..5aff723 100644
--- a/benchs/usenix_atc_2021_zns_eval.py
+++ b/benchs/usenix_atc_2021_zns_eval.py
@@ -24,7 +24,8 @@ class Run(Bench):
     # Original run on a 2TB ZNS SSD: (3.8B)
     # scale_num = 3800000000
     # The current state of ZenFS creates a bit more space amplification
-    scale_num = 3300000000
+    scale_num = 6000000000

     # All benchmarks
     wb_size = str(2 * 1024 * 1024 * 1024)
@@ -64,7 +65,7 @@ class Run(Bench):
                       " --key_size=", self.key_size, \
                       " --value_size=", self.value_size, \
                       " --target_file_size_base=", self.target_fz_base, \
-                      " --write_buffer_size=", self.wb_size, \
+                      " --open_files=1000 --write_buffer_size=", self.wb_size, \
                       " --max_bytes_for_level_base=", self.max_bytes_for_level_base, \
                       " --max_bytes_for_level_multiplier=4", \
                       " --max_background_jobs=8", \
@@ -186,8 +187,9 @@ class Run(Bench):

     def create_mountpoint(self, dev, filesystem):
         relative_mountpoint = "%s_%s" % (dev.strip('/dev/'), filesystem)
-        mountpoint = os.path.join(self.output, relative_mountpoint)
-        os.mkdir(mountpoint)
+        # mountpoint = os.path.join(self.output, relative_mountpoint)
+        mountpoint = "/mnt/f2fs"
+        # os.mkdir(mountpoint)
         return mountpoint, relative_mountpoint

     def create_new_nullblk_dev_config_path(self):
@@ -209,6 +211,8 @@ class Run(Bench):

     def create_f2fs_nullblk_dev(self, dev, container):
         dev_config_path = self.create_new_nullblk_dev_config_path()
+        with open(os.path.join(dev_config_path, 'size') , "w") as f:
+            f.write("19456")
         with open(os.path.join(dev_config_path, 'blocksize') , "w") as f:
             f.write(str(self.get_sector_size(dev)))
         with open(os.path.join(dev_config_path, 'memory_backed') , "w") as f:
@@ -231,8 +235,8 @@ class Run(Bench):
             self.conv_nullblk_dev = self.create_f2fs_nullblk_dev(dev, container)
             self.run_cmd(dev, container, 'mkfs.f2fs', f'-f -o 5 -m -c {dev} {self.conv_nullblk_dev}', f'-v "{self.conv_nullbl
k_dev}:{self.conv_nullblk_dev}"')
             subprocess.check_call('sudo modprobe f2fs', shell=True)
-            subprocess.check_call(f'mount -t f2fs -o active_logs=6,whint_mode=user-based {self.conv_nullblk_dev} {mountpoint}
', shell=True)
-            self.db_env_param = f'--db=/output/{relative_mountpoint}/eval'
+            subprocess.check_call(f'mount -t f2fs -o hot_data_streams=2 -o warm_data_streams=3 -o cold_data_streams=4 -o stre
am_policy=amfs {self.conv_nullblk_dev} /mnt/f2fs', shell=True)
+            self.db_env_param = f'--db=/mnt/f2fs/eval'
             return mountpoint
         else:
             print("Filesystem %s is not currently not supported for ZNS drives in this benchmark" % filesystem)
```

Then running zbdbench (copy results manually to `zbdbench-data/` dir to plot with `python3 plot.py`):

```bash
./run.py -d /dev/nvme0n2 -c no -b usenix_atc_2021_zns_eval
```
