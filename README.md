# Switch

A quiet, local-first studio for preparing your next engineering role.

**[Open the study app](https://23anish.github.io/Switch/)** · **[Download for macOS](https://github.com/23Anish/Switch/releases)**

## What is inside

- 250 original DSA practice problems, grouped by topic and progression, with Easy/Medium/Hard difficulty.
- Clear input/output contracts, constraints, worked examples, baseline and improved approaches, complexity notes, and C++17/Python 3 reference solutions.
- A coding workspace with saved drafts, custom inputs, and included practice tests. C++ is the default language.
- Core CS: operating systems, networks, databases, OOP/C++, and distributed systems.
- Separate low-level and high-level design case studies with theory, diagrams, interview questions, and labs.
- Modern AI: transformers, embeddings, RAG, agents, OpenAI, Claude, Gemini, MCP, hooks, skills, evaluations, quantization, and inference.
- Google and Microsoft preparation tracks grounded in official interview guidance.
- Step-through pattern diagrams, a 12-week roadmap, a mock timer, notes, spaced revision, and separate learner profiles.
- Sage, Paper, and Midnight themes. Progress and theme preferences stay on your device; JSON export/import moves them between devices.

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

The universal app supports Apple Silicon and Intel Macs with macOS 12 or newer. The included C++ JSON library is bundled, so there are no runtime downloads.

**Local execution:** the Mac app runs the code you explicitly submit as your user account. Time and output limits prevent common accidental runaway programs, but this is not an OS security sandbox. Run only code you trust. The app does not send your code to an external judge.

## Coding contract

C++ reference code implements `json solve(const json& input)`. The runner supplies standard headers, `using namespace std`, the nlohmann `json` type, and a main function. Python implements `solve(input)` and can import standard-library modules. Inputs and outputs follow each problem’s JSON contract, including any required order of arrays. Tests are practice checks, not an exhaustive judge.

For a standalone C++ program, include `native/include/switch_runtime.hpp`, paste the function, then add `native/include/harness.cpp`. The harness reads an array of `{ "input": ..., "expected": ... }` test cases from standard input. Omit `expected` for a custom-output run. The Python harness works the same way.

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
python3 scripts/check-content.py
```

The Python check executes every Python reference and compiles/executes every C++ reference against the included tests. A C++17 compiler named `clang++` is required. The tests validate examples and selected boundaries; they do not prove every algorithm correct for every valid input.

## Contributing

Edit `dsa.json`, `lessons.json`, `design-lessons.json`, or `companies.json`, then rebuild the bundled data. Keep problem IDs stable so saved progress survives updates. Add boundary tests with independently reasoned expected results when changing solutions. Company practice tracks are recommendations, not question-frequency claims or confidential interview material. AI documentation changes; use the linked official sources and keep review dates accurate.

The curriculum is original, with [Take U Forward](https://takeuforward.org/prep-hub) as a reference for topic-based preparation. No TUF premium content is copied. External resources and company names belong to their respective owners; this app is not affiliated with them.

## Scope

This is a study companion, not a complete textbook, live AI tutor, cloud compiler, or guarantee of hiring success. Solution notes cover principal approaches, not every possible implementation. The AI track prioritizes durable theory and engineering decisions, with dated official documentation links rather than claims to cover every newly released product.

## License

MIT for the app and original curriculum. The bundled nlohmann JSON library is MIT licensed; its notice is preserved in `native/include/json.hpp` and `THIRD_PARTY_NOTICES.md`.
