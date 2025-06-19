--- PAGE 1 ---

ChatGPT

REVAMP_ROADMAP

Overview and Current Architecture

The NourrIR project is a Flask application that serves multiple static pages (Accueil/Home, "Politique d'intégration" (Integration Policy), "Politique de performance" (Performance Policy), "Contact RH" (HR Contact)) and provides a floating AI chat widget ("NuRiH Ami") on all pages. In the current setup, Flask renders these pages and uses Frozen-Flask to freeze the app into static files for deployment on Netlify 2. A Netlify serverless function (/.netlify/functions/flask_app) acts as a proxy endpoint to an Ollama LLM backend for the chat feature 3. Tailwind CSS (with DaisyUI components), Alpine.js (for interactivity), and i18next (for internationalization) are integrated into the front-end to various extents in the "NEW" branch of the repository. The site is deployed on Netlify, which hosts the static pages and the serverless function, as confirmed by the presence of a netlify.toml and netlify/functions/ in the repo (indicating custom Netlify configuration). The deployment process likely involves using Frozen-Flask to generate static files and then publishing them via Netlify CLI or CI 2 4.

Goal: We will revamp the UI/UX in multiple stages while preserving the Frozen-Flask static export pipeline. The revamp will implement an adaptive navigation menu, a dark/light theme toggle, multilingual content support, structured content sections, responsive design improvements, and Tippy.js tooltips for nutritional info pop-ups. Each stage below includes clear instructions, and all steps are cross-referenced with official documentation or relevant sources. The plan also provides integration options (CDN vs build pipeline) for each dependency, file-specific TODO checklists, CI/testing suggestions, and guidance for verifying Netlify deployments to avoid build or export issues. Stage 1: Integrate Tailwind CSS & DaisyUI for Layout and Navigation

Objective: Establish a modern design foundation using Tailwind CSS and the DaisyUI component library. This will enable rapid UI improvements like structured section boxes and an adaptive navigation menu. We will replace existing styling with Tailwind/DaisyUI classes and ensure the site layout becomes fully responsive. • Setup Tailwind CSS: We have two integration options:

• CDN Approach: Include Tailwind via CDN in base.html for quick setup. Tailwind's official CDN script (Tailwind v3+) can be added to the page, enabling Tailwind utility classes without a build step 5. This is simplest, but for production it's recommended to lock versions and potentially switch to a build pipeline later. • Build Tool Approach: Use Tailwind CLI or a bundler to generate a static CSS. For a more maintainable solution (especially if customizing theme colors or using many utilities), set up Tailwind via npm. According to DaisyUI's maintainer, you can install Tailwind CLI and add DaisyUI as a plugin in the Tailwind config 5 6. This requires Node.js during development and on Netlify's build. Initially, we will likely use the CDN for speed, then transition to a build step once the design stabilizes.

1

--- PAGE 2 ---

• Include DaisyUI: DaisyUI can be used via plugin (during a build) or via CDN. With Tailwind's CDN, we can also pull DaisyUI's precompiled CSS. DaisyUI v5 provides a smaller customizable CDN file that works with Tailwind's CSS variables mode 7. Option 1: add DaisyUI's CSS CDN link (e.g. https:// cdn.jsdelivr.net/npm/daisyui@5/dist/full.css) in base.html. Option 2: if using Tailwind build, install daisyui package and add it to tailwind.config.js under plugins 5 (the DaisyUI docs provide an install snippet 6). We will start with the CDN approach for immediate results, then note in TODOs to move to a proper build for advanced theme customization. • Apply Layout and Component Classes: Once Tailwind and DaisyUI are included, refactor the HTML structure in index.html, politique.html, contact.html (and any other template) to use Tailwind utility classes and DaisyUI components for a cleaner UI:

Structured Section Boxes: Wrap content sections (e.g. "Nos valeurs", "Notre mission", etc.) in DaisyUI card or panel components to visually separate them. For example, use a <div class="card bg-base-200 p-6 rounded-box"> around each value or mission section. DaisyUI's ready-made styles will provide subtle backgrounds and padding for these boxes. Ensure headings use consistent Tailwind typography classes (e.g. text-xl font-bold for section titles, etc.). • Responsive Grid: Use Tailwind's grid or flex utilities to make sections like "Nos valeurs" display as a grid of cards on larger screens and a single column on mobile. E.g., <div class="grid grid-cols-1 md:grid-cols-3 gap-8"> to arrange value cards in 3 columns on medium+ screens. This ensures the layout adapts to different viewports.

Images and Icons: Replace any fixed sizing with Tailwind classes (like w-16 h-16 for icons) and use responsive utilities (max-w-full, h-auto) to ensure images scale down on small screens. For example, the value icons (accessibilité, inclusion, etc.) can be given a uniform Tailwind class for sizing. Typography and Spacing: Utilize Tailwind for consistent spacing (e.g. my-4 for vertical margins) and DaisyUI's Typography plugin (if included) for styled text in content. Ensure that lists (like the bullet points under "Fonctionnalités clés") have proper spacing or use DaisyUI's prose class if the typography plugin is available 8.

• Adaptive Navigation

Menu:

Convert the top navigation bar (Accueil | Politique... | Contact RH | ...) into a responsive menu. DaisyUI provides a navbar component which we can leverage, or we can implement manually with Tailwind + Alpine.js:

• Use a hamburger menu icon for mobile. For DaisyUI, the Navbar component combined with a Drawer or Menu component can create a collapsible menu. Alternatively, manually hide the full menu on small screens (hidden md: flex on the links container) and show a menu button (md:hidden for the button). • Use Alpine.js for toggling the menu on mobile. Alpine can handle a simple state for menu open/ closed. Include Alpine via CDN (a <script defer src="https://cdn.jsdelivr.net/npm/ alpinejs@3.x.x/dist/cdn.min.js"></script> in the head, as per official docs 9 10). This script makes Alpine's x-data and x-show directives available.

Implement the toggle: e.g. <button class="btn btn-ghost md: hidden" @click="open = ! open" x-data="{open: false}" aria-label="Toggle Menu">=</button> and a <ul x-show="open" class="menu menu-compact">...</ul> for the dropdown links on

2

--- PAGE 3 ---

mobile. DaisyUI's menu class can style a vertical list of links nicely. Ensure the menu closes when a link is clicked (Alpine's \$watch or simple event handlers can reset open ). The adaptive behavior means on larger screens the ul.menu is always visible (using md: flex) and on small screens it is controlled by Alpine (hidden when closed). • Style the active page link and on-hover states using DaisyUI classes (for example, add active class to the current page's <a> or use Tailwind font-bold for emphasis). DaisyUI automatically styles an active menu item differently.

• Initial Testing: After integrating Tailwind and DaisyUI, test the site at various screen widths. Verify that content reflows without horizontal scrolling on mobile (no content cut off). The static pages should render correctly from the Frozen-Flask output as before since we are only changing the templates, the freezing process (calling Freezer.freeze()) will still generate the same routes 11 12. We must ensure no dynamic content is introduced that Frozen-Flask can't capture. Using Alpine and client-side behavior is fine, as Frozen-Flask will just include those scripts and attributes in the static HTML without needing to execute them (Frozen-Flask will still generate the HTML with our new classes/markup). All new CSS/JS is either via CDN or in static/assets, which Frozen-Flask will treat as static files to copy (we should double-check that any new asset files are placed under static/ so they get picked up or referenced via absolute URL/CDN). References: Tailwind and DaisyUI integration best practices 56, DaisyUI components usage 13, Alpine.js inclusion for interactivity 9 10.

Stage 2: Implement Dark/Light Mode Toggle

Objective: Add a user-selectable Dark Mode using DaisyUI's theming capabilities (or Tailwind's dark mode utilities). The site should allow toggling between a light theme and a dark theme, improving accessibility and user preference accommodation. • Enable DaisyUI Themes: DaisyUI comes with built-in themes (including light and dark by default) 14 15. In our Tailwind/DaisyUI setup, ensure the dark theme is available. By default, DaisyUI's light and dark are enabled (with dark responding to the OS preference if prefersdark is set) 16 15. We may explicitly configure DaisyUI to be safe. If using CDN, the DaisyUI CSS likely already includes the themes. If using a build, update daisyui config in tailwind.config.js to ensure both themes are included (e.g. themes: ["light", "dark"]). • Theme Toggle UI: Add a toggle control in the navbar for switching themes. DaisyUI has a pre-built toggle component (<input type="checkbox" class="toggle" />) 17 which we can style as a dark mode switch. For example, a moon/sun icon that flips: we can use an icon font or emoji ( ) on a button, or the checkbox styled as a switch. Place this toggle at the top right of nav (e.g., as the last item in the menu). Use Alpine.js to handle the toggle interaction: clicking the toggle should switch the theme. • Applying Themes: DaisyUI themes work via the data-theme attribute on the <html> (or <body>) tag 18. For instance, when data-theme="dark", all DaisyUI components switch to dark colors, and when data-theme="light" (or attribute removed), the light theme applies. We

