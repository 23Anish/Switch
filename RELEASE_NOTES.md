Switch 2.5 gives the learning workspace a floating layout inspired by the approved spatial design.

- A compact top menu replaces the permanent sidebar. Expand it to reach every study section and switch learner profiles; Escape closes it.
- Focus mode hides navigation with an always-available Show menu button to bring it back.
- All 20 light and dark themes now use their own gradient pair, floating panels, and coordinated controls. Code and reading surfaces stay clear and legible.
- The overview pairs a curved BFS teaching trace with your next unsolved problem, an unread lesson, and your real revision queue.
- Theme and focus changes preserve the editor, cursor, selection, and Undo history. Theme preferences continue to save on your device.
- The same layout extends across the problem set, coding studio, Pattern Lab, theory, design, company tracks, and Interview studio, with a responsive menu for phones and reduced-motion support.

The 250-problem curriculum, 2,006 submission cases, typed C++17/Python solutions, indentation support, and full-suite Submit behavior are retained. Existing profiles, progress, code drafts, notes, and bookmarks keep their storage keys.

[Open the website](https://23anish.github.io/Switch/).

Download **Switch-macOS.zip**, unzip it, and replace the previous **Switch.app** in Applications. Supports Apple Silicon and Intel on macOS 12+. This personal build is ad-hoc signed, not Apple notarized; if macOS blocks it, review the source and use System Settings → Privacy & Security → Open Anyway.

C++ execution requires Apple Command Line Tools; Python requires Python 3. JavaScript needs neither. Code runs locally on your Mac, so run only code you trust.

Validation includes navigation/focus/profile/theme regressions, all 20 palettes in the browser, phone layouts, existing editor/submission and learning-trace checks, curriculum validation, and native runner self-tests. These are practice checks, not an exhaustive judge.

The attached SHA256SUMS.txt records this package’s checksum. GitHub Actions builds it from this release’s public source.
