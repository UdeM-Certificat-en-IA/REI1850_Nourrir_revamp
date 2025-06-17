# TODO for Integrating the Performance Policy into the Main Web App

1. Integrate performance pages into Flask:
   - Copy the `site/` HTML files from `static/assets/Performance/performance_policy/site/` into a new `templates/performance_policy/` folder.
   - Convert each static HTML file into a Jinja template: wrap with `{% extends 'base.html' %}` and place the existing `<main>` content inside `{% block content %}`.
   - Update asset paths in templates:
     - Replace `src="../docs/Presentatation.mp3"` with `src="{{ url_for('static', filename='assets/Performance/performance_policy/docs/Presentatation.mp3') }}"`.
     - Replace `href="../docs/performance_policy_fr/performance_policy_fr.pdf"` with `href="{{ url_for('static', filename='assets/Performance/performance_policy/docs/performance_policy_fr/performance_policy_fr.pdf') }}"`.
   - Add new routes in `app.py` (or create a blueprint) for:
     - `/performance` → renders the performance index template.
     - `/performance/<section>` → renders the corresponding section template.
   - Add a “Politique de Performance” link in the main navigation (`templates/base.html`), pointing to `url_for('performance_index')`.

2. Serve static media:
   - Ensure `static/assets/Performance/performance_policy/docs/Presentatation.mp3` and `performance_policy_fr.pdf` remain in place.
   - Verify Flask’s `static_folder` settings correctly serve these files.

3. Navigation and UI:
   - Add buttons or links on the homepage (or other key pages) to promote access to the performance policy section.
   - Ensure menu highlighting works for the performance section when active.
   - Apply consistent CSS animations or transitions (e.g., fade-in on page load) to harmonize with the site’s style.
   - Confirm responsive behavior on tablets and mobile devices.

4. Cleanup and consistency:
   - Remove `static/assets/Performance/performance_policy/scripts/`, source `.md` files, archives, and conversion scripts from the assets folder.
   - Keep only:
     - `site/` (for HTML templates or reference).
     - `docs/Presentatation.mp3`.
     - `docs/performance_policy_fr/performance_policy_fr.pdf`.
     - This `TODO.md` (task list).
   - Remove any leftover `README.md`, `Instructions.md`, `LICENSE`, and markdown source files not used by the running site.

5. Testing and documentation:
   - Run the Flask app locally and navigate through `/performance` and its subpages to ensure correct rendering.
   - Test PDF download and audio playback within the performance pages.
   - Update the project’s main `README.md` to mention the new “Performance Policy” section and provide navigation instructions.
