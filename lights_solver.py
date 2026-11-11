#!/usr/bin/env python3
"""Lights-Out-on-a-graph solver (GF(2) linear algebra).

Pressing a light toggles itself and every light directly connected to it.
Edit the starting state interactively, then solve for "all on" (or "all off").
"""
from itertools import product

# ---- The graph from the drawing -------------------------------------------
NAMES = [
    "Top-left antenna",        # 0
    "Top-right antenna",       # 1
    "Row 1 (left end)",        # 2
    "Row 2",                   # 3
    "Row 3 (middle)",          # 4
    "Row 4",                   # 5
    "Row 5 (right end)",       # 6
    "Left side 1 (oval)",      # 7
    "Left side 2",             # 8
    "Triangle left",           # 9
    "Right side 1",            # 10
    "Triangle right",          # 11
    "Triangle bottom",         # 12
]
EDGES = [
    (0, 2), (1, 6),                      # antennas
    (2, 3), (3, 4), (4, 5), (5, 6),      # horizontal row
    (2, 7), (7, 8), (8, 9),              # left side down to triangle
    (6, 10), (10, 11),                   # right side down to triangle
    (9, 11), (9, 12), (11, 12),          # triangle
]
N = len(NAMES)

# Starting state: True = on. Edit here, or interactively when you run it.
state = [False] * N
for i in (0, 1, 2, 4, 6):
    state[i] = True

# ---- Solver ----------------------------------------------------------------
def neighbours():
    nb = [{i} for i in range(N)]          # a press affects itself...
    for a, b in EDGES:                    # ...and its direct neighbours
        nb[a].add(b)
        nb[b].add(a)
    return nb

def solve(start, goal_on=True):
    """Return the smallest list of lights to press, or None if impossible."""
    nb = neighbours()
    # Light i flips if odd number of presses among nb[i]. Need flip == start XOR goal.
    need = [(s != goal_on) for s in start]
    # Augmented matrix rows as bitmasks: bits 0..N-1 = unknown presses, bit N = rhs.
    rows = []
    for i in range(N):
        r = 0
        for j in nb[i]:
            r |= 1 << j
        if need[i]:
            r |= 1 << N
        rows.append(r)

    pivots, r = [], 0
    for col in range(N):
        p = next((k for k in range(r, N) if rows[k] >> col & 1), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for k in range(N):
            if k != r and rows[k] >> col & 1:
                rows[k] ^= rows[r]
        pivots.append(col)
        r += 1

    if any(rows[k] == 1 << N for k in range(r, N)):
        return None                        # inconsistent: unsolvable

    free = [c for c in range(N) if c not in pivots]
    best = None
    for vals in product((0, 1), repeat=len(free)):   # try every free-variable choice
        x = [0] * N
        for c, v in zip(free, vals):
            x[c] = v
        for k, c in enumerate(pivots):
            x[c] = (rows[k] >> N & 1) ^ (
                sum(x[f] for f in free if rows[k] >> f & 1) & 1)
        presses = [i for i in range(N) if x[i]]
        if best is None or len(presses) < len(best):
            best = presses
    return best

def simulate(start, presses):
    s = list(start)
    nb = neighbours()
    for p in presses:
        for j in nb[p]:
            s[j] = not s[j]
    return s

# ---- Interactive UI --------------------------------------------------------
def show(s):
    print()
    for i in range(N):
        print(f"  {i:>2}  [{'ON ' if s[i] else 'off'}]  {NAMES[i]}")

def main():
    global state
    goal_on = True
    print("Lights solver. Commands:")
    print("  <numbers>   toggle those lights in the starting state (e.g. '0 3 7')")
    print("  on / off    set the GOAL (all on / all off)   [default: all on]")
    print("  clear / all set every light off / on")
    print("  solve       find the presses      quit")
    while True:
        show(state)
        print(f"Goal: all {'ON' if goal_on else 'OFF'}")
        cmd = input("> ").strip().lower()
        if cmd in ("q", "quit", "exit"):
            break
        if cmd == "on":   goal_on = True
        elif cmd == "off": goal_on = False
        elif cmd == "clear": state = [False] * N
        elif cmd == "all":   state = [True] * N
        elif cmd in ("s", "solve"):
            sol = solve(state, goal_on)
            if sol is None:
                print("\nNo solution exists for this starting state.")
            elif not sol:
                print("\nAlready solved!")
            else:
                print(f"\nPress these {len(sol)} lights (any order):")
                for step, i in enumerate(sol, 1):
                    print(f"  {step}. {i}: {NAMES[i]}")
                assert all(v == goal_on for v in simulate(state, sol))
        else:
            try:
                for tok in cmd.split():
                    i = int(tok)
                    state[i] = not state[i]
            except (ValueError, IndexError):
                print("Didn't understand that.")

if __name__ == "__main__":
    main()
