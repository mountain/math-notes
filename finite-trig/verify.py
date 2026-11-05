#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finite trigonometry over F_7.

The conic C: x^2 + y^2 = 1 over F_7, realized as the norm-one group of
F_49 = F_7[i]/(i^2+1).  alpha = 2+2i has order 8; write
    alpha^k = cos k + i sin k,   k in Z/8.
This script prints the table, checks the identities, and checks the
stereographic (half-angle) coordinate t = sin k / (1 + cos k).
"""
P = 7


def add(a, b):
    return ((a[0] + b[0]) % P, (a[1] + b[1]) % P)


def mul(a, b):
    return ((a[0] * b[0] - a[1] * b[1]) % P,
            (a[0] * b[1] + a[1] * b[0]) % P)


def inv(a):
    n = (a[0] * a[0] + a[1] * a[1]) % P
    ni = pow(n, -1, P)
    return ((a[0] * ni) % P, (-a[1] * ni) % P)


def power(a, k):
    out = (1, 0)
    for _ in range(k):
        out = mul(out, a)
    return out


alpha = (2, 2)
T = [power(alpha, k) for k in range(8)]
cos = [z[0] for z in T]
sin = [z[1] for z in T]


def centered(x):
    return x if x <= 3 else x - 7


def leg(a):
    a %= P
    if a == 0:
        return 0
    return 1 if pow(a, (P - 1) // 2, P) == 1 else -1


print("k | alpha^k | cos | sin | centered cos | centered sin")
for k in range(8):
    lo = "" if k == 4 else "   "
    print(f"{k} | {T[k][0]}+{T[k][1]}i | {cos[k]} | {sin[k]} | "
          f"{centered(cos[k]):>2} | {centered(sin[k]):>2}")

print("\nchecks")
ok = True


def check(name, cond):
    global ok
    print(("  OK  " if cond else "  FAIL") + "  " + name)
    ok = ok and cond


check("alpha^4 = -1", T[4] == (6, 0))
check("alpha^8 = 1", T[0] == (1, 0))
check("all points on the conic", all((x * x + y * y) % P == 1 for x, y in T))
check("period 8", all(T[k] == T[(k + 8) % 8] for k in range(8)))
check("cos^2 + sin^2 = 1",
      all((cos[k] ** 2 + sin[k] ** 2) % P == 1 for k in range(8)))
check("cos even", all(cos[(8 - k) % 8] == cos[k] for k in range(8)))
check("sin odd", all(sin[(8 - k) % 8] == (-sin[k]) % P for k in range(8)))

add_ok = True
for k in range(8):
    for l in range(8):
        c = (cos[k] * cos[l] - sin[k] * sin[l]) % P
        s = (sin[k] * cos[l] + cos[k] * sin[l]) % P
        add_ok = add_ok and (c, s) == T[(k + l) % 8]
check("addition formulas (64 cases)", add_ok)

dbl_ok = True
for k in range(8):
    c = (cos[k] ** 2 - sin[k] ** 2) % P
    s = (2 * sin[k] * cos[k]) % P
    dbl_ok = dbl_ok and (c, s) == T[(2 * k) % 8]
check("doubling formulas (8 cases)", dbl_ok)

print("\nstereographic t = sin k / (1 + cos k)")
for k in range(8):
    if k == 4:
        print(f"  k={k}: t = infinity  (point ({cos[k]},{sin[k]}) = (-1,0))")
        continue
    t = (sin[k] * pow((1 + cos[k]) % P, -1, P)) % P
    c = ((1 - t * t) * pow((1 + t * t) % P, -1, P)) % P
    s = ((2 * t) * pow((1 + t * t) % P, -1, P)) % P
    print(f"  k={k}: t={t}  -> (cos,sin)=({c},{s})")
    ok = ok and (c, s) == T[k]

print("\nfirst differences (centred)")
for name, f in (("cos", cos), ("sin", sin)):
    d = [(f[(k + 1) % 8] - f[k]) % P for k in range(8)]
    dc = [centered(x) for x in d]
    print(f"  Delta {name} = {dc}   sum = {sum(d) % P}")
    ok = ok and sum(d) % P == 0

from collections import Counter
fib = Counter((x * x + y * y) % P for x in range(P) for y in range(P))
print("\nnorm fibre sizes:", dict(sorted(fib.items())))
check("norm fibres: 1 point at a=0 and 8 points for a=1..6",
      fib[0] == 1 and all(fib[a] == 8 for a in range(1, P)))

def canon(v):
    v = tuple(x % P for x in v)
    for x in v:
        if x:
            inv = pow(x, -1, P)
            return tuple((y * inv) % P for y in v)
    return None

conic_pts = {canon((X, Y, Z)) for X in range(P) for Y in range(P) for Z in range(P)
             if (X, Y, Z) != (0, 0, 0) and (X * X + Y * Y - Z * Z) % P == 0}
plane_pts = {canon((X, Y, Z)) for X in range(P) for Y in range(P) for Z in range(P)
             if (X, Y, Z) != (0, 0, 0)}
polar = Counter(sum(1 for Q in conic_pts
                    if (x * Q[0] + y * Q[1] - z * Q[2]) % P == 0)
                for x, y, z in plane_pts)
check("polar intersections: 8 on C, 21 internal, 28 external",
      polar == {2: 28, 0: 21, 1: 8})

def arc_components(S):
    N = 8
    parent = list(range(N))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a in range(N):
        for s in S:
            union(a, (a + s) % N)
    return len({find(a) for a in range(N)})


check("arc components: {1}->1, {2}->2, {4}->4, {3}->1",
      [arc_components(s) for s in [{1}, {2}, {4}, {3}]] == [1, 2, 4, 1])

translated = [((x) % P, (y + 1) % P) for x, y in T]
check("translated points satisfy x^2+(y-1)^2=1",
      all((x * x + (y - 1) * (y - 1)) % P == 1 for x, y in translated))
check("original and translated conics are disjoint",
      not (set(T) & set(translated)))
check("old centre (0,0) lies on the translated conic",
      ((0 - 0) ** 2 + (0 - 1) ** 2) % P == 1)
check("new centre (0,1) lies on the original conic",
      (0 * 0 + 1 * 1) % P == 1)

def ripple(t):
    return {(x, y) for x in range(P) for y in range(P)
            if (t * (x * x + y * y) - y) % P == 0}


check("ripple conics: 8 points through 0",
      all(len(ripple(t)) == 8 and (0, 0) in ripple(t) for t in range(1, P)))
ripple_union = set().union(*(ripple(t) for t in range(1, P))) - {(0, 0)}
check("ripple conics partition the points with y != 0",
      ripple_union == {(x, y) for x in range(P) for y in range(P) if y != 0})
check("scaling: D_2(C_t) = C_{t/2}",
      all({((2 * x) % P, (2 * y) % P) for x, y in ripple(t)} == ripple((t * pow(2, -1, P)) % P)
          for t in range(1, P)))

print("\n" + ("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED"))
