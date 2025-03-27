#!/usr/bin/env python3
"""
I;ve updated my previous XSS scanner for CTF challenges
------------------------------------
Scans a domain for XSS vulnerabilities using custom payloads.
Works best on simple CTF challenges with GET parameter injection points.

TODO: Add POST request support
"""

import argparse
import os
import re
import sys
import time
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import requests


# Defaults - change these if you always use different files
PAYLOADS_FILE = "payload.txt"
DOMAINS_FILE = "domain.txt"
MAX_THREADS = 3  # Don't hammer the CTF server too hard


def read_file(filename):
    """Read entries from a file, skipping empty lines and comments."""
    if not os.path.exists(filename):
        print(f"Error: File {filename} not found!")
        sys.exit(1)
        
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def find_parameters(html, url):
    """Try to find injectable parameters in the page."""
    params = set()
    
    # Look for input fields
    inputs = re.findall(r'<input.*?name=[\'"](.+?)[\'"]', html)
    if inputs:
        params.update(inputs)
    
    # Look for URL parameters
    url_params = re.findall(r'[?&]([^=&]+)=', url)
    if url_params:
        params.update(url_params)
        
    # No params? Try some common ones as fallback
    if not params:
        params = {"q", "search", "id", "xss", "payload", "test"}
        
    return params


def test_url(domain, payload, verbose=False):
    """Test a specific domain with a specific payload."""
    results = []
    url = f"http://{domain}"
    
    # Sometimes CTFs have weird timeouts
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        if verbose:
            print(f"Error accessing {url}: {e}")
        return []
    
    # Too many 'if "input" in response.text' checks miss stuff
    # Better to try to find actual parameters
    params = find_parameters(resp.text, resp.url)
    
    if verbose and params:
        print(f"Found potential parameters: {', '.join(params)}")
    
    # The meat of it - try each parameter with our payload
    for param in params:
        # Had to fix this in the middle of a CTF once
        test_payload = urllib.parse.quote(payload)
        test_url = f"{url}?{param}={test_payload}"
        
        try:
            test_resp = requests.get(test_url, timeout=5)
            
            # We got something!
            if payload in test_resp.text:
                # Grab some context to understand where it's reflected
                match = re.search(f".{{30}}{re.escape(payload)}.{{30}}", test_resp.text)
                context = match.group(0) if match else "Unknown context"
                
                results.append({
                    "url": test_url,
                    "param": param,
                    "payload": payload,
                    "context": context.replace(payload, f"HERE→{payload}←HERE")
                })
                
                if verbose:
                    print(f"✓ XSS found: {test_url}")
                    print(f"  Context: {context}")
                    
        except requests.RequestException:
            # Move on silently unless verbose
            if verbose:
                print(f"Request failed for {test_url}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="XSS Scanner for CTF challenges")
    parser.add_argument("-d", "--domain", help="Single domain to scan")
    parser.add_argument("-D", "--domains-file", default=DOMAINS_FILE,
                        help=f"File with domains to scan (default: {DOMAINS_FILE})")
    parser.add_argument("-p", "--payload", help="Single XSS payload to test")
    parser.add_argument("-P", "--payloads-file", default=PAYLOADS_FILE,
                        help=f"File with XSS payloads (default: {PAYLOADS_FILE})")
    parser.add_argument("-v", "--verbose", action="store_true", 
                        help="Show detailed progress")
    parser.add_argument("-o", "--output", help="Save results to file")
    args = parser.parse_args()
    
    # Get domains - either from arg or file
    if args.domain:
        domains = [args.domain]
    else:
        domains = read_file(args.domains_file)
    
    # Get payloads - either from arg or file
    if args.payload:
        payloads = [args.payload]
    else:
        payloads = read_file(args.payloads_file)
    
    if not domains or not payloads:
        print("Error: No domains or payloads to test!")
        parser.print_help()
        return
    
    print(f"Scanning {len(domains)} domain(s) with {len(payloads)} payload(s)...")
    start_time = time.time()
    
    # I kept this part simple on purpose - no need for fancy progressbars
    # in a CTF tool, but multithreading is actually useful
    all_results = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for domain in domains:
            for payload in payloads:
                futures.append(
                    executor.submit(test_url, domain, payload, args.verbose)
                )
        
        for future in futures:
            try:
                all_results.extend(future.result())
            except Exception as e:
                # This should never happen but just in case
                print(f"Error in worker thread: {e}")
    
    # Show results
    if all_results:
        print(f"\nFound {len(all_results)} XSS vulnerabilities:")
        for i, result in enumerate(all_results, 1):
            print(f"\n{i}. {result['url']}")
            print(f"   Payload: {result['payload']}")
            print(f"   Context: {result['context']}")
            
        # Save to file if requested
        if args.output:
            with open(args.output, 'w') as f:
                for i, result in enumerate(all_results, 1):
                    f.write(f"{i}. {result['url']}\n")
                    f.write(f"   Payload: {result['payload']}\n")
                    f.write(f"   Context: {result['context']}\n\n")
            print(f"\nResults saved to {args.output}")
    else:
        print("\nNo XSS vulnerabilities found. Try different payloads?")
    
    print(f"\nScan completed in {time.time() - start_time:.2f} seconds")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted. Exiting...")
    except Exception as e:
        print(f"Unexpected error: {e}")
