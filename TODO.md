## TODO

- [x] Remove extraneous shell prompt lines from `README.md`.
- [x] Add closing text for the license section.
- [x] Clean up shell prompt artifacts in `test.py`.
- [x] Add Netlify deployment configuration.
- [x] Verify Netlify deployment with serverless-wsgi wrapper.
- [x] Expand automated tests beyond network smoke test.
- [x] Integrate performance policy pages into the Flask app.
- [x] Replace old performance policy with NEW version and update sections.
- [ ] Convert network smoke test to optional script and exclude from pytest.
- [ ] Improve responsive styling for performance policy pages.
- [x] Add dropdown navigation menu to performance policy pages.
- [x] Replace back-to-index links with arrow buttons.
- [x] Embed policy explanation video on the performance index page.
- [x] Validate Netlify deploy after removing python version setting.
- [x] Confirm Netlify functions deploy correctly with new directory setting.
- [x] Verify 404 issue is resolved with base path stripping.
- [x] Fix redirect to include `:splat` for path forwarding.
- [ ] Test Netlify deploy after replacing union types with Optional for Python
      3.9 compatibility.
- [x] Allow Flask port to be set via `PORT` environment variable.
- [ ] Verify Gunicorn command expands `$PORT` properly in Dockerfile.
- [x] Parameterize Netlify base path via `API_GATEWAY_BASE_PATH` environment variable.
- [x] Set Netlify publish directory to `templates` to ensure static files are deployed.
 - [x] Integrate Frozen-Flask build for Netlify static deploy.
 - [x] Add GitHub Actions workflow to test build.
- [ ] Expand unit tests for API endpoints and performance pages.
- [x] Ensure Frozen-Flask outputs `.html` files for performance policy subpages.
