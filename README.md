# Multithreading-Assignment

# Python Multithreading Assignment

This repository contains implementations of multithreaded algorithms and utilities for the Sai University School of Computing and Data Science multithreading assignment.

## Contents

1. [Multithreaded Merge Sort](#multithreaded-merge-sort)
2. [Multithreaded Quicksort](#multithreaded-quicksort)
3. [Concurrent File Downloader](#concurrent-file-downloader)
4. [Optional Challenge: ThreadPoolExecutor](#optional-challenge-threadpoolexecutor)

## Requirements

- Python 3.6+
- No external dependencies required (only standard library modules are used)

## Multithreaded Merge Sort

The `merge_sort.py` script implements a multithreaded version of the merge sort algorithm.

### Features

- Recursive thread creation for sorting subarrays
- Parameter to control minimum subarray size for threading
- Performance comparison with sequential merge sort

### Usage

```bash
python merge_sort.py --size 100000 --runs 3 --min-size 1000
```

Parameters:
- `--size`: Size of random array to sort (default: 100000)
- `--runs`: Number of benchmark runs (default: 3)
- `--min-size`: Minimum array size to use threading (default: 1000)

### Sample Output

```
Benchmarking with array size: 100000, runs: 3
Run 1:
  Sequential: 0.1543 seconds
  Threaded:   0.0912 seconds
  Speedup:    1.69x
Run 2:
  Sequential: 0.1467 seconds
  Threaded:   0.0879 seconds
  Speedup:    1.67x
Run 3:
  Sequential: 0.1489 seconds
  Threaded:   0.0895 seconds
  Speedup:    1.66x

Average times:
  Sequential: 0.1500 seconds
  Threaded:   0.0895 seconds
  Speedup:    1.67x
```

## Multithreaded Quicksort

The `quicksort.py` script implements a multithreaded version of the quicksort algorithm.

### Features

- Controlled thread creation to avoid excessive threading
- Dynamically falls back to sequential sort when thread limit is reached
- Performance comparison with sequential quicksort

### Usage

```bash
python quicksort.py --size 100000 --runs 3 --threads 4
```

Parameters:
- `--size`: Size of random array to sort (default: 100000)
- `--runs`: Number of benchmark runs (default: 3)
- `--threads`: Maximum number of threads to use (default: 4)

### Sample Output

```
Benchmarking with array size: 100000, runs: 3, max threads: 4
Run 1:
  Sequential: 0.1256 seconds
  Threaded:   0.0823 seconds
  Speedup:    1.53x
Run 2:
  Sequential: 0.1214 seconds
  Threaded:   0.0801 seconds
  Speedup:    1.52x
Run 3:
  Sequential: 0.1228 seconds
  Threaded:   0.0809 seconds
  Speedup:    1.52x

Average times:
  Sequential: 0.1233 seconds
  Threaded:   0.0811 seconds
  Speedup:    1.52x
```

## Concurrent File Downloader

The `file_downloader.py` script downloads multiple files concurrently using threads.

### Features

- Downloads files from provided URLs using multiple threads
- Creates separate thread for each download
- Optional ThreadPoolExecutor implementation
- Performance comparison with sequential downloading

### Usage

```bash
# With command line URLs
python file_downloader.py --urls https://example.com/file1.txt https://example.com/file2.txt

# With URLs from a file
python file_downloader.py --file urls.txt

# Using ThreadPoolExecutor
python file_downloader.py --urls https://example.com/file1.txt https://example.com/file2.txt --use-pool --max-workers 4
```

Parameters:
- `--urls`: List of URLs to download
- `--file`: File containing URLs (one per line)
- `--output`: Output directory (default: "downloads")
- `--use-pool`: Use ThreadPoolExecutor instead of raw threads
- `--max-workers`: Maximum worker threads for pool

### Sample URL File (urls.txt)

```
https://speed.hetzner.de/100MB.bin
https://speed.hetzner.de/10MB.bin
https://httpbin.org/image/jpeg
https://httpbin.org/image/png
https://httpbin.org/image/svg
```

### Sample Output

```
Preparing to download 5 files

Starting sequential download...
Downloaded https://httpbin.org/image/jpeg to downloads/jpeg
Downloaded https://httpbin.org/image/png to downloads/png
Downloaded https://httpbin.org/image/svg to downloads/svg
Downloaded https://speed.hetzner.de/10MB.bin to downloads/10MB.bin
Downloaded https://speed.hetzner.de/100MB.bin to downloads/100MB.bin
Sequential download completed in 15.72 seconds

Starting threaded download...
Downloaded https://httpbin.org/image/jpeg to downloads/jpeg
Downloaded https://httpbin.org/image/png to downloads/png
Downloaded https://httpbin.org/image/svg to downloads/svg
Downloaded https://speed.hetzner.de/10MB.bin to downloads/10MB.bin
Downloaded https://speed.hetzner.de/100MB.bin to downloads/100MB.bin
Threaded download completed in 6.23 seconds

Speedup with threading: 2.52x
```

## Optional Challenge: ThreadPoolExecutor

The file downloader includes an implementation using ThreadPoolExecutor. This approach provides:

- More efficient thread management
- Control over maximum concurrency
- Simplified error handling

To use this implementation, add the `--use-pool` flag when running the file downloader.

## Approach and Implementation Details

### General Approach

Each implementation follows these principles:

1. Implement a sequential version of the algorithm first
2. Add multithreading with appropriate control mechanisms
3. Benchmark both versions to compare performance
4. Ensure correctness by verifying results

### Thread Creation Strategy

- **Merge Sort**: Creates threads recursively, with a minimum array size threshold to avoid excessive thread creation for small arrays
- **Quicksort**: Limits the total number of active threads and reverts to sequential sorting when the limit is reached
- **File Downloader**: Creates one thread per file or uses a thread pool with configurable worker count

### Performance Considerations

- Thread creation has overhead, so it's important to find the right balance
- For sorting algorithms, using threads only for larger chunks improves performance
- The ideal number of threads depends on CPU cores and workload characteristics
- Thread pools provide better resource management for many small tasks
