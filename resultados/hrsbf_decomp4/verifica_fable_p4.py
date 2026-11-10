import numpy as np, itertools, sys
sys.stdout.reconfigure(encoding="utf-8")
# todas as 2^16 funções em 4 variáveis: Walsh ≡ ±1 (mod 3) em todo u  =>  bent  ou  afim + delta_a ?
F = ((np.arange(1 << 16)[:, None] >> np.arange(16)[None, :]) & 1).astype(np.int64)
a = 1 - 2 * F; h = 1
while h < 16:
    a = a.reshape(a.shape[0], -1, 2, h); x = a[:, :, 0, :].copy(); y = a[:, :, 1, :]
    a[:, :, 0, :] = x + y; a[:, :, 1, :] = x - y; a = a.reshape(a.shape[0], 16); h *= 2
ok = np.all(np.mod(a, 3) != 0, axis=1)
bent = np.all(np.abs(a) == 4, axis=1)
pad = np.sort(np.abs(a), axis=1)
quase = np.all(pad[:, :15] == 2, axis=1) & (pad[:, 15] == 14)
print("funções com W ≢ 0 mod 3 em todo u:", int(ok.sum()), "| bent:", int((ok & bent).sum()), "| afim+delta (15×2, 1×14):", int((ok & quase).sum()), "| outras:", int((ok & ~bent & ~quase).sum()))
# RS em 4 variáveis: g(0)+g(1) em cada caso
rot = lambda v: ((v << 1) | (v >> 3)) & 15
rs = np.array([all(F[i, rot(v)] == F[i, v] for v in range(16)) for i in range(1 << 16)])
for nome, m in (("bent", ok & bent & rs), ("afim+delta", ok & quase & rs)):
    idx = np.nonzero(m)[0]
    print(f"RS {nome}: {len(idx)}; g(0)+g(1) =", sorted(set(int(F[i, 0] ^ F[i, 15]) for i in idx)))
