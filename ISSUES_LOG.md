## Issues Log

- [ ] Test script fails due to network access restrictions when reaching n8n webhook.
- [ ] Netlify deployment may fail if Ollama endpoints are blocked or require authentication.
- Added local Flask route tests using pytest to avoid network failures.
- [ ] Performance policy pages need improved responsive styling.
- [x] Netlify deploy failed to parse configuration; replaced `python_runtime` with `python_version`.
- [x] Netlify deploy still failed due to `python_version`; removed the property entirely.
- [x] Netlify deploy preview served 404s due to functions not detected; added explicit directory setting.
- [ ] Deployed site still returns 404; added base path stripping and included files for templates. Parameterized the base path via `API_GATEWAY_BASE_PATH` to allow configuration. Pending verification after next deploy.
- [x] Redirect did not forward the requested path to the Flask function; added `:splat` to the Netlify redirect.
- [ ] Netlify deploy uploaded 0 files because no publish directory was defined. Set `publish = "templates"` in `netlify.toml` to ensure pages are uploaded.
- [ ] Netlify Python runtime may be <3.10 causing syntax errors from union type
      hints. Updated code to use `typing.Optional` for compatibility.
- [ ] Docker container may not honor `PORT` variable due to exec-form CMD.
