# Switch

An immersive, local-first studio for preparing your next engineering role.

**[Open the study app](https://23anish.github.io/Switch/)** · **[Download for macOS](https://github.com/23Anish/Switch/releases)**

## What is inside

- 250 original DSA practice problems, grouped by topic and progression, with Easy/Medium/Hard difficulty.
- Clear input/output contracts, constraints, worked examples, baseline and improved approaches, complexity notes, and C++17/Python 3 reference solutions.
- A coding workspace with saved drafts, named argument fields, optional raw JSON input, and included practice tests. C++ is the default language.
- An interactive BFS learning canvas, collapsible topic sheet, searchable problem table, sorting, and bookmarks.
- 24 executable worked theory examples with walkthroughs, diagrams, expected output, and follow-up exercises.
- Six interactive theory traces: CPU/I/O overlap, cumulative TCP ACKs, guarded inventory updates, TTL/LRU, token buckets, and permission-aware RAG.
- Core CS: operating systems, networks, databases, OOP/C++, and distributed systems.
- Separate low-level and high-level design case studies with theory, diagrams, interview questions, and labs.
- Modern AI: transformers, embeddings, RAG, agents, OpenAI, Claude, Gemini, MCP, hooks, skills, evaluations, quantization, and inference.
- Google, Microsoft, and NVIDIA preparation tracks, with dated official guidance and clearly labeled reported pilots.
- An Interview studio for code comprehension, debugging, patch validation, and explicit tool-policy checks.
- 45 guided patterns with searchable categories, play/pause/replay and step controls, state snapshots, invariants, complexity, and linked C++/Python practice: arrays, trees, tries, graphs, shortest paths, DSU, backtracking, DP, and strings.
- A 12-week roadmap, a mock timer, notes, spaced revision, and separate learner profiles.
- Ten light and dark themes: Sage, Paper, Midnight, Graphite, Ocean, Forest, Lavender, Rose, Sand, and Solarized. Progress and theme preferences stay on your device; JSON export/import moves them between devices.

## Choose how to use it

| Capability | Website / browser | Mac app |
| --- | --- | --- |
| Curriculum, solutions, themes, saved notes | Yes | Yes, bundled offline |
| JavaScript practice runner | Yes | Yes |
| C++ and Python practice runner | Edit/view only | Yes, using installed local tools |
| Account or API subscription | Not needed | Not needed |

The browser app caches its content after an initial HTTPS visit. External reading links still need the internet. Browser storage can be cleared by the browser; export a backup periodically. The Mac app and each browser keep separate progress until you transfer a backup.

## Install on Mac

1. Download `Switch-macOS.zip` from Releases and unzip it.
2. Drag `Switch.app` to Applications and open it.
3. If macOS blocks the app, review it in **System Settings → Privacy & Security → Open Anyway**. This personal build is ad-hoc signed, not Apple notarized.
4. For C++ execution, install Apple’s Command Line Tools (`xcode-select --install`). For Python, install Python 3 from [python.org](https://www.python.org/downloads/macos/) or your preferred package manager. JavaScript needs neither.

The universal app supports Apple Silicon and Intel Macs with macOS 12 or newer. All runner dependencies are bundled, so there are no runtime downloads.

**Local execution:** the Mac app runs the code you explicitly submit as your user account. Time and output limits prevent common accidental runaway programs, but this is not an OS security sandbox. Run only code you trust. The app does not send your code to an external judge.

## Coding contract

C++ starters and solutions are standard C++17 functions with typed parameters and return values, such as `int largestElement(const vector<int>& nums)`. Each snippet includes its own standard-library headers. Linked-list and tree exercises include `ListNode` and `TreeNode` definitions. Implement the function shown in the starter; the app supplies test calls, so no `main` is needed. You can also copy a solution into an ordinary C++ program and call it from your own `main`.

Problem examples use named test fields, with tree, list, and matrix diagrams where useful. The test panel offers argument fields and an optional JSON view. The Mac runner converts them to the function's C++ types behind the scenes, including trees, linked lists, optional values, and structured results. JSON is not part of the C++ code you write. Python uses `solve(input)` and can import standard-library modules. Output ordering follows each problem's contract. Included tests are practice checks, not an exhaustive judge.

**Upgrading from 2.0:** install Switch 2.1 or newer for the typed C++ runner. Earlier C++ drafts remain available under **Previous C++ draft** beneath the editor. New typed drafts are saved separately. Notes, completion, Python drafts, and profiles keep their existing keys.

For contributors, `dsa.json` stores each problem's typed starter, solution, signature, and private input/output adapter. `scripts/build-data.py` generates the browser curriculum without adapter code and packages the adapter map for the native runner. Generated bundles are not committed.

## Run or build from source

The web app has no package manager or build dependency:

```sh
python3 scripts/build-data.py
python3 -m http.server 8765 --bind 127.0.0.1 --directory web
```

Open `http://127.0.0.1:8765`. You can also open `web/index.html` directly; browser file-storage behavior varies. Build the Mac app on macOS with Xcode Command Line Tools:

```sh
bash scripts/build-mac.sh
```

The result is `dist/Switch-macOS.zip`. Rebuild after changing the source or curriculum.

## Verify content

```sh
node scripts/check-javascript.js
node scripts/check-workspace.js
node scripts/check-inputs.js
node scripts/check-immersive.js
python3 scripts/check-studio.py
python3 scripts/check-theory.py
python3 scripts/check-content.py
```

The Python check executes every Python reference, checks all C++ starters and solutions as standalone standard C++17, verifies starter compatibility with the adapters, and executes every C++ reference against the included tests. A C++17 compiler named `clang++` is required. The tests validate examples and selected boundaries; they do not prove every algorithm correct for every valid input.

## Contributing

Edit `dsa.json`, `lessons.json`, `design-lessons.json`, `companies.json`, `patterns.json`, `interviews.json`, or `learning-traces.json`, then rebuild the bundled data. Keep problem IDs stable so saved progress survives updates. Add boundary tests with independently reasoned expected results when changing solutions. Company practice tracks are recommendations, not question-frequency claims or confidential interview material. AI documentation changes; use the linked official sources and keep review dates accurate.

The curriculum is original, with [Take U Forward](https://takeuforward.org/prep-hub) as a reference for topic-based preparation. No TUF premium content is copied. External resources and company names belong to their respective owners; this app is not affiliated with them.

## Scope

This is a study companion, not a complete textbook, live AI tutor, cloud compiler, or guarantee of hiring success. Solution notes cover principal approaches, not every possible implementation. The AI track prioritizes durable theory and engineering decisions, with dated official documentation links rather than claims to cover every newly released product.

## License

MIT for the app and original curriculum. The bundled nlohmann JSON library is MIT licensed; its notice is preserved in `native/include/json.hpp` and `THIRD_PARTY_NOTICES.md`.
