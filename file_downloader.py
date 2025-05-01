#!/usr/bin/env python3
"""
Concurrent File Downloader using threads
"""

import threading
import time
import argparse
import os
import urllib.request
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from typing import List
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context


def download_file(url: str, output_dir: str = "downloads") -> str:
    """
    Download a file from the given URL.
    Returns the path to the downloaded file.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Parse the URL to get the filename
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If filename is empty, use a default name with a timestamp
    if not filename:
        filename = f"file_{int(time.time())}"
    
    # Full path to save the file
    output_path = os.path.join(output_dir, filename)
    
    # Download the file
    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"Downloaded {url} to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None


def sequential_download(urls: List[str], output_dir: str = "downloads") -> float:
    """
    Download files sequentially and return the time taken.
    """
    start_time = time.time()
    
    for url in urls:
        download_file(url, output_dir)
    
    end_time = time.time()
    elapsed = end_time - start_time
    return elapsed


def threaded_download(urls: List[str], output_dir: str = "downloads") -> float:
    """
    Download files using multiple threads and return the time taken.
    """
    start_time = time.time()
    threads = []
    
    # Create and start a thread for each URL
    for url in urls:
        thread = threading.Thread(target=download_file, args=(url, output_dir))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    elapsed = end_time - start_time
    return elapsed


def thread_pool_download(urls: List[str], output_dir: str = "downloads", max_workers: int = None) -> float:
    """
    Download files using ThreadPoolExecutor and return the time taken.
    """
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit download tasks for each URL
        futures = [executor.submit(download_file, url, output_dir) for url in urls]
        
        # Wait for all tasks to complete (this happens automatically when exiting the context)
    
    end_time = time.time()
    elapsed = end_time - start_time
    return elapsed


def read_urls_from_file(file_path: str) -> List[str]:
    """
    Read URLs from a text file, one URL per line.
    """
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    return urls


def main():
    parser = argparse.ArgumentParser(description='Concurrent File Downloader')
    parser.add_argument('--urls', nargs='+', help='List of URLs to download')
    parser.add_argument('--file', help='File containing URLs (one per line)')
    parser.add_argument('--output', default='downloads', help='Output directory')
    parser.add_argument('--use-pool', action='store_true', help='Use ThreadPoolExecutor')
    parser.add_argument('--max-workers', type=int, help='Maximum worker threads for pool')
    
    args = parser.parse_args()
    
    # Get URLs from command line or file
    urls = []
    if args.urls:
        urls = args.urls
    elif args.file:
        urls = read_urls_from_file(args.file)
    else:
        # Example URLs for testing if none provided
        urls = [
            'https://speed.hetzner.de/100MB.bin',
            'https://speed.hetzner.de/10MB.bin',
            'https://httpbin.org/image/jpeg',
            'https://httpbin.org/image/png',
            'https://httpbin.org/image/svg'
        ]
        print("No URLs provided, using example URLs for testing.")
    
    print(f"Preparing to download {len(urls)} files")
    
    # Run sequential download
    print("\nStarting sequential download...")
    seq_time = sequential_download(urls, args.output)
    print(f"Sequential download completed in {seq_time:.2f} seconds")
    
    # Run threaded download
    print("\nStarting threaded download...")
    if args.use_pool:
        thread_time = thread_pool_download(urls, args.output, args.max_workers)
        print(f"ThreadPoolExecutor download completed in {thread_time:.2f} seconds")
    else:
        thread_time = threaded_download(urls, args.output)
        print(f"Threaded download completed in {thread_time:.2f} seconds")
    
    # Calculate and display the speedup
    speedup = seq_time / thread_time
    print(f"\nSpeedup with threading: {speedup:.2f}x")


if __name__ == "__main__":
    main()