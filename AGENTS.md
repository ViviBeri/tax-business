# Agent instructions

## 21st.dev component discovery

The 21st.dev CLI is the preferred component-discovery tool for UI work in this repository when it can provide a useful reference.

- Search before designing a substantial UI component: `21st search "<component or interaction>"`.
- Inspect the selected component and its dependencies before adapting it.
- This repository is a static HTML/CSS/JavaScript website built with `_builder/build.py`; it is not a React, Next.js, or Vite application.
- Do not add React, Next.js, Vite, or a framework runtime just to consume a 21st.dev component.
- Adapt useful patterns into the existing HTML/CSS/JavaScript architecture, preserve the English and Tamil pages, and keep generated pages builder-owned.
- Preserve existing design tokens, responsive behavior, accessibility, SEO, privacy disclosures, and working contact links.
- Review the full diff and run the site builder plus relevant checks before publishing.

## Authentication and secrets

- Run `bash scripts/setup-21st.sh` from the repository root for the interactive one-time CLI and skill setup.
- The interactive `21st login` stores credentials locally; never commit its token or credential files.
- For automation only, provide `API_KEY_21ST` as a GitHub Actions secret/environment variable and pass it as `--api-key "$API_KEY_21ST"`. Never hardcode or print the key.
- Do not add a CI workflow that calls 21st unless a workflow genuinely needs component retrieval.
