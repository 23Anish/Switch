Switch 2.4 adds more personality and makes the coding loop smoother: write, test, submit, and save your progress.

- 20 themes in total: the original ten plus Retro Terminal, Pokémon, Naruto, One Piece, Spider-Man, Superman, Neon Pop, Cyberpunk, Arcade, and Candy Pop. New palettes use original UI styling, with brief pop animations and reduced-motion support.
- `#include <bits/stdc++.h>` now works in the Mac C++17 runner through a bundled compatibility header. GNU-only extensions are not added.
- Enter preserves indentation; opening braces and Python blocks indent the next line. Paired braces, closing-brace indentation, and multiline Tab/Shift+Tab are supported.
- 2,006 test cases across all 250 problems, with at least eight per problem. Existing sample cases remain available separately from the full submission suite.
- Submit checks every case, records acceptance for the correct learner, marks the problem complete, and schedules revision. Failed, incomplete, or stale-code submissions do not mark a problem complete. Sample and custom runs never auto-complete a problem.
- The native runner reports structured per-case results separately from debug output. C++/Python Submit requires this Mac release; JavaScript Submit also works on the website.
- Existing profiles, code drafts, notes, bookmarks, and completion keys are retained.

[Open the website](https://23anish.github.io/Switch/).

Download **Switch-macOS.zip**, unzip it, and replace the previous **Switch.app** in Applications. Supports Apple Silicon and Intel on macOS 12+. This personal build is ad-hoc signed, not Apple notarized; if macOS blocks it, review the source and use System Settings → Privacy & Security → Open Anyway.

C++ execution requires Apple Command Line Tools; Python requires Python 3. JavaScript needs neither. Code runs locally on your Mac, so run only code you trust.

Validation covers 500 standalone C++ starter/solution snippets, all 2,006 cases in C++/Python/JavaScript, editor indentation and submission regressions, native header compatibility, structured results, compile failures, early exits, and debug-output handling. These are practice checks, not an exhaustive judge.

The attached SHA256SUMS.txt records this package’s checksum. GitHub Actions builds it from this release’s public source.
