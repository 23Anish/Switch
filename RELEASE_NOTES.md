Switch 2.2 rebuilds the study experience and fixes the C++ workspace across all 250 problems.

- A new landing page, topic progress sheet, searchable problem table, sorting, and bookmarks.
- Ten light and dark themes, plus named argument fields for custom tests.
- 24 executable worked examples across core CS, LLD, HLD, and AI, with diagrams and follow-up exercises.
- Ordinary C++17 starters and solutions with typed parameters, standard containers, and `TreeNode` / `ListNode` where appropriate.
- Readable reference code that can be loaded directly into the editor. Input conversion stays inside the Mac test runner.
- Previous C++ drafts preserved separately; notes, completion, profiles, and Python drafts retained.
- C++ remains the default language. Python and JavaScript practice remain available.

[Open the website](https://23anish.github.io/Switch/).

Download **Switch-macOS.zip** below, unzip it, and replace the previous **Switch.app** in Applications. Supports Apple Silicon and Intel on macOS 12+. This build is ad-hoc signed, not Apple notarized; if macOS blocks it, review the source and use System Settings → Privacy & Security → Open Anyway.

C++ execution requires Apple Command Line Tools; Python requires Python 3. JavaScript works without additional tools. The website supports C++/Python editing and solutions; their execution runs locally in the Mac app. Run only code you trust.

Validation includes all 500 C++ starter/solution snippets, starter compatibility with the runner, and 506 cases per language in C++, Python, and JavaScript. The native runner is also checked with representative typed problems. These cover examples and selected boundaries, not an exhaustive judge.

The attached SHA256SUMS.txt records the checksum of this package. The Mac package is built from this release's source by the repository's visible GitHub Actions workflow.
