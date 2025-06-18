# Dark/Light Mode Toggle Tasks

 - [ ] **Add Theme Toggle UI**: Insert a theme switch control in the nav:
   - Use a checkbox input (`<input type="checkbox" class="toggle" />`) or an icon button.
   - Label it with a moon/sun icon or inline SVG that changes on state.

 - [ ] **Alpine State for Theme**: Initialize Alpine in `base.html`:
   ```html
   <html x-data="{ theme: localStorage.getItem('theme') || 'light' }" data-theme="theme">
   ```

 - [ ] **Toggle Logic**: Bind the checkbox to Alpine:
   ```html
   <input type="checkbox" class="toggle"
     :checked="theme === 'dark'"
     @change="theme = $event.target.checked ? 'dark' : 'light'; localStorage.setItem('theme', theme)">
   ```

 - [ ] **Verify DaisyUI Theme Activation**: Confirm that setting `data-theme="dark"` switches to dark mode (check `bg-base-100`, `bg-base-200`, `text-base-content`).

 - [ ] **Icon Feedback**: Optionally show toggle icons:
   ```html
   <span x-show="theme==='light'">☀️</span>
   <span x-show="theme==='dark'">🌙</span>
   ```

 - [ ] **Persist on Reload**: Test that theme preference persists after page refresh and reloading the site.

 - [ ] **System Prefers Dark (optional)**: Detect `window.matchMedia('(prefers-color-scheme: dark)')` to set default theme on first load if no localStorage value.

 - [ ] **Test Styling in Both Modes**: Manually verify UI components switch correctly in light and dark modes.

 - [ ] **Edge Cases**: Ensure i18n translation and theme toggle coexist without conflicts.

 - [ ] **Update Documentation**: Document dark mode support and toggle instructions in `README.md`.