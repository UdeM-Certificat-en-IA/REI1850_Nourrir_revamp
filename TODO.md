## TODO

- [x] Remove extraneous shell prompt lines from `README.md`.
- [x] Add closing text for the license section.
- [x] Clean up shell prompt artifacts in `test.py`.
- [x] Add Netlify deployment configuration.
- [x] Verify Netlify deployment with serverless-wsgi wrapper.
- [x] Expand automated tests beyond network smoke test.
- [x] Integrate performance policy pages into the Flask app.
- [ ] Convert network smoke test to optional script and exclude from pytest.
- [ ] Improve responsive styling for performance policy pages.
- [x] Validate Netlify deploy after removing python version setting.
- [x] Confirm Netlify functions deploy correctly with new directory setting.
- [ ] Verify 404 issue is resolved with base path stripping.
- [x] Allow Flask port to be set via `PORT` environment variable.
- [ ] Verify Gunicorn command expands `$PORT` properly in Dockerfile.
- [x] Parameterize Netlify base path via `API_GATEWAY_BASE_PATH` environment variable.
