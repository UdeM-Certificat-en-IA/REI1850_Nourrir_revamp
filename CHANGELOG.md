## Changelog

### Unreleased
- Created `REVAMP` branch from `work` to continue UI/UX revamp tasks.
- Added responsive DaisyUI navbar with Tailwind and Alpine.js; active page now highlighted via context.
- Cleaned up `README.md` by removing shell prompt artifacts and adding missing license closing text.
- Added pytest fixture that freezes the site if `build/index.html` is missing; documented this under "Running Tests".
- Added pytest-based tests for key routes and documented how to run them.
- Added Netlify deployment files and documentation.
- Fixed trailing prompt artifact in `test.py`.
- Integrated performance policy pages and routes.
- Fixed Netlify configuration parse error by using `python_version` in `netlify.toml`.
- Removed fixed header/nav offsets; navbar now uses `sticky top-0` and body padding was dropped in favor of Tailwind spacing.
- Updated Netlify configuration to remove unsupported `python_version` property.
- Fixed functions directory path so Netlify deploy detects Python functions.
- Added base path stripping and included files to ensure Flask routes work on Netlify.
- Made Flask server port configurable via `PORT` env variable and updated Dockerfile.
- Read serverless function base path from `API_GATEWAY_BASE_PATH` environment
  variable and documented the setting in Netlify configuration.
- Replaced Python 3.10 union type hints with `typing.Optional` for
  compatibility with Netlify's Python runtime.
- Updated Netlify redirect to include `:splat` so route paths reach the Flask
  function correctly.
- Added Alpine.js theme state and navbar toggle; preferences persist via `localStorage`.
- Set `publish = "templates"` in Netlify configuration so deploys upload the site's HTML files.
- Switched Netlify deploy to Frozen-Flask static build with `freeze.py` and new workflow.
- Fixed failing route tests by adjusting `tests/test_routes.py` to load the
  local module explicitly.
- Added new unit tests covering the `/models` API and performance policy pages.
- Replaced legacy performance policy with new policy structure and HTML sections.
- Ensured Frozen-Flask outputs `.html` files for performance policy subpages.
- Switched page logo to backgroundless variant.
- Added dropdown navigation and arrow-style back buttons on performance policy pages.
- Embedded policy explanation video at the top of the performance index page.
- Fixed integration policy page by serving it at `/politique/` and redirecting the legacy path.
- Added direct section links at the bottom of the performance index page and ensured dropdowns toggle via JavaScript.
- Expanded route tests to cover all pages and updated politique path tests.
- Added circular stage buttons on the performance index page with links to each phase and new route tests.
- Added unit tests for Ollama query logic and fallback handling.
- Fixed duplicate Docker build/run commands in README.
- Implemented basic internationalization with i18next, French/English locale files, and a navbar language switcher.
- Reworked layout using Tailwind sections and DaisyUI cards; removed redundant CSS and improved image alt text.
- Integrated Tippy.js tooltips for glossary terms (dopamine, probiotiques, freemium, NurrIA) with theme-aware initialization and i18n support. Added tooltip translations in locale files.
- Animated header fades out on scroll and mobile menu now transitions smoothly.
- Navbar now shrinks on scroll and logo slides to the left for a cleaner sticky header.
- Logo now physically moves from the header into the navbar on scroll, and menu buttons use consistent DaisyUI styles with a working dark-mode toggle.
