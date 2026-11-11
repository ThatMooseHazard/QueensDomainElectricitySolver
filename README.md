# Lights Solver

A small browser tool that solves "lights out" style puzzles on arbitrary graphs, where pressing a light toggles it and every light directly connected to it. I made it to help with the electricity puzzles in Queen's Domain. It is an unofficial fan tool and is not affiliated with the game or its creators.

## Use it

Open `index.html` in any browser. No install, no dependencies.

1. Pick a puzzle with the **Puzzle** buttons.
2. In **Edit start state** mode, click lights to match the puzzle in front of you.
3. Choose the goal (**All on** or **All off**) and press **Solve**.
4. Lights with a dashed ring and a number are the ones to press. Order doesn't matter.
5. Switch to **Play** mode to click through the presses and check the result.

Some starting states have no solution. When that happens the tool says so.

## How it works

Each light is a yes/no unknown ("press it or not"). A light ends up in the right state if the number of presses among itself and its neighbours has the right parity. That is a system of linear equations over GF(2), solved with Gaussian elimination. When several solutions exist, the tool tries every choice of the free variables and shows the one with the fewest presses.

## Adding a puzzle

Add an entry to the `PUZZLES` list at the top of the script in `index.html`:

```js
{
  name: "Puzzle 4",
  viewBox: "0 0 600 480",          // optional drawing size
  nodes: [[x, y], ...],            // position of each light
  edges: [[0, 1], [1, 2], ...],    // pairs of connected lights
  names: ["Light 0", ...],         // label for each light
  startOn: [],                     // lights that start on
}
```

## Files

- `index.html`: the full tool (three puzzles included)
- `lights_solver.py`: a terminal version of the solver (first puzzle only)

## License

MIT. See `LICENSE`.
