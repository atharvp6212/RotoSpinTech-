"""Benchmark multi-level BOM expansion without database overhead."""

import argparse
import csv
import sys
import time
import tracemalloc
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inventory.research_algorithms import explode_bom


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--depths', nargs='+', type=int, default=[10, 100, 1000])
    parser.add_argument('--output', default='bom_results.csv')
    args = parser.parse_args()
    rows = []
    for depth in args.depths:
        edges = [(f'part-{index}', f'part-{index + 1}', 1.1) for index in range(depth)]
        tracemalloc.start()
        started = time.perf_counter()
        result = explode_bom('part-0', 1, edges)
        elapsed = time.perf_counter() - started
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        rows.append((depth, elapsed, peak, next(iter(result.values()))))
    with open(args.output, 'w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(('depth', 'seconds', 'peak_bytes', 'leaf_demand'))
        writer.writerows(rows)


if __name__ == '__main__':
    main()
