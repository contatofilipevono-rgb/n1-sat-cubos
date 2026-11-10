"""Check the alternating-form reduction of the mixed degree-eight equations."""
import argparse
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np


def xor_selected(columns, mask):
    result = 0
    while mask:
        bit = mask & -mask
        result ^= columns[bit.bit_length() - 1]
        mask ^= bit
    return result


def xor_space(basis):
    values = [0]
    for row in basis:
        values += [x ^ row for x in values]
    return values


def complete_pair_space(a, b, anf, beta, kernel):
    pa, pb = anf(a), anf(b)
    columns = []
    for i in range(40):
        v = anf(1 << i)
        entries = beta(pa, v) + beta(pb, v)
        columns.append(sum(c << j for j, c in enumerate(entries)))
    return kernel(columns, 40)


def top_product(a, b, c, wedge):
    two = wedge(a, b)
    return sum((two >> (255 ^ v)) & 1 for v in c) % 2


def forms(a, b, basis, cub, anf, solutions, wedge, t):
    pa, pb = cub(anf(a)), cub(anf(b))
    a0, directions = solutions(pa, pb)
    assert a0 is not None
    cubics = [cub(anf(c)) for c in basis]
    lift_a = [solutions(pa, c)[0] for c in cubics]
    lift_b = [solutions(pb, c)[0] for c in cubics]
    n = len(basis)
    matrices = [[0] * n for _ in range(len(directions) + 1)]
    for i, j in combinations(range(n), 2):
        for k, q in enumerate([a0, *directions]):
            value = top_product(cubics[i], cubics[j], q, wedge)
            if k == 0:
                value ^= top_product(t, lift_a[j], lift_b[i], wedge)
                value ^= top_product(t, lift_b[j], lift_a[i], wedge)
            matrices[k][i] |= value << j
            matrices[k][j] |= value << i
    return matrices, a0, directions


def choose_pair(rng, sample, beta_basis, em_n):
    a = sample(rng, lambda: int(rng.integers(1, 1 << 40, dtype=np.uint64)))
    assert a is not None
    basis = beta_basis(a)
    for _ in range(400):
        candidates = np.zeros(8192, dtype=np.uint64)
        for v in basis:
            pick = rng.integers(0, 2, len(candidates), dtype=np.uint64)
            candidates ^= pick * np.uint64(v)
        candidates = candidates[em_n(candidates)]
        candidates = candidates[em_n(candidates ^ np.uint64(a))]
        if len(candidates):
            return a, int(candidates[0])
    raise RuntimeError('No compatible pair found within the sampling limit')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path, help='Directory with gama_dirigido.py and its data')
    p.add_argument('output', type=Path)
    p.add_argument('--pairs', type=int, default=8)
    p.add_argument('--seed', type=int, default=1517)
    p.add_argument('--rank-audit', type=Path, help='Use only rank-deficient pairs found by beta_posto.py')
    a = p.parse_args()
    sys.path.insert(0, str(a.source.resolve()))
    from gama_dirigido import amostra_N, base_nucleo_beta, espaco_phi3, nucleo_int, solucoes_A12
    from gama_massey import cub, wedge
    from sete_beta import T, anf, beta, em_N

    rng = np.random.default_rng(a.seed)
    results = []
    if a.rank_audit is None:
        pairs = [choose_pair(rng, amostra_N, base_nucleo_beta, em_N) for _ in range(a.pairs)]
    else:
        data = json.loads(a.rank_audit.read_text())['sampled_pair_rank']
        planes = {tuple(sorted((row['a'], hit['b'], row['a'] ^ hit['b'])))
                  for row in data for hit in row['pairs_in_N']}
        pairs = [(x, y) for x, y, _ in sorted(planes)]
    for x, y in pairs:
        basis = complete_pair_space(x, y, anf, beta, nucleo_int)
        matrices, a0, directions = forms(x, y, basis, cub, anf, solucoes_A12, wedge, T)
        d = len(basis)
        packed = [sum(v << (d * j) for j, v in enumerate(m)) for m in matrices]
        hist = Counter()
        checked = 0
        seen = set()
        hits = []
        high_nullity = []
        for choice in range(1 << len(directions)):
            matrix = packed[0] ^ xor_selected(packed[1:], choice)
            rows = [(matrix >> (d * j)) & ((1 << d) - 1) for j in range(d)]
            kernel = nucleo_int(rows, d)
            values = tuple(sorted(xor_selected(basis, v) for v in xor_space(kernel)))
            assert all(v in values for v in (0, x, y, x ^ y))
            hist[len(kernel)] += 1
            if choice % 64 == 0 or len(kernel) >= 7:
                particular = set(a0)
                for j, v in enumerate(directions):
                    if choice >> j & 1:
                        particular.symmetric_difference_update(v)
                original = espaco_phi3(cub(anf(x)), cub(anf(y)), sorted(particular))
                assert values == tuple(sorted(xor_space(original)))
                checked += 1
                if len(kernel) >= 7:
                    high_nullity.append({'A12_choice': choice, 'A12_supports': sorted(particular),
                                         'radical_dimension': len(kernel)})
            if values in seen:
                continue
            seen.add(values)
            tests = np.array(values, dtype=np.uint64)
            for shift in (0, x, y, x ^ y):
                tests = tests[em_N(tests ^ np.uint64(shift))]
            if len(tests):
                hits.append({'A12_choice': choice, 'third_vectors': [int(v) for v in tests]})
        result = {'a': x, 'b': y, 'dimension_C': d, 'radical_dimension_histogram': dict(hist),
                  'distinct_radicals': len(seen), 'cross_checks': checked,
                  'directly_verified_radicals_of_dimension_at_least_seven': high_nullity, 'hits': hits}
        results.append(result)
        print(result, flush=True)
    a.output.write_text(json.dumps({'seed': a.seed, 'pairs': results}, indent=2) + '\n')


if __name__ == '__main__':
    main()
