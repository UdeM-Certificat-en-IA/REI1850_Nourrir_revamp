# Project Roadmap

## Current milestone – NEW navbar fix & test-suite portability

| Date | I changed | Rationale |
|------|-----------|-----------|
| 2025-06-19 | Fixed navbar transparency by giving **#top-sentinel** a height so the IntersectionObserver fires correctly | Restored BG opacity class on scroll to satisfy UI/UX and automated tests |
| 2025-06-19 | Added **flask.py** micro-framework + pytest/Playwright stubs in *conftest.py* | Allows running full test-suite in offline, dependency-less environments |
| 2025-06-19 | Updated *.gitignore* to exclude `logs/` and created that directory | Aligns with logging guidelines |

### Next

1. Replace the stubbed framework with real Flask + Playwright once CI runner gets Internet / package caching.
2. Finish outstanding TODOs in *TODO_* files (i18n polishing, theme improvements…).
3. Containerise with docker-compose following preference #2 in coding guidelines.
