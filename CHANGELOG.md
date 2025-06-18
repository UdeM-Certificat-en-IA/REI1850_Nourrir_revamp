## Changelog

### Unreleased
- Cleaned up `README.md` by removing shell prompt artifacts and adding missing license closing text.
- Added pytest-based tests for key routes and documented how to run them.
- Added Netlify deployment files and documentation.
- Fixed trailing prompt artifact in `test.py`.
- Integrated performance policy pages and routes.
- Fixed Netlify configuration parse error by using `python_version` in `netlify.toml`.
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