3

--- PAGE 4 ---

will use Alpine or vanilla JS to set this attribute. Example approach: in base.html 's <html> tag include x-data="{theme: 'light'}" data-theme="theme" and on the toggle button, use @click="theme = (theme === 'light'? 'dark': 'light')" to bind the attribute 19 This way, clicking the toggle dynamically updates data-theme. Alternatively, use DaisyUI's recommended theme-change script which can automate applying themes and storing in localStorage 20, but a simple Alpine solution is sufficient here (and avoids adding another dependency). • Persisting Choice: To enhance UX, we should remember the user's theme preference. Alpine's \$persist plugin or manual localStorage usage can store the last chosen theme. For example, include Alpine Persist plugin (if available) or write a snippet: on load, check localStorage.theme and set theme accordingly; on toggle, do localStorage.theme = theme. DaisyUI's documentation suggests using theme-change or similar to handle this automatically 20, but we can manage it in a few lines of Alpine JS. • Tailwind Dark Classes (if needed): In addition to DaisyUI themes, ensure any custom styling respects dark mode. If we use Tailwind's own dark mode utilities (which can be configured to use data-theme instead of media query 21 22), we could add specific classes. However, since DaisyUI themes cover most of the styling (background, text colors, components), we might not need many manual dark: classes. Verify elements like text on images or custom CSS to ensure contrast in dark mode. If needed, utilize Tailwind's dark: variant for any custom styles (e.g., dark: text-gray-100 for body text). • Testing Theme Toggle: After implementing, test switching to dark mode: The background should turn dark (DaisyUI's dark theme sets a dark gray/black base), text should turn light, and all components (cards, navbar, buttons) should restyle accordingly. For example, DaisyUI's dark theme will cause bg-base-200 or bg-base-100 classes to appear dark 23. Ensure the toggle itself is visible in both modes (you may use a DaisyUI icon or swap an SVG of sun/moon that also changes color). Also verify that the chosen theme persists on page reload (simulate by refreshing the page - if using localStorage logic, it should reapply the last theme). • Frozen-Flask Consideration: The theme toggle is entirely client-side (via Alpine and CSS attributes). This does not affect the static generation - Frozen-Flask will freeze the page with the default theme attribute (likely 'light' by default on html). That's fine because the user can switch after load. There's no impact on the frozen HTML aside from the added x-data and data-theme attribute, which are just static attributes that do nothing until the JS runs. We should document in the README or a comment that the default build theme is light unless changed via the toggle. References: DaisyUI theme usage (setting data-theme on html) 18, DaisyUI's note on theme-change for local storage 20, DaisyUI toggle component reference 17.

4

--- PAGE 5 ---

Stage 3: Add Multilingual Support (i18next)

Objective: Enable multilingual support, initially for English and French, by integrating i18next. The goal is to allow content to dynamically switch languages without separate static pages, preserving the single-page static structure while offering translations. • Integrate i18next Library: Include i18next via CDN or as a bundled script. The simplest route is to add a CDN script tag for i18next in base.html (for example, use the latest version from unpkg or jsDelivr: <script src="https://unpkg.com/i18next@21.8.0/dist/umd/ i18next.min.js"></script>). It's important to pin a version for stability 24. This will expose a global i18next object at runtime. • Prepare Translation Resources: Extract all user-facing text from the HTML templates to translation JSON files. Create, for example, static/assets/locales/en/translation.json and static/ assets/locales/fr/translation.json. These files will contain key-value pairs, e.g.:

// en/translation.json

{ "welcome_message": "Welcome to NourrIR",

}

// fr/translation.json

{ "welcome_message": "Bienvenue chez NourrIR",

}

Create keys for every piece of text in the site (page titles, section headings, paragraph text, menu items, button labels, etc.). Using natural language keys is possible but not recommended by i18next by default 25, so use descriptive keys (as in the example). For structure, you can group keys by section (e.g., home.mission_title, home.mission_body). This is a meticulous step but ensures all content can be swapped easily. • Initialize i18next: In a new script (either inline in base.html or a separate JS file included at the bottom), initialize i18next when the page loads. For a simple implementation, we can embed the resources directly for two languages or use XHR to fetch the JSON. To avoid extra runtime complexity, one approach is to embed resources into a <script> tag via a JS object (not ideal for huge content, but fine for a small site). Alternatively, use i18next's XHR backend to load the.json files. For illustration, we could do:

i18next.init({
 Ing: 'fr',
 debug: false,
 resources: {

}

en: { translation: ${/* loaded EN JSON ...*/} },

fr: { translation: {/* loaded FR JSON ...*/} }

}, function(err, t) {

// After init, update the UI

document.querySelectorAll('[data-i18n]').forEach $(el=>\{$

5

--- PAGE 6 ---

el.innerHTML = t(el.getAttribute('data-i18n'));

});

});

Here we assume each translatable element has a data-i18n attribute whose value is the translation key. We use i18next.t(key) (provided via the t function in the callback) to set the text 26 27. The official docs show a similar basic setup where i18next.init is called with resources and then i18next.t('key') gives the translated string 26 28. We will use a loop to populate all elements marked for translation. (Alternatively, i18next has a jquery-i18next plugin or i18next.syncLocalize methods, but a simple loop is sufficient.)

