## Dark/Light Theme Toggle Issue

### Description
The dark/light theme toggle button does not function as expected:
- Clicking the button does not switch the theme.
- The selection is not persisted across page reloads.

### Root Cause
- Theme logic is currently implemented using Alpine.js directives (`x-data`, `x-init`, and `:data-theme`) that may not execute reliably:
  - Reliance on Alpine.js loaded from an external CDN can fail in offline or restricted environments.
  - The JavaScript module `ui.js` provides `getPreferredTheme` and `applyTheme` utility functions for theme management but does not invoke them on page load or button click.
  - Initial theme application is not performed by `ui.js`, leading to missing `data-theme` attribute until Alpine mounts.
- Tests (e.g., Playwright) may check `data-theme` before Alpine initializes, causing assertion failures.

### Proposed Solutions
1. **Implement Theme Initialization in `ui.js`**  
   - Call `applyTheme(getPreferredTheme())` on `DOMContentLoaded` to set the `data-theme` attribute and persist theme selection.  
   - Attach a click listener to the theme toggle button to invoke `applyTheme` and update `aria-pressed`.
2. **Remove or Supplement Alpine.js Theme Code**  
   - Optionally remove Alpine-specific theme directives (`x-data`, `x-init`, `:data-theme`, `@click`) from the HTML to prevent duplication.  
   - Rely on the standalone `ui.js` logic for theme toggling to reduce external dependencies and improve test stability.
3. **Vendor Alpine.js Locally**  
   - Bundle Alpine.js within the project (e.g., `/static/js/alpine.min.js`) instead of loading from a CDN to ensure availability in offline/test environments.
4. **Add Inline Fallback Script**  
   - Insert a small inline script in the `<head>` to read `localStorage` and apply the `data-theme` attribute before the page renders, preventing FOUC and ensuring correct initial theme.
## Missing Performance Policy Dropdown

### Description
- The desktop navigation under “Politique de performance” should display a dropdown menu listing all performance sections (Phases 1–4, Acteurs clés, Conclusion, Glossaire, Bibliographie, Résumé) but currently offers no submenu.

### Root Cause
- The template `base.html` only includes a direct link for “Politique de performance” in the desktop menu without any nested submenu markup.
- The mobile view includes a nested dropdown for performance sections, but the desktop menu omits this pattern.
- There is no data-driven mechanism in Flask to pass performance section metadata into the desktop menu for rendering.

### Proposed Solutions
1. **Add Dropdown Markup in Desktop Menu**  
   - Wrap the “Politique de performance” `<li>` in a `<div>` or `<li>` with DaisyUI’s `dropdown dropdown-hover` (or `dropdown dropdown-click`) classes.  
   - Insert a nested `<ul class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52">` containing `<li><a>` entries for each performance section.  
   - Include a caret indicator (e.g., ▾) next to the main link to signal the submenu.
2. **Make Menu Data-Driven**  
   - Define a list of performance sections (identifiers, URLs, labels) in the Flask view for `performance_index` and pass it to `base.html` (e.g., `nav_items.performance_sections`).  
   - Use a Jinja2 loop in the desktop dropdown to render submenu items, preventing duplication with the mobile menu logic.
3. **Enhance Accessibility & Keyboard Support**  
   - Add `aria-haspopup="true"` and `aria-expanded="false"` on the parent link, and toggle `aria-expanded` on hover or click.  
   - Enable focus and Escape key handling to open/close the submenu.
4. **Improve Aesthetics & Transitions**  
   - Use Tailwind transition classes (e.g., `transition-opacity duration-150 ease-in`) to fade the dropdown in/out.  
   - Apply a slight border or backdrop-blur (`backdrop-blur-sm bg-opacity-80`) for visual separation.  
   - Ensure high-contrast hover and focus states for submenu items, consistent with existing `.hover:bg-base-200` styling.
5. **Refactor Navigation Partial**  
   - Extract the desktop and mobile menu into a separate Jinja2 partial (e.g., `_nav.html`) to centralize updates and avoid code duplication.
6. **Update Tests**  
   - Modify `tests/test_nav_dropdown.py` to assert the presence of the desktop dropdown container and submenu items on hover or click.  
   - Ensure keyboard navigation tests reflect updated `aria-*` attributes.