# Internationalization (Multilingual) Tasks

 - [x] **Extract Text Keys**: Identify all visible text in templates (`*.html`) and map to key-value pairs (e.g., `home.title = "Accueil"`).

 - [x] **Create Locale Files**: Add `static/assets/locales/fr/translation.json` and `static/assets/locales/en/translation.json`. Populate with French and English translations.

 - [x] **Include i18next**: Add in `base.html`:
   ```html
   <script src="https://unpkg.com/i18next@21.8.12/dist/umd/i18next.min.js"></script>
   ```
   Pin the version to avoid breaking changes.

 - [x] **Load Translations in JS**: Initialize i18next with resources or fetch JSON files:
   ```js
   i18next.init({
     lng: localStorage.getItem('lang') || 'fr',
     resources: {
       fr: { translation: {/* ... */} },
       en: { translation: {/* ... */} }
     }
   }, () => updateContent());
   ```
   Implement `updateContent()` to replace elements with `data-i18n` attributes.

 - [x] **Mark Up HTML for i18n**: Add `data-i18n="key.path"` to elements. Keep French text in HTML as fallback.

 - [x] **Language Switcher UI**: Add buttons or a select in the nav:
   ```html
   <button @click="switchLang('en')">EN</button>
   <button @click="switchLang('fr')">FR</button>
   ```

 - [x] **Switch Language Function**: Implement in JS:
   ```js
   function switchLang(lng) {
     i18next.changeLanguage(lng);
     localStorage.setItem('lang', lng);
     updateContent();
   }
   ```

 - [x] **Maintain Language State**: Use `localStorage` to persist chosen language and initialize i18next from it on load.

 - [ ] **Test Content Swap**: Verify translations on switch and on page reload, including menu items, headings, and buttons.

 - [x] **Edge Cases & Fallback**: Ensure no missing keys; translation fallback works. With JS disabled, the site should display French by default.

 - [ ] **Update Netlify Config**: Ensure locale JSON files under `static/assets/locales` are deployed (no changes needed if placed correctly).