// Enumeracao exaustiva do espaco de pi (rotulos de 4 bits em 256 pontos de F2^8).
// Mantem os mapas em que toda fibra tem 16 pontos e o codigo C (constante + coordenadas) e auto-ortogonal,
// isto e, soma de y e de y_i y_j nula em cada fibra.  Saida: um codigo (inteiro) por linha.
// Uso: Enumera.exe gens_V2.bin saida.txt
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;

static class Enumera {
    static void Main(string[] a) {
        byte[] raw = File.ReadAllBytes(a[0]);
        int n = BitConverter.ToInt32(raw, 0);
        byte[][] G = new byte[n][];
        for (int j = 0; j < n; j++) { G[j] = new byte[256]; Array.Copy(raw, 4 + 256 * j, G[j], 0, 256); }
        ulong[] PP = new ulong[256];
        for (int y = 0; y < 256; y++) {
            ulong m = (ulong)y; int b = 8;
            for (int i = 0; i < 8; i++) for (int k = i + 1; k < 8; k++) { if (((y >> i) & 1) == 1 && ((y >> k) & 1) == 1) m |= 1UL << b; b++; }
            PP[y] = m;
        }
        int low = Math.Min(n, 18), high = n - low;
        long tot16 = 0, totSO = 0;
        object lk = new object();
        List<long> outp = new List<long>();
        Parallel.For(0L, 1L << high, hi => {
            byte[] lab = new byte[256];
            for (int j = 0; j < high; j++) if (((hi >> j) & 1) == 1) { byte[] g = G[low + j]; for (int y = 0; y < 256; y++) lab[y] ^= g[y]; }
            int[] cnt = new int[16]; ulong[] acc = new ulong[16];
            long c16 = 0, cso = 0; List<long> loc = new List<long>();
            long gray = 0;
            for (long it = 0; it < (1L << low); it++) {
                if (it > 0) {
                    int j = 0; long t = it; while ((t & 1) == 0) { t >>= 1; j++; }
                    gray ^= 1L << j; byte[] g = G[j];
                    for (int y = 0; y < 256; y++) lab[y] ^= g[y];
                }
                for (int l = 0; l < 16; l++) { cnt[l] = 0; acc[l] = 0; }
                for (int y = 0; y < 256; y++) { int l = lab[y]; cnt[l]++; acc[l] ^= PP[y]; }
                bool ok = true;
                for (int l = 0; l < 16; l++) if (cnt[l] != 16) { ok = false; break; }
                if (!ok) continue;
                c16++;
                for (int l = 0; l < 16; l++) if (acc[l] != 0) { ok = false; break; }
                if (!ok) continue;
                cso++; loc.Add(gray | (hi << low));
            }
            lock (lk) { tot16 += c16; totSO += cso; outp.AddRange(loc); }
        });
        outp.Sort();
        using (StreamWriter w = new StreamWriter(a[1])) foreach (long c in outp) w.WriteLine(c);
        Console.WriteLine("geradores: " + n + "; mapas percorridos: 2^" + n + "; fibras de 16 pontos: " + tot16 + "; auto-ortogonais: " + totSO);
    }
}
