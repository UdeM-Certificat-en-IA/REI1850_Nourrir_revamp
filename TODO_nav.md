# Adaptive Navigation & Responsive Menu Tasks

 - [x] **Integrate DaisyUI/Tailwind Navbar**: Replace current nav HTML in `base.html` with a responsive navbar. Use DaisyUI’s navbar component or custom Tailwind classes:
   - Wrap nav elements in `<div class="navbar bg-base-100">...</div>`. Ensure branding/logo is on the left and menu on the right.

 - [x] **Mobile Hamburger Menu**: Add a menu toggle button for small screens:
   - `<button class="btn btn-ghost md:hidden" aria-label="Toggle navigation">☰</button>`
   - Bind Alpine `@click` to toggle a menu state (e.g., `x-data="{open:false}" @click="open = !open"`).

 - [x] **Menu Items List**: Convert page links into a desktop menu:
   - Use `<ul class="menu menu-horizontal p-0 hidden md:flex">` with `<li><a href="/...">Label</a></li>`.
   - For mobile, use `<ul class="menu menu-compact" x-show="open">` to show links when `open` is true.

 - [x] **Active Link Highlight**: Add `class="active"` to the `<a>` of the current page. Use Jinja or Flask context to set this dynamically.

 - [x] **Accessibility**:
   - Add `aria-label="Toggle navigation"` to the hamburger button.
   - Ensure `<ul role="menu">` and `<a role="menuitem">` for links.
   - Bind `@keydown.escape.window="open=false"` to close the menu with Esc.

 - [x] **Test Responsive Behavior**: Verify in narrow viewport only the hamburger icon appears and toggles the menu. In wide viewport, ensure menu items display and hamburger is hidden without overflow.

 - [x] **Scroll Animation**: Fade header out when scrolling down and back in when scrolling up for smoother transitions.

 - [x] **Logo Transition**: Shrink and move the logo to the left as the header hides, returning to center when scrolling back to the top.

 - [x] **Dark Mode Toggle**: Ensure the theme switch is easily clickable and aligned to the right of the navbar.


 - [x] **Style Consistency**: Use DaisyUI classes for styling. Optionally apply `btn btn-ghost` on links or default `<a>` styling, and accent colors for hover/active states.

 - [x] **Logo Integration**: If a logo exists, place it on the left with `<img>` inside a `btn btn-ghost`, sized with Tailwind classes (e.g., `w-10 mr-2`) and proper `alt` text.

 - [x] **Netlify Routing Check**: Confirm nav `href` values match existing routes (`/`, `/politique`, `/performance`, `/contact`) with no URL changes.