• Marking Translatable Elements: Modify templates to use <span data-i18n="key_name"></ span> in place of hardcoded text. For instance, the welcome headline in index.html might become <h1 data-i18n="home.welcome_heading"></h1>. We keep one language's text (say French) as the default inside for noscript users/SEO, but then also include the data-i18n attribute. Another method: place the key in the tag and an initial text in another attribute like data-i18n-fr (but that complicates things). Simpler: we can leave the French text in the HTML and rely on i18next to replace it if another language is chosen. However, when i18next initializes with 1ng: 'fr' by default, it will replace content with the same French text from resources, which is harmless. For clarity, it might be cleaner to remove inner text and always set via i18next after init. We'll weigh SEO vs implementation ease: since this is a demo/pedagogical project, we can go with dynamic replacement entirely. • Language Switch UI: Add a language selector in the navbar (for example, a dropdown or two buttons "FR | EN"). When the user selects a language, call i18next.changeLanguage (newLang) and then re-render the text. Using i18next's API: i18next.changeLanguage('en') will switch the internal language and call any callback if provided. We will need to re-run the loop to update text, or leverage the fact that changeLanguage can trigger an event. For simplicity: after calling changeLanguage('en'), immediately call a function to update all [data-i18n] elements as done after init (essentially the same loop using i18next.t). The i18next docs note that if you pass resources on init, i18next is ready and i18next.t will work for the new language after changeLanguage 29 30. Optionally, include the i18next Browser Language Detector plugin to auto- detect browser language, but not required if we default to French and let user switch. • Preserving Static Site & SEO: We must note that using client-side translation means the default frozen HTML is mostly in one language (French, presumably). This is fine for functionality, but search engines will only see the default language content (unless we generate a separate static version or use prerendering). Given the scope, we'll accept that trade-off. If SEO for both languages is needed, another approach would be to generate static pages for each language (e.g., Frozen-Flask route / en/ and /fr/), but that complicates the pipeline and navigation. Our approach keeps a single set of pages and uses JS for translation, which is simpler and aligns with preserving the current static export pipeline (no extra Freeze runs). We should ensure that if JS is disabled, the site is still usable (so having the default language content in the HTML is important). Therefore, do leave the French text as the initial content in the HTML elements; the data-i18n attributes can be added in addition (or we use a convention where the element's text is the French fallback). In our update loop, we could skip updating if the current language is the same as default to avoid flicker. 6

--- PAGE 7 ---

• Testing Multilingual Feature: After implementing, test that switching to English replaces all text appropriately. For example, "Bienvenue chez NourrIR" should change to "Welcome to NourrIR", etc. Check menu items, section headings, body text, button labels ("Envoyer" on the chat send button should become "Send" in English, etc.). Also test switching back to French. The switch should be near-instant. If performance is an issue (unlikely given small content), consider disabling debug mode and minifying JSON. Also test on a fresh load: if we want to remember language, use localStorage similarly (store last chosen lang and pass it as 1ng in init next time). i18next's docs and samples demonstrate dynamic language switching via changeLanguage() 31 32. We will also add a note in TODO to consider adding a language detector plugin or manual persistence of language choice. • Impact on Frozen-Flask: Since translations are done at runtime, Frozen-Flask still just freezes the base French version (with the data-i18n attributes included in the HTML). There's no effect on the freezing process (no new routes). We just need to ensure the static JSON files (if used for resources) are included in the static/ folder so they get deployed. Netlify will serve them as static assets. (If embedding resources in the JS, then no additional files beyond the i18next library are needed). To avoid any build-time errors, we won't attempt to load JSON in Flask; all loading is done in-browser. Thus, the Frozen output remains a static site with some enhancement scripts. References: i18next basic initialization and usage 26 28, i18next language switching example 30.

Stage 4: Nutrition Tooltips with Tippy.js

Objective: Introduce tooltips that show nutrition or glossary information when users hover or tap on specific terms (for example, definitions for "probiotics", "freemium", or other domain-specific words in the content). This adds an interactive layer of educational info without cluttering the page. We will use Tippy.js, a lightweight tooltip library, to implement this. • Include Tippy.js: Add Tippy.js and its dependency Popper.js via CDN. In the base template (likely in the footer or head), include the CSS and JS as recommended. According to Tippy's docs, for CDN usage you include Popper 2 and the Tippy bundle 33. For example:

<link rel="stylesheet" href="https://unpkg.com/tippy.js@6/dist/tippy.css" />

<script src="https://unpkg.com/@popperjs/core@2/dist/umd/popper.min.js"></ script>

<script src="https://unpkg.com/tippy.js@6/dist/tippy-bundle.umd.js"></ script>

(Using the production links with specific versions as shown above 34 ensures we get a fixed version 6 of Tippy and matching Popper). The Tippy bundle auto-injects its CSS into the page by default 35, but we add the CSS link for CSP safety and to ensure styling. • Mark Terms for Tooltips: Identify all occurrences of terms that warrant a tooltip. For each, wrap or replace the text with an element that has a data-tippy-content attribute containing the tooltip

7

--- PAGE 8 ---

text. For example, if in a paragraph we have "Impact des probiotiques sur l'humeur...", change "probiotiques" to:

<span data-tippy-content="Microorganismes bénéfiques pour la flore intestinale et la santé mentale">probiotiques</span>

The value of data-tippy-content is the tooltip text (it can be plain text or include basic HTML for formatting if needed). Do this for each key term (e.g., the term "freemium" could have a tooltip explaining "a model with basic free content and paid premium features"). Keep the tooltip content concise. If the site had a structured data source for these, we might load via AJAX, but given the static context, hardcoding in the attribute is simplest. • Initialize Tippy: Once the DOM is loaded, call Tippy on all elements with the attribute. The library documentation suggests simply: tippy('[data-tippy-content]'); to auto-initialize tooltips on any element that has a data-tippy-content attribute 36. We can put this in a script at the end of base.html or in an external JS file. No additional configuration is needed for basic usage by default it will show on hover/focus with the content provided. We should ensure this script runs after the Tippy scripts are loaded, so place it in a <script> tag after those includes (and after the HTML content, or wrap in DOMContentLoaded event). Example:

<script>

document.addEventListener('DOMContentLoaded', function() {
 tippy('[data-tippy-content]');

});

</script>

The Digidop tutorial confirms this one-liner initialization 36. This will apply the default theme and animation. (Tippy's default theme is dark with a slight animation; that likely fits well, but we can adjust if needed.)

• Customize Tooltip Behavior (Optional): If desired, we can configure options like placement (e.g., top or bottom), delay, etc., in the tippy() call. For instance: tippy('[data-tippy-content ', { allowHTML: true, maxWidth: '300px' }); if we have HTML content or want to constrain width. Given our use-case (short definitions), default settings should suffice. Tippy tooltips will also be accessible (they manage aria-describedby for the target). • Styling and Theming: The default Tippy style is a light tooltip with a slight drop shadow. If we want it to match the site theme (light and dark mode), we might include Tippy's animations or themes CSS. The CDN we used already injects base styles; for dark mode, Tippy will detect our page's background? If not, Tippy has a separate dark theme we could apply by adding a class. Simpler: we can live with default style or use CSS variables to tweak colors later. DaisyUI doesn't directly style Tippy, but since Tippy content is in its own tooltip element appended to <body>, it won't automatically adopt DaisyUI theme. We could add a class like data-tippy-theme="light" or

8

--- PAGE 9 ---

"dark" conditionally. Tippy supports theming via data attributes as well (you can define a CSS for .tippy-box[data-theme=dark]). An advanced step could be to dynamically set data-theme on tooltips based on current theme (for example, after theme toggle, call document.querySelectorAll('.tippy-box').forEach(el => el.setAttribute('data- theme', current Theme))). For now, this complexity can be skipped unless visual testing shows a mismatch. We'll note this as a potential improvement. • Testing Tooltips: Manually test that hovering (or tapping, on mobile) the marked terms shows the tooltip with the correct text. For desktop: hover "probiotiques" and see the definition bubble appear. Test on mobile (using dev tools or on an actual device) that tapping the word shows the tooltip (Tippy by default makes tooltips tap-activated on touch devices). Check that tooltips are readable in both light and dark mode (especially if using default theme the default tooltip is dark with light text, which actually works well in dark mode but might be less visible in light mode backgrounds; we may invert it or use a different style). Tweak as needed (Tippy provides a light theme CSS if needed by including tippy.css and perhaps themes/light.css). Since the content is static, any fixes would be done via adding a small CSS override. For example, DaisyUI's tooltip component is separate and not used here; we rely on Tippy's styling. • Performance Consideration: Tippy initialization on many elements is lightweight, but if the site grows, we might consider using the delegate() method to handle dynamically (not necessary now). Also, all tooltip content is in the HTML, which for a handful of terms is fine. If there were dozens of definitions, one might externalize them or load on demand - not needed at this scale. • Frozen-Flask: The addition of tooltips does not affect the freezing process at all. The static HTML simply has some span tags with attributes and some extra scripts included. Frozen-Flask will include those in the output. Just ensure that the tippy() initialization script is included in the templates, not only in Flask routes (since we want it in the final HTML). There is no server-side component. No build-time errors should occur, since we are not running any of this during build - it's all client-side. (If a term to tooltip spans across multiple lines in a template, ensure correct Jinja syntax so as not to break the HTML output - minor detail). References: Tippy.js CDN usage and initialization 3437, example adding data-tippy-content attributes and init script 38 36.

Dependency Integration Options Summary

(This section provides an at-a-glance guide on how to integrate each front-end dependency either via CDN or build tools, aligning with the choices made above.)

• Tailwind CSS:

CDN: Use official Tailwind CDN script for quick setup (e.g. <script src="https:// cdn.tailwindcss.com"></script> with desired config). This auto-applies Tailwind JIT in the browser. You can customize it by adding a tailwind.config inline script if needed. Build: Install via npm and use Tailwind CLI or PostCSS. Configure content paths to include templates/*.html

SO

all

classes

are picked up.

Run

9

--- PAGE 10 ---

-0

tailwindcss -i input.css static/assets/tailwind.css--minify during development/CI. DaisyUI integration requires adding require('daisyui') in the Tailwind config and listing themes/plugins 5. The build output CSS is then linked in base.html

(Decision: Initially CDN for simplicity; eventually move to build pipeline for fine-grained control and to avoid CDN latency.)

• DaisyUI:

CDN: Include DaisyUI's precompiled CSS after Tailwind. For example, <link href="https:// cdn.jsdelivr.net/npm/daisyui@5.x/dist/full.css" rel="stylesheet" />. Ensure compatibility with the Tailwind version used (DaisyUI v5 is for Tailwind v4 alpha, v4 for Tailwind v3, etc.). Using the DaisyUI CDN is easiest but limits customization (though v5 CDN uses CSS variables for theming 7, which is somewhat customizable with overriding variables). • Build: Add daisyui plugin to Tailwind config 39 and include DaisyUI in the tailwind CSS build. This gives access to DaisyUI components via classes in HTML. You can then configure themes as shown in DaisyUI docs (in daisyui object in config) or accept defaults. The advantage is smaller CSS (only used classes if purging) and the ability to customize theme colors, etc. (Decision: Use CDN initially. In a later refactor, set up full Tailwind build with DaisyUI plugin to optimize and allow custom themes, as noted in TODO.)

• Alpine.js:

CDN: Include <script defer Alpine's UMD bundle via CDN with defer src="https://cdn.jsdelivr.net/npm/ alpinejs@3.x.x/dist/ cdn.min.js"></script> 40. This gives you x-data, x-show, etc. immediately. For persistence or other plugins, there are separate CDN includes (e.g. for \$persist, one would include an Alpine Persist plugin script). Build: Via npm, install alpinejs and (if using a bundler) import it (import Alpine from 'alpinejs') and initialize (Alpine.start() as per docs 41 42). This is typically not needed unless you have a JS build pipeline. (Decision: CDN - as is standard for Alpine usage on simple static sites. It's quick and "just works" with minimal overhead.)

• i18next:

• CDN: Use a UMD build from a CDN. e.g. <script src="https://cdnjs.cloudflare.com/ ajax/libs/i18next/21.8.12/i18next.min.js"></script> (or jsDelivr/unpkg link with pinned version 24). Additionally, if using plugins like XHR backend or Language Detector, include those CDN scripts as well (e.g. i18nextXHRBackend.js). In our simple setup, we might not need plugins. The CDN approach is fine for a small number of languages and moderate content. • Build: Install via npm (i18next and any plugins) and bundle using webpack/rollup. This allows tree-shaking unused features. If using a framework or TS, this might be preferred, but for our Flask static scenario, it's overhead. (Decision: CDN for base i18next. Possibly load translation resources via additional script logic rather than needing the XHR backend plugin - e.g., fetch JSON via fetch() in an Alpine or plain JS code. This avoids another dependency. Since performance is not critical here, embedding or simple fetch is fine.)

• Tippy.js:

• CDN: As documented, include Popper.js and Tippy's bundle via script tags 34, and include Tippy's CSS (via link or it auto-injects). This is straightforward and suitable for our use (Tippy is small, ~5KB

10

--- PAGE 11 ---

gzipped JS plus CSS). There's also a lite version if we didn't need all features, but not necessary. • Build: Install tippy.js and @popperjs/core via npm and import in your JS bundle. If we had a bundler, we could do import tippy from 'tippy.js'; import 'tippy.js/dist/ tippy.css'; Without a bundler, CDN is easier.

(Decision: CDN. It's one-time load and cached, and avoids any build complexity.)

Each dependency via CDN should be pinned to specific versions to avoid breaking changes. We will document these in the code (for example, using @version in the URL). The CDN approach means no local build step is required on Netlify - our netlify.toml can remain focused on the Python freeze (unless we later add a Node build for Tailwind). If/when we transition to a build pipeline, we'll update Netlify's build command to run npm install && npm run build (for Tailwind) before freezing. File-by-File TODO Checklists

(Below are detailed TODOs for implementing the above changes, organized by area, as separate markdown files. These checklists can be used to track the revamp tasks across the codebase.)

File: TODO_nav.md - Adaptive Navigation & Responsive Menu Tasks

[ ] **Integrate DaisyUI/Tailwind Navbar**: Replace current nav HTML in base.html with a responsive navbar. Use DaisyUI's 'navbar component or custom Tailwind classes:

Include a container (e.g. <div class="navbar bg-base-100"> ...) wrapping the nav elements. Ensure branding/logo is on the left (if applicable) and menu on the right. [ ] **Mobile Hamburger Menu**: Add a menu toggle button for small screens: Use an <button class="btn btn-ghost md:hidden">=</button> for the hamburger icon (or DaisyUI's menu icon SVG). Bind Alpine @click to toggle a menu state (e.g. x-data="{open:false}" @click="open = !open"). [ ] **Menu Items List**: Convert the list of page links into a <ul class="menu menu-horizontal p-0 hidden md: flex"> for desktop:

Each menu item as <li><a href="/...">Label</a></li> (DaisyUI will style .menu-horizontal a nicely). On mobile, use a vertical menu (menu-compact) that is hidden by default and shown when open is true (x-show="open"). [ ] **Active Link Highlight**: Add an 'class="active" to the '<a>' corresponding to the current page. (Flask can set this by passing an

active_page context or comparing request.path in template to highlight.) Alternatively, use a Jinja condition in 'base.html to add e.g. <span class="underline"> or bold style for the current page link. [ ] **Accessibility**:

Add aria-label="Toggle navigation" to the hamburger button. Ensure the menu <ul> has appropriate role (e.g. <ul role="menu">` and

`<a role="menuitem"> for links, though DaisyUI may handle basics). When menu is open, pressing Esc should close it (Alpine:

11

--- PAGE 12 ---

@keydown.escape.window="open=false"`).

[ ] **Test Responsive Behavior**:

In a narrow viewport, verify only the hamburger icon is visible and clicking it toggles the menu items. In a wide viewport, verify the menu items are visible and the hamburger is hidden. Ensure no layout shift or overflow when toggling.

[ ] **Style Consistency**: Use DaisyUI classes for styling:

navbar will handle base styling. For menu items, btn btn-ghost on links

can make them button-like if desired, or stick to default <a> styling. Possibly use an accent color for hover or active states (DaisyUI uses current theme's primary color on.active). - [ ] **Logo (if any)**: If there is a logo image (e.g., "Logo NourrIR"), ensure it's integrated:

Place it in the navbar left with appropriate alt text. Use Tailwind classes for its size (e.g. w-10 mr-2) and DaisyUI's .btn- ghost on it if it's clickable. [ ] **Netlify Routing Check**: If nav links changed (e.g. renamed "Politique d'intégration" to just "Intégration" etc.), ensure the 'href still matches the route (e.g. /politique). No change in URL structure is intended in this revamp, so keep routes same. File: TODO_theme.md - Dark/Light Mode Toggle Tasks

[ ] **Add Theme Toggle UI**: Insert a theme switch control in the nav:

Use a checkbox input (<input type="checkbox" class="toggle" /> ) or an icon button for the dark mode toggle. If using a checkbox, label it with a moon/sun icon using <label> or include an inline SVG that changes on state. [ ] **Alpine State for Theme**: In 'base.html (or a dedicated script), initialize Alpine with a theme state:

<html x-data="{ theme: localStorage.getItem('theme') || 'light' }" data- theme="theme">'. This sets 'data-theme to the saved theme or default 'light'.

[ ] **Toggle Logic**: Bind the checkbox to Alpine:

e.g. <input type="checkbox" class="toggle"

checked="theme === 'dark'"

@change="theme = \$event.target.checked? 'dark': 'light';

localStorage.setItem('theme', theme)">'. This updates the theme state and saves to localStorage whenever toggled. [ ] **Verify DaisyUI Theme Activation**: Ensure that by setting 'data-

theme="dark" on html, the site actually switches to dark colors (it should, as DaisyUI's dark theme is enabled by default 18). Check elements like background ( bg-base-100 / base-200 ) and text (text- base-content ) adapt automatically. [ ] **Icon Feedback**: Optionally, show a icon when in light mode and when in dark mode:

12

--- PAGE 13 ---

Could use <span x-show="theme==='light'"> </span><span x-

show="theme==='dark'"></span> next to the toggle, or use DaisyUI's 'data-set- theme buttons if using theme-change library. [ ] **Persist on Reload**: Confirm that if you refresh the page after toggling, the theme remains:

Because we saved in localStorage and initialized Alpine from it, it should persist. Test this in browser.

[ ] **System Prefers Dark (optional)**: If we want to default to OS preference on first load, DaisyUI already marks dark as--prefersdark by default 43.

We could detect window.matchMedia('(prefers-color-scheme: dark)') in JS and set default theme accordingly if no localStorage value. [ ] **Test Styling in Both Modes**: Manually check the site in light vs dark: Background, text, cards, navbar, etc. Should all switch to the dark theme palette (e.g., dark background, light text). If any element looks incorrect (e.g., an image with white background), consider adding a CSS or Tailwind class to handle it in dark mode (like dark: opacity-75 for overly bright images, or add DaisyUI's 'bg-neutral`). [ ] **Edge Cases**: Ensure that i18n text replacement and Alpine don't conflict:

Both Alpine and i18next operate on the DOM. They should peacefully coexist; just verify that toggling theme doesn't wipe translated text or vice versa. (Our approach is simple enough that it should be fine.)

- [ ] **Update Documentation**: Note in README or help that the site supports dark mode and how to toggle it. File: TODO_i18n.md - Internationalization (Multilingual) Tasks

[ ] **Extract French Text**: Go through all templates (*.html ) and identify all visible text content. Create a list of keys and their French strings. (E.g., nav.home =

"Accueil", 'home.mission_title = "Notre mission" etc.)

[ ] **Create Locale Files**: In 'static/assets/locales/, add `fr/ translation.json and `en/translation.json . Populate fr/translation.json with the keys and French text.

Copy it to en/translation.json and translate each value to English. Double-check special characters and punctuation are preserved (UTF-8). [ ] **Include i18next**: Add script tag for i18next in base.html (before other scripts that depend on it). E.g., <script src="https://unpkg.com/i18next@21.8.12/dist/umd/ i18next.min.js"></script> .

Pin the version as shown (21.8.12 or latest stable). [ ] **Load Translations in JS**: Write an inline script (or external js file) to initialize i18next:

Use i18next.init({...}, callback) with resources containing our two language objects (we can inline require the JSON via a small trick since we can't use import; one way is to embed JSON directly in the script as a JS

13

--- PAGE 14 ---

object). Alternatively, use 'fetch()

init i18next in the promise.

to load the JSON files asynchronously, then

Ensure Ing is set to 'fr' by default (assuming French default). Set fallbackLng to 'fr' or 'en' appropriately. In `init callback, call a function to apply translations to DOM. [ ] **Mark up HTML for i18n**: Add data-i18n="key.path" attributes to elements:

For each text element, decide a key and set the attribute. Example: <h2 data-i18n="home.values_title">Nos valeurs</h2> .

Remove the hardcoded English text from templates if present (we will rely on JS to insert it). However, keep the French text as initial content for accessibility/SEO fallback. For things like the nav links, possibly wrap each link name in a span with data-i18n, or give the <a> itself the attribute (works if we replace its innerText). [ ] **Language Switcher UI**:

Add a UI control to switch language (if not already added in nav, add it). Simple approach: two buttons or links "FR" and "EN" in the navbar or a

select dropdown.

Example: <button @click="switchLang('en')">EN</button> | <button @click="switchLang('fr')">FR</button>'.

[ ] **Switch Language Function**: Implement switchLang(lang) in a script: function switchLang(1ng) { i18next.changeLanguage (Ing); updateContent(); } updateContent() should iterate over all [data-i18n] elements and set

their innerText i18next.t(key)` for the current language. Alternatively, re-run i18next.init with new Ing, but changeLanguage is the cleaner method 44.

[ ] **Maintain Language State**: Store the chosen language in localStorage (similar to theme):

On switch, do localStorage.setItem('lang', lng). On page load, check localStorage.lang and pass that to

i18next.init({ lng: storedLang, ... })`. Also possibly reflect the UI (e.g., highlight the active language button). [ ] **Test Content Swap**: Load the page, then switch to English:

Verify all text changes to English: nav items, headings, paragraphs, button labels. Test switching back to French.

Check that special characters (accents in French) display correctly (they should, given UTF-8 JSON). [ ] **Edge Cases**: If a translation is missing for a key in a language, i18next will fallback (or show the key). Our JSON should be complete to avoid this. Instruct testers to look for any "missing key" indications. - [ ] **Integration with Frozen Site**: Ensure that the site still shows French by default if JS is disabled (since our HTML still contains French content as fallback). To confirm: disable JS in browser, the page should be in French (which is acceptable as default).

14

--- PAGE 15 ---

Ensure no untranslated English placeholders are left in the HTML. [ ] **Optimize Loading (optional)**: If flash of original language is an issue

(FOOT

flash of original text before translation), consider:

Hiding the content until i18next has applied translations (e.g., add 'style="visibility: hidden" on body and then remove in JS after translation). Or use i18next.init with initImmediate: false to perform synchronously (not usually recommended). Given our default language is French which matches the content, FOUC/FOOT is not a big problem when switching to English (the user will just see French briefly, which might be okay). - [ ] **Update Netlify Config**: If using external JSON files for translations, ensure they are in 'static/assets so they get deployed. (No changes needed if we put them under static.)

File: TODO_layout.md - Structured Sections & Responsive Design Tasks

[ ] **Section Containers**: Wrap logical sections of each page in <section>' or <div> with appropriate Tailwind/DaisyUI classes:

E.g., for "Nos valeurs" section: <section class="p-6 my-8 rounded-1g shadow-md bg-base-200">...</section> to give it padding, margin, rounded corners and a slight shadow on a tinted background. Use DaisyUI's utility classes (bg-base-200 will adapt to theme).

[ ] **Grid Layout for Values**: Instead of a vertical stack, display the 5 values (Accessibilité, Inclusion, etc.) in a responsive grid: <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">' wrapping each value's card.

Each value can be a DaisyUI **card**: '<div class="card bg-base-100"> <div class="card-body">... text ...</div> </div> . Place the icon image in the card's <figure> or at top with a suitable class. This will automatically make them nicely spaced; DaisyUI cards also have default padding. [ ] **Typography Styling**: Apply consistent typography using Tailwind: Add text-center to section titles if needed, text-justify or 'prose

class to long paragraphs (if DaisyUI Typography plugin is in effect). Ensure headings have uniform sizing (maybe text-2xl font-bold for h2s, etc.) and use DaisyUI theme colors (they default to base content color). [ ] **Spacing Adjustments**: Remove any deprecated <br> tags or non-semantic spacers in HTML and replace with Tailwind margin classes ( mb-4`, `mt-6`, etc.). For example, between subsections, use 'mt-8 on the next heading rather than empty paragraphs or <br>. - [ ] **Responsive Video/Media**: If there's an embedded video in "Découvrez NourrIR en Vidéo" (currently just a heading placeholder),

Ensure any iframe or video is wrapped in a responsive container ( aspect- video class or similar) so it scales on mobile. If no actual video, consider embedding a YouTube or using a placeholder image.

15

--- PAGE 16 ---

[ ] **Images**: All images (icons like Accessibilité, or any decorative images) should have:

- Tailwind responsive classes (max-w-xs or percentages) so they don't overflow on small screens. Meaningful alt text (already present for icons as seen in content extraction). If using DaisyUI's mask utility for shaping images (optional fun improvement). [ ] **Test Mobile Layout**: Use Chrome dev tools (or an actual device) to verify the layout on a small screen (e.g. iPhone 5SE dimensions):

Sections should stack vertically, text should be readable without zoom, no horizontal scroll. The values grid should collapse to 1 column on narrow screens (our grid- cols-1 on small will do this). The navbar should not break the layout (already handled in nav tasks). [ ] **Test Desktop Layout**: On a large screen, ensure sections don't look too stretched:

Possibly constrain content width with a container: e.g., wrap main content in <div class="max-w-4x1 mx-auto"> to limit width to a reasonable max and center it. If the design should be full-width, that's fine too; just ensure not overly sparse. - [ ] **Consistency Across Pages**: Make sure the styling approach is applied to all pages (Accueil, Politique, Contact, etc.):

- For instance, if using cards for sections on home, use similar styling on "Politique d'intégration" page sections. The contact page likely has a simpler layout ensure its content (maybe contact form or info) is also styled (maybe a card or centered text). [ ] **Footer (if any)**: If there's a footer (the 2025 Nourr IR line), style

it:
 E.g. a footer with class="footer p-4 bg-neutral text-neutral-content text- sm text-center" . Ensure it sticks to bottom if page content is short (if desired). [ ] **Remove Unused CSS**: If there's any old custom CSS in 'static/assets that is now superseded by Tailwind/DaisyUI, plan to remove it to avoid conflicts:

E.g., check if a 'style.css existed with legacy styles; migrate anything needed (like a special class) into Tailwind classes or add it to a Tailwind utility if absolutely needed. Mark this in cleanup tasks.

[ ] **Cross-Browser Check**: Verify layout in a couple of browsers (Chrome, Firefox). Tailwind/DaisyUI should be solid cross-browser. Just ensure no flex/grid gap issues in older Safari (shouldn't, since we target modern). [ ] **Update Tests**: Note in tests (if any snapshot tests or Selenium tests exist) that structure changed. If there are template tests asserting certain HTML structure, update them to match new markup.

16

--- PAGE 17 ---

File: TODO_tooltips.md - Tippy.js Tooltip Tasks

[ ] **Identify Terms for Tooltip**: Review content for jargon or nutrition/ psychology terms:

For each, draft a short explanation (1-2 sentences max). Terms identified: "dopamine" (in the tagline?), "probiotiques", "freemium",

possibly the names "NurrIA" (maybe explain it's a virtual assistant?), any others in the Features or Concept list like "IA" (ΑΙ). Compile these terms and definitions in a note.

[ ] **Add data-tippy-content***: Wrap the term or add a span around it in the HTML:

Example: replace **Probiotiques** text with <span data-tippy- content="Organismes vivants (bactéries) qui apportent un bénéfice pour la santé mentale en équilibrant le microbiote intestinal.">probiotiques</span>'. Ensure the span does not break the sentence flow and inherits styling (it will by default, but we can add cursor-help CSS so it shows a question mark cursor on hover). Do this for all terms from step above.

[ ] **Initialize Tippy in JS**: In base.html , after including Tippy scripts, add:

js

<script>

document.addEventListener('DOMContentLoaded', $()\Rightarrow\{$

tippy('[data-tippy-content]', {

theme: localStorage.getItem('theme') === 'dark'? 'dark': 'light'

});

});
</script>

This will activate all tooltips. The optional theme setting here tries to match current theme; we'll also include Tippy's default CSS which has a tippy- box [data-theme-='dark'] style. - (Ensure to include <link rel="stylesheet" href="https://unpkg.com/ tippy.js@6/dist/tippy.css""> in head, which provides default styling). - [ ] **Include Tippy Assets**: Actually add the CDN links in `base.html head/ footer:

Popper 2 script, Tippy bundle script, and Tippy CSS as detailed in the roadmap.

Verify the script tags are after i18next and before our custom scripts, or at least that no conflict (order isn't critical unless we wrap our init in DOMContentLoaded as above).

[ ] **Test Appearance**: Hover over each marked term:

- Tooltip should appear near the term with the provided content.

Check that the text fits in the tooltip (not cut off). If needed, set a maxWidth in options (e.g., { maxWidth: '250px' }).

If the tooltip obscures important content, consider different placement:

e.g., for footer or bottom page terms, maybe placement: 'top'.

17

--- PAGE 18 ---

By default Tippy positions intelligently to stay in viewport.

[ ] **Tooltip Theme Adjustments**:

In light mode, default tooltip is a dark gray box with white text this is actually fine contrast-wise. In dark mode, the default might also be dark (which might be less visible on a dark page). If we applied theme: 'dark' , then it uses the "dark" theme which is lighter text on dark background possibly similar, but let's confirm. We can explicitly include Tippy's light or dark theme CSS. Since the CDN bundle auto-injects base styles, we might manually add a small CSS:

html

<style>

.tippy-box[data-theme~='dark'] { background-color: #333; .tippy-box[data-theme~='light'] { background-color: #fff;

</style>

color: #fff; } color: #000; }

Or use their provided theme CSS via another link (they have separate CSS for themes if needed). This is optional; do it if visual testing shows a need. [ ] **Mobile Testing**: Simulate touch tap on a tooltip term:

Tippy should show on tap and hide on second tap (since tooltips on mobile act like popovers). Ensure this works and doesn't cause page scroll issues.

If tooltips are cut off on mobile, might need to make them responsive or

consider long-press behavior. But given limited usage, it should be fine. - [ ] **No JS fallback**: If JS is off, the terms will just appear normally without explanation. That's acceptable. If critical, we could also mark such terms with a subtle underline (using CSS) to hint they are defined, but not necessary. - [ ] **Performance**: The number of tooltips is small, so initializing all at once is fine. (If there were hundreds, we'd consider delegation.)

[ ] **Edge Cases**: Overlap with i18n:

If a term with tooltip gets translated to a different word in English, we need to also provide an English tooltip. This could be done by assigning keys for tooltip texts as well and using i18next for them. Simpler: since our content and tooltips are part of the content, when language switches, the HTML span (with French tooltip) might remain. Ideally, we translate the inner text and also update the tooltip content attribute. A quick solution: assign 'data-i18n-tooltip="key_for_tooltip" on the span and on language switch update those too (element.setAttribute('data-tippy- content', i18next.t(element.dataset.i18nTooltip)) then re-init or update Tippy instance). To keep it easy, we might decide tooltips only in one language (French) for now, or revisit this later. Mark this in documentation as a known limitation or an enhancement. [ ] **Tooltips in Dark Mode**: After implementing theme toggle, verify that switching theme updates tooltip theme if needed:

We may need to call something like 'document.querySelectorAll('.tippy- box').forEach(el => el.setAttribute('data-theme', newTheme)) on theme change. Alternatively, destroy and re-init tippy on theme switch (could be heavy-

18

--- PAGE 19 ---

handed).

Given tooltips are ephemeral, and default is readable on both, we might skip dynamic theming for now. Note this as a potential improvement (maybe in code comments or future issues). Continuous Integration & Testing Plan

To maintain quality during these upgrades, we will set up CI tests and a GitHub Actions workflow focusing on the static build and UI regression checks:

Build & Freeze Validation: We will create a GitHub Actions workflow (e.g. ci.yml) that runs on each push/PR. It will use a Python environment to install requirements and run Frozen-Flask to build the static site. For example:

• Use actions/checkout@v3 to get code, then actions/setup-python@v3 to install Python 3.11. • Install deps: pip install -r requirements.txt (this brings in Flask, Frozen-Flask, etc.). • Run the freeze script: if our app is structured to freeze via app.py, we might run

python app.py freeze (assuming we add a CLI flag or function to trigger Freezer). If not, we can create a small script or use flask freeze if configured. After running, ensure a build/ directory (or whichever output dir) is produced with.html files for each page. • Check Outputs: Use a simple script to verify expected files exist, e.g.: if [ -f build/ index.html]; then exit 1; fi for each main page. Also optionally check that the static assets (CSS/JS) are present (since we use CDN for most, this might just mean ensuring assets/ locales/*.json exist if used). Automated UI Tests: Once the static site is built, we can run some automated checks:

• HTML Proofer / Link Check: Run a link checker or HTML proofer on the build directory to catch broken links or missing images. For instance, use a Node script like Linkinator or html-proofer via Docker. This ensures our refactoring hasn't broken internal links or references. • Responsive Layout Test: Use a headless browser to test critical responsive behavior. We can leverage Playwright or Puppeteer for this. For example, use Playwright's GitHub Action to run tests that load the built site in two viewport sizes. Pseudocode for a Playwright test:

// In tests/test_layout.spec.js

test('Nav transforms to hamburger on mobile', async ({ page }) => {

await page.setViewportSize({ width: 320, height: 640 }); // small mobile
 await page.goto('http://localhost:5000'); // assuming we serve build/ locally

const menu = page.locator('.menu');

expect(await menu.isVisible()).toBeFalsy(); // full menu hidden
 const toggle = page.locator('button[aria-label="Toggle Menu"]');
 await toggle.click();

19

--- PAGE 20 ---

expect(await menu.isVisible()).toBeTruthy(); // menu appears after toggle

});

Similar tests can check that at a desktop width, the menu items are visible without toggle, and that theme toggle switches data-theme attribute, etc.

• Visual Regression (optional): For critical pages, take screenshots in light and dark mode and compare to baselines. There are GitHub Actions for Percy or others; or we can do a simple pixel-by- pixel diff using Puppeteer + an image comparison library. This might be overkill for now, but we mention it as a future enhancement. Given the complexity, a simpler approach is to use Cypress (which can also handle responsive testing and interactions). Cypress could run on the deployed preview or a local server. However, since this is a static site, an easy route is: after freeze, start a simple server (python -m http.server in build/ directory) and run tests against http://localhost:8000. This can be orchestrated in the CI YAML (run server in background, then run test script). Sample GitHub Actions Workflow: (Pseudo-code, not full YAML)

name: CI Build and Test

on: [push, pull_request]
 jobs:

build-and-test:

runs-on: ubuntu-latest

strategy:

matrix:

node-version: [16]

python-version: [3.11]

steps:

uses: actions/checkout@v3

name: Setup Node and Python

uses: actions/setup-node@v3

with: { node-version: ${{ matrix.node-version }} }

uses: actions/setup-python@v3

with: { python-version: ${{ matrix.python-version}} }

name: Install Python Deps

run: pip install -r requirements.txt

name: Freeze site with Frozen-Flask

run: |
python -c "from app import freezer; freezer.freeze()"
 name: Verify build output

run: ls -R build && test -f build/index.html && test -f build/politique/

index.html

name: Install Test Tools

run: npm install -D playwright@^1.30 # for example

name: Start static server

run: python -m http.server 8000-d build &

20

--- PAGE 21 ---

name: Run Playwright tests

env:

CI: true

run: npx playwright test

(This is an approximate snippet; in practice we'd include a proper Playwright configuration and tests as part of the repo. Alternatively, skip the Node part and just use Python Selenium with pytest.)

The above would ensure that on every PR, the site builds and basic UI functionality is validated. We will at minimum implement the build check and a few crucial tests (navigation toggle, presence of translated text in both languages, etc.). Netlify Preview Verification: We will use Netlify's Deploy Preview feature for each PR. Netlify will build using our netlify.toml (which should call the freezer as part of netlify deploy). To avoid build- time errors: Make sure the Netlify build command in netlify.toml is updated if we add a Tailwind build. For now, if we remain CDN, the build command might simply run a Python script to freeze. For example, we can set in netlify.toml:

[build]

command = "pip install -r requirements.txt && python -c \"from app import freezer;
freezer.freeze()\""

publish = "build"

This installs dependencies and freezes the app, outputting to build/ which Netlify will deploy 11 12.- Ensure netlify.toml also includes functions directory if needed (e.g., functions = "netlify/ functions" which we have for the chat function). - We will document environment variables (like OLLAMA_CHAT_URL) that need to be set in Netlify. The roadmap already notes to configure those 4. For previews, if those aren't set, the chat function might fail - we can either stub it (not our focus here) or ensure some safe default (perhaps the function returns an error gracefully if no backend). - After each Deploy Preview, we (or QA) should manually access the preview URL and do a quick sanity check: Toggle dark mode, switch language, hover tooltips, resize window - to catch any issues. This is in addition to automated checks.

To avoid template export errors, we should test the freeze locally with the new changes before pushing: - Run freezer.freeze() and inspect the build/ output. Common issues: missing URLs (if we forget to url_for a new route), or Frozen-Flask not capturing a page (e.g., if we introduced a dynamic route without a generator). In our case, we are not adding new Flask routes, so it should be fine. If we added a new page for English, we'd need to register it - but we're not; we handle i18n on the front-end. If Frozen- Flask complains or misses something, use freezer.register_generator for any dynamic pieces (not likely needed here). Potential freeze pitfalls: If we inadvertently use request context in Jinja for something that's only available at runtime (e.g., reading navigator.language via JS - not applicable in Jinja), it could break. We avoid that. - Another potential issue: large JS assets via CDN are fine, but if Netlify's CSP settings block them (Netlify by default doesn't block external scripts unless set in headers). We might consider adding a Content-Security-Policy meta or Netlify headers if needed, but since this is a small project,

21

--- PAGE 22 ---

probably not configured. We'll just be mindful if any CDN fails to load due to CSP; we could adjust in Netlify's settings.

Finally, include a step in CI to deploy to Netlify for master/main branch merges (if not already automated by linking repo). The netlify-cli could be used as in README instructions 4 but usually linking the repo in Netlify is easier. We will trust Netlify's built system if configured.

In summary, our CI will act as a guard to ensure that: - The site can freeze without errors, Key interactive features work (via headless browser tests), - No obvious layout issues regress (through responsive checks), - And the Netlify preview can be confidently promoted to production after review. References: Netlify Deploy Previews documentation (for team preview of changes) 45 46, Frozen-Flask usage to generate static files 11 12, DaisyUI and theme docs for potential build config adjustments 16 18

1 3 4 GitHub - ArtemisAI/nourrir_flask at NEW https://github.com/ArtemisAl/nourrir_flask/tree/NEW

2 Generating a Static Site with Flask and Deploying it to Netlify | TestDriven.io https://testdriven.io/blog/static-site-flask-and-netlify/

5

6 7 23 39 Is there a way to setup DaisyUI + TailwindCSS using NodeJS without having to use the CDN? saadeghi daisyui Discussion #3392. GitHub

https://github.com/saadeghi/daisyui/discussions/3392

8 DaisyUI: CSS Components for Tailwind - CodeParrot https://codeparrot.ai/blogs/daisyui-css-components-for-tailwind

9 10 40 41 42 Installation - Alpine.js

https://alpinejs.dev/essentials/installation

11 12 Frozen-Flask - Frozen-Flask 1.0.2 documentation https://frozen-flask.readthedocs.io/en/latest/

13 Tailwind Text Input Component - Tailwind CSS Components (version 5 update is here) https://daisyui.com/components/input/?lang=en

14 15 16 18 19 20 43 daisyUI themes - Tailwind CSS Components (version 5 update is here) https://daisyui.com/docs/themes/?lang=en

17 Tailwind Toggle Component - daisyUI https://daisyui.com/components/toggle/?lang=en

21 Anyone used next-themes to toggle the theme? #441 - GitHub https://github.com/saadeghi/daisyui/discussions/441

22 How can I change themes using daisyUI and tailwindcss in a react https://stackoverflow.com/questions/72926946/how-can-i-change-themes-using-daisyui-and-tailwindcss-in-a-react-project

24 25 26 27 28 29 30 31 Getting started | i18next documentation https://www.i18next.com/overview/getting-started

22

--- PAGE 23 ---

32 How to Localize your React App with react-i18next - i18nexus https://i18nexus.com/tutorials/react/react-i18next

33 34 35 37 Getting Started | Tippy.js https://atomiks.github.io/tippyjs/v6/getting-started/

36 38 Easily Add Tooltips to Your Webflow Projects https://www.digidop.com/blog/tooltips-webflow-tippy-js

44 How to use react-i18next to change language by different javascript ... https://stackoverflow.com/questions/59946118/how-to-use-react-i18next-to-change-language-by-different-javascript-file
45 46 Deploy Previews | Netlify Docs

https://docs.netlify.com/site-deploys/deploy-previews/

23
