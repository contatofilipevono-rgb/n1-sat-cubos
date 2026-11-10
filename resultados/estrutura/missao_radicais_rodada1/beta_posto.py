"""Exact rank-ten check on N, with an optional pair-rank test on sampled a."""
import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

from radical_grau8 import xor_selected, xor_space


def matrices(anf, beta):
    basis = [anf(1 << i) for i in range(40)]
    m = [[0] * 40 for _ in range(10)]
    for i, j in combinations(range(40), 2):
        for k, v in enumerate(beta(basis[i], basis[j])):
            m[k][i] |= v << j
            m[k][j] |= v << i
    return m


def all_forms(m):
    packed = [sum(v << (40 * j) for j, v in enumerate(row)) for row in m]
    for code in range(1, 1024):
        q = xor_selected(packed, code)
        yield code, [(q >> (40 * j)) & ((1 << 40) - 1) for j in range(40)]


def exact_single(forms, f40, kernel, em_n):
    histogram = Counter()
    cover = {}
    small = set()
    rank24 = set()
    for code, form in forms:
        basis = kernel(form, 40)
        histogram[len(basis)] += 1
        if len(basis) == 16:
            rank24.add(code)
            valid = np.ones(len(f40), dtype=bool)
            for v in basis:
                valid &= np.all(np.bitwise_count(f40 & np.uint64(v)) % 2 == 0, axis=1)
            assert valid.any()
            cover[code] = int(np.flatnonzero(valid)[0])
        else:
            assert len(basis) == 8
            small.update(xor_space(basis))
    words = np.array(sorted(small), dtype=np.uint64)
    for i in range(0, len(words), 4096):
        assert not em_n(words[i:i + 4096]).any()
    rank24.add(0)
    return {'radical_dimensions': dict(histogram), 'rank24_forms_with_one_covering_U': cover,
            'distinct_vectors_in_small_radicals': len(words),
            'rank24_and_zero_form_a_subspace': all(a ^ b in rank24 for a in rank24 for b in rank24)}


def pair_rank(a, m, forms, kernel, em_n):
    image = [xor_selected(b, a) for b in m]
    beta_rows = [sum(((x >> j) & 1) << (40 + i) for i, x in enumerate(image)) for j in range(40)]
    mask = (1 << 40) - 1
    possible = {}
    for mu, form in forms:
        cols = [x | y for x, y in zip(form, beta_rows)] + image
        space = kernel(cols, 50)
        for word in xor_space(space):
            b = word & mask
            if b not in (0, a):
                possible.setdefault(b, [word >> 40, mu])
    v = np.array(list(possible), dtype=np.uint64)
    v = v[em_n(v)]
    v = v[em_n(v ^ np.uint64(a))]
    return {'a': a, 'b_candidates_with_rank_deficiency': len(possible),
            'pairs_in_N': [{'b': int(b), 'lambda_mu': possible[int(b)]} for b in v]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('source', type=Path)
    p.add_argument('output', type=Path)
    p.add_argument('--sampled-first-cubics', type=int, default=16)
    p.add_argument('--seed', type=int, default=1732)
    a = p.parse_args()
    sys.path.insert(0, str(a.source.resolve()))
    from gama_dirigido import amostra_N, nucleo_int
    from sete_beta import F40, anf, beta, em_N
    m = matrices(anf, beta)
    forms = list(all_forms(m))
    single = exact_single(forms, F40, nucleo_int, em_N)
    print({k: v for k, v in single.items() if 'covering' not in k}, flush=True)
    rng = np.random.default_rng(a.seed)
    sampled = []
    for _ in range(a.sampled_first_cubics):
        x = amostra_N(rng, lambda: int(rng.integers(1, 1 << 40, dtype=np.uint64)))
        result = pair_rank(x, m, forms, nucleo_int, em_N)
        print(result, flush=True)
        sampled.append(result)
    sha = hashlib.sha256((a.source / 'base.npz').read_bytes()).hexdigest()
    a.output.write_text(json.dumps({'seed': a.seed, 'base_sha256': sha, 'single_rank': single,
                                   'sampled_pair_rank': sampled}, indent=2) + '\n')


if __name__ == '__main__':
    main()
