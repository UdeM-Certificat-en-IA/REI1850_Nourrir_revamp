<!--
This document provides instructions for the Codex AI agent.
Please read this file before proceeding with any code changes.
Instructions on solving bugs will be added below. Once the fixes are fully implemented,
remove the entire contents of this file (including this comment block) before creating the Pull Request.
-->
# Codex AI Agent Instructions

## Objectives
- Ensure all integrations are functioning correctly.
- Implement rigorous tests for new features and regression tests to confirm no existing functionality is broken.

## Known Issues & Proposed Solutions

### 1. Missing DaisyUI
- **Description**: DaisyUI components are not available; the package is not installed or configured.
- **Proposed Solution**:
  1. Add DaisyUI to the project dependencies: `npm install daisyui`
  2. Update `tailwind.config.js` to include the DaisyUI plugin:
     ```js
     module.exports = {
       // ...existing config
       plugins: [require('daisyui')],
     }
     ```
  3. Import DaisyUI styles in the main CSS entry point if needed.

### 2. Main Menu Transition Issues
- **Description**: The main menu transitions (open/close animations) are not smooth or are not triggering correctly.
- **Proposed Solution**:
  1. Verify Tailwind CSS transition classes on the menu elements (e.g., `transition-all`, `duration-300`).
  2. Ensure state changes (e.g., toggling a boolean for `open`) are properly bound to class changes.
  3. Add automated UI tests (using Playwright or Cypress) to open/close the menu and assert transition states.

## Next Steps
1. Implement the above fixes.
2. Write or update unit, integration, and end-to-end tests covering these areas.
3. Run all tests and ensure the CI pipeline passes.
4. Remove this file entirely before submitting your Pull Request.

## Validation Commands
- Install dependencies: `npm install`
- Run style checks: `npm run lint`
- Run unit tests: `npm run test`
- Run backend tests: `pytest`
- (Optional) Run end-to-end tests: `npm run e2e`