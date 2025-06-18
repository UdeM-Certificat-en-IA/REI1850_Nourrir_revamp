# Tippy.js Tooltip Tasks

 - [ ] **Identify Tooltip Terms**: List jargon or concepts (e.g., "dopamine", "probiotiques", "freemium", "NuRiH Ami") and draft concise definitions.

 - [ ] **Add `data-tippy-content`**: Wrap terms in spans:
   ```html
   <span data-tippy-content="Definition of the term">term</span>
   ```
   Add `cursor-help` style for hover indication.

 - [ ] **Include Tippy.js Assets**: In `base.html` `<head>`:
   ```html
   <link rel="stylesheet" href="https://unpkg.com/tippy.js@6/dist/tippy.css" />
   <script src="https://unpkg.com/@popperjs/core@2"></script>
   <script src="https://unpkg.com/tippy.js@6"></script>
   ```

 - [ ] **Initialize Tippy**: After DOM load:
   ```js
   document.addEventListener('DOMContentLoaded', () => {
     tippy('[data-tippy-content]', {
       theme: (localStorage.getItem('theme') === 'dark') ? 'dark' : 'light',
     });
   });
   ```

 - [ ] **Test Appearance**: Hover over terms to verify tooltip content, positioning, and readability. Adjust `maxWidth` or `placement` as needed.

 - [ ] **Tooltip Theme Adjustments**: Confirm tooltips display correctly in light and dark modes. Add custom CSS overrides if necessary.

 - [ ] **Mobile Behavior**: Test tooltip tap behavior on touch devices (tap to show/hide).

 - [ ] **Edge Cases**: Ensure tooltips do not overlap or disrupt layout on both desktop and mobile.

 - [ ] **i18n Integration (Optional)**: For multilingual tooltips, use `data-i18n-tooltip="key"` and update tooltip content on language switch.

 - [ ] **No JS Fallback**: Accept that tooltips will not display without JS; consider an underline CSS hint if desired.

 - [ ] **Performance Consideration**: Verify initialization overhead is minimal for a small number of tooltips.