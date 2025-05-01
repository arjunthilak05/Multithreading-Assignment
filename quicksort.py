#!/usr/bin/env python3
"""
Multi-threaded Quicksort implementation
"""

import threading
import time
import random
import argparse
from typing import List


def partition(arr: List[int], low: int, high: int) -> int:
    """
    Partition the array and return the pivot index.
    Uses the last element as the pivot.
    """
    pivot = arr[high]
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def sequential_quicksort(arr: List[int], low: int, high: int):
    """Regular sequential quicksort implementation."""
    if low < high:
        # Get pivot position
        pivot_idx = partition(arr, low, high)
        
        # Sort elements before and after pivot
        sequential_quicksort(arr, low, pivot_idx - 1)
        sequential_quicksort(arr, pivot_idx + 1, high)


def threaded_quicksort(arr: List[int], low: int, high: int, max_threads: int = 4, thread_count: List[int] = None):
    """
    Multi-threaded quicksort implementation.
    Controls number of threads with max_threads parameter.
    """
    # Initialize thread counter if this is the first call
    if thread_count is None:
        thread_count = [0]  # Use a list to make it mutable across function calls
    
    if low < high:
        # Get pivot position
        pivot_idx = partition(arr, low, high)
        
        # Create threads if we haven't reached the maximum
        if thread_count[0] < max_threads:
            # Create a new thread for the left part
            thread_count[0] += 1
            left_thread = threading.Thread(
                target=threaded_quicksort,
                args=(arr, low, pivot_idx - 1, max_threads, thread_count)
            )
            left_thread.start()
            
            # Process the right part in this thread
            threaded_quicksort(arr, pivot_idx + 1, high, max_threads, thread_count)
            
            # Wait for the left thread to complete
            left_thread.join()
            thread_count[0] -= 1
        else:
            # If we've reached the thread limit, revert to sequential sort
            sequential_quicksort(arr, low, pivot_idx - 1)
            sequential_quicksort(arr, pivot_idx + 1, high)


def run_benchmarks(size: int = 100000, num_runs: int = 3, max_threads: int = 4):
    """Run benchmarks comparing sequential and threaded quicksort."""
    print(f"Benchmarking with array size: {size}, runs: {num_runs}, max threads: {max_threads}")
    
    total_sequential = 0
    total_threaded = 0
    
    for i in range(num_runs):
        # Generate random arrays
        arr1 = [random.randint(0, 10000) for _ in range(size)]
        arr2 = arr1.copy()  # Use the same array for fair comparison
        
        # Time sequential quicksort
        start = time.time()
        sequential_quicksort(arr1, 0, len(arr1) - 1)
        sequential_time = time.time() - start
        total_sequential += sequential_time
        
        # Time threaded quicksort
        start = time.time()
        threaded_quicksort(arr2, 0, len(arr2) - 1, max_threads)
        threaded_time = time.time() - start
        total_threaded += threaded_time
        
        # Verify correctness
        assert arr1 == arr2, "Sorting results do not match!"
        
        print(f"Run {i+1}:")
        print(f"  Sequential: {sequential_time:.4f} seconds")
        print(f"  Threaded:   {threaded_time:.4f} seconds")
        print(f"  Speedup:    {sequential_time/threaded_time:.2f}x")
    
    # Calculate and display averages
    avg_sequential = total_sequential / num_runs
    avg_threaded = total_threaded / num_runs
    
    print("\nAverage times:")
    print(f"  Sequential: {avg_sequential:.4f} seconds")
    print(f"  Threaded:   {avg_threaded:.4f} seconds")
    print(f"  Speedup:    {avg_sequential/avg_threaded:.2f}x")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Multi-threaded Quicksort')
    parser.add_argument('--size', type=int, default=100000, 
                        help='Size of the array to sort')
    parser.add_argument('--runs', type=int, default=3, 
                        help='Number of benchmark runs')
    parser.add_argument('--threads', type=int, default=4, 
                        help='Maximum number of threads to use')
    
    args = parser.parse_args()
    
    # Run the benchmark
    run_benchmarks(args.size, args.runs, args.threads)