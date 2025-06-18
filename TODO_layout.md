# Structured Sections & Responsive Design Tasks

  - [x] **Section Containers**: Wrap logical sections in `<section>` or `<div>` with Tailwind/DaisyUI classes (e.g., `class="p-6 my-8 rounded-lg shadow-md bg-base-200"`).

  - [x] **Grid Layout for Values**: Use:
   ```html
   <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
     <!-- DaisyUI cards for each value -->
   </div>
   ```
   and `card` components for each item with icon and text.

 - [x] **Typography Styling**: Apply consistent headings (e.g., `text-2xl font-bold`) and body text (`prose` class if using DaisyUI Typography plugin).

  - [x] **Spacing Adjustments**: Remove `<br>` tags; use Tailwind margin utilities (`mt-8`, `mb-4`) for vertical spacing.

  - [x] **Responsive Video/Media**: Wrap iframes or videos in a responsive container (e.g., `class="aspect-video"`).

  - [x] **Image Responsiveness**: Add `max-w-full h-auto` and meaningful `alt` text for all images. Optionally use DaisyUI masks.

 - [x] **Test Mobile Layout**: Verify on small viewports (e.g., iPhone SE) that content stacks vertically without horizontal scroll.

 - [x] **Test Desktop Layout**: Ensure content width is constrained (e.g., wrap in `max-w-4xl mx-auto`) and spacing is balanced.

  - [x] **Consistency Across Pages**: Apply above styling to all pages (Accueil, Politique, Performance, Contact).

 - [x] **Footer Styling**: Style footer with DaisyUI classes (e.g., `footer p-4 bg-neutral text-neutral-content text-sm text-center`).

  - [x] **Clean Up Old CSS**: Remove or deprecate legacy custom CSS in `static/assets` that is superseded by Tailwind/DaisyUI.

- [x] **Update Tests**: Adjust any existing tests (snapshots or Selenium) to match the new HTML markup.

 - [x] **Insert Performance Images**: Added NEW_Images to the performance policy pages with alternating layout and fade-in transitions.
 - [x] **Fade-In on Scroll**: Implemented IntersectionObserver script to reveal sections smoothly when scrolling.
 - [ ] **Add Missing Office Images**: Insert additional office scene visuals once assets become available.
