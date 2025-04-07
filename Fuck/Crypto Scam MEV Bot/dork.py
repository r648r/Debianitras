#!/usr/bin/env python3
# Google dork search tool

import argparse
import json
import os
import sys
import time
from datetime import datetime
from googlesearch import search

# Terminal colors
class Colors:
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

def print_colored(text, color, end="\n"):
    """Print text with color."""
    print(f"{color}{text}{Colors.ENDC}", end=end)

def log_to_json(dork, results, log_file="dork-log.json"):
    """Log search and results to JSON file."""
    # Create log structure
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "dork": dork,
        "results_count": len(results),
        "results": results
    }

    # Load existing log if it exists
    if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        except json.JSONDecodeError:
            log_data = {"searches": []}
    else:
        log_data = {"searches": []}

    # Add new entry and save
    log_data["searches"].append(log_entry)
    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=4)

    print_colored(f"[•] JSON log updated: {log_file}", Colors.BLUE)

def perform_search(dork, amount, output_file):
    """Perform Google dork search and save results to a file."""
    try:
        print_colored(f"[+] Starting search for: {dork}", Colors.YELLOW)
        print_colored(f"[+] Retrieving up to {amount} results...", Colors.YELLOW)

        # Clear the output file before starting
        open(output_file, 'w').close()

        counter = 0
        results = []

        for result in search(dork, tld="com", lang="en", num=amount, start=0, stop=None, pause=2):
            counter += 1
            print_colored(f"[+] {counter}: {result}", Colors.GREEN)
            results.append(result)

            # Write each result to file without numbering
            with open(output_file, 'a') as file:
                file.write(f"{result}\n")

            if counter >= amount:
                break

        print_colored(f"\n[•] Search completed. Found {counter} results.", Colors.BLUE)
        print_colored(f"[•] Results saved to {output_file}", Colors.BLUE)

        # Log results to JSON
        log_to_json(dork, results)

    except KeyboardInterrupt:
        print_colored("\n[!] User interrupted the search.", Colors.RED)
        # Still log the partial results we got
        if counter > 0:
            log_to_json(dork, results)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n[!] An error occurred: {e}", Colors.RED)
        sys.exit(1)

def main():
    # Set up command line arguments
    parser = argparse.ArgumentParser(description="Ork - Google Dork Search Tool")
    parser.add_argument("-d", "--dork", required=True, help="Specify the dork search query")
    parser.add_argument("-o", "--output", default="dorks-result.txt", help="Output file (default: dorks-result.txt)")
    parser.add_argument("-n", "--number", type=int, default=500, help="Number of results to display (default: 500)")

    args = parser.parse_args()

    # Perform the search
    perform_search(args.dork, args.number, args.output)

if __name__ == "__main__":
    # Print a small header
    print_colored("\n=== Ork - Google Dork Search Tool ===\n", Colors.BOLD + Colors.BLUE)
    main()