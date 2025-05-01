#!/usr/bin/env python3
"""
Multi-threaded Merge Sort implementation
"""

import threading
import time
import random
import argparse
from typing import List


def merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted arrays into a single sorted array."""
    result = []
    i = j = 0
    
    # Compare elements from both arrays and merge them in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add any remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def sequential_merge_sort(arr: List[int]) -> List[int]:
    """Regular sequential merge sort implementation."""
    if len(arr) <= 1:
        return arr
        
    # Split the array
    mid = len(arr) // 2
    left = sequential_merge_sort(arr[:mid])
    right = sequential_merge_sort(arr[mid:])
    
    # Merge the sorted halves
    return merge(left, right)


def threaded_merge_sort(arr: List[int], min_size: int = 100) -> List[int]:
    """
    Multi-threaded merge sort implementation.
    Uses threads for arrays larger than min_size.
    """
    if len(arr) <= 1:
        return arr
        
    # Base case: use sequential sort for small arrays
    if len(arr) <= min_size:
        return sequential_merge_sort(arr)
    
    # Split the array
    mid = len(arr) // 2
    
    # Create containers for results
    left_result = [None]
    right_result = [None]
    
    # Define thread functions
    def sort_left():
        left_result[0] = threaded_merge_sort(arr[:mid], min_size)
    
    def sort_right():
        right_result[0] = threaded_merge_sort(arr[mid:], min_size)
    
    # Create and start threads
    left_thread = threading.Thread(target=sort_left)
    right_thread = threading.Thread(target=sort_right)
    
    left_thread.start()
    right_thread.start()
    
    # Wait for both threads to complete
    left_thread.join()
    right_thread.join()
    
    # Merge the sorted halves
    return merge(left_result[0], right_result[0])


def run_benchmarks(size: int = 100000, num_runs: int = 3):
    """Run benchmarks comparing sequential and threaded merge sort."""
    print(f"Benchmarking with array size: {size}, runs: {num_runs}")
    
    total_sequential = 0
    total_threaded = 0
    
    for i in range(num_runs):
        # Generate the same random array for both algorithms
        arr = [random.randint(0, 10000) for _ in range(size)]
        arr_copy = arr.copy()
        
        # Time sequential merge sort
        start = time.time()
        sequential_result = sequential_merge_sort(arr)
        sequential_time = time.time() - start
        total_sequential += sequential_time
        
        # Time threaded merge sort
        start = time.time()
        threaded_result = threaded_merge_sort(arr_copy)
        threaded_time = time.time() - start
        total_threaded += threaded_time
        
        # Verify correctness
        assert sequential_result == threaded_result, "Sorting results do not match!"
        
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
    parser = argparse.ArgumentParser(description='Multi-threaded Merge Sort')
    parser.add_argument('--size', type=int, default=100000, 
                        help='Size of the array to sort')
    parser.add_argument('--runs', type=int, default=3, 
                        help='Number of benchmark runs')
    parser.add_argument('--min-size', type=int, default=1000, 
                        help='Minimum array size to use threading')
    
    args = parser.parse_args()
    
    # Run the benchmark
    run_benchmarks(args.size, args.runs)