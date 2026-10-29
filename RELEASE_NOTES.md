Switch 2.3 makes the learning process visible: trace an algorithm, inspect its state, then solve the linked problem in ordinary C++17 or Python.

- The approved immersive learning design across the home, practice, lesson, and interview pages, with ten retained light/dark themes and reduced-motion support.
- A working BFS home canvas linking highlighted C++ lines, tree nodes, queue state, and visit order.
- 45 searchable Pattern Lab traces: DFS/BFS, tree traversals, tries, heaps, shortest paths, DSU, backtracking, greedy, DP, KMP, and more. Play, pause, step, scrub, or restart; each trace includes its invariant, complexity, assumptions, and linked practice.
- Clear named test contracts for all 250 problems, with tree/list/matrix diagrams, cycle and shared-tail conventions, and explicit graph indexing where relevant.
- Six interactive theory walkthroughs, alongside the existing 24 executable theory examples and 68 lessons.
- Updated Google and Microsoft tracks, a new NVIDIA track, and an Interview studio with original code-comprehension and patch-review exercises. Official policies and reported pilots are labeled separately and reviewed 29 October 2026.
- Existing learner profiles, drafts, completion, bookmarks, and notes retain their keys. C++ remains the default editor language.

[Open the website](https://23anish.github.io/Switch/).

Download **Switch-macOS.zip** below, unzip it, and replace the previous **Switch.app** in Applications. Supports Apple Silicon and Intel on macOS 12+. This build is ad-hoc signed, not Apple notarized; if macOS blocks it, review the source and use System Settings → Privacy & Security → Open Anyway.

C++ execution requires Apple Command Line Tools; Python requires Python 3. JavaScript works without additional tools. The website supports C++/Python editing and solutions; their execution runs locally in the Mac app. Run only code you trust.

Validation includes all 500 C++ starter/solution snippets, 506 cases per language in C++, Python, and JavaScript, 24 executable theory examples, named input round-trips, trace-state checks, playback cleanup, and the native runner smoke test. These cover examples and selected boundaries, not an exhaustive judge.

The attached SHA256SUMS.txt records this package’s checksum. GitHub Actions builds the package from the public release source.
