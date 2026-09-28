# OnlyWorlds Tool Deployment

Hosting patterns for OnlyWorlds tools. Static frontends calling the OnlyWorlds API.

## Contents
1. Architecture Pattern
2. Cloudflare Pages
3. Vercel
4. GitHub Pages
5. Credential Handling Patterns
6. Project Structure
7. CORS Notes
8. Deployment Checklist

---

## Architecture Pattern

Most OnlyWorlds tools follow this architecture:

```
┌─────────────────┐     ┌─────────────────┐
│  Static Site    │────▶│  OnlyWorlds API │
│  (your tool)    │◀────│  (hosted)       │
└─────────────────┘     └─────────────────┘
     Your host           onlyworlds.com
```

- **No backend needed.** Your tool is static HTML/JS/CSS.
- **API handles data.** OnlyWorlds stores and serves world data.
- **CORS configured.** The API accepts browser requests from common static hosts (including `*.pages.dev`) and from localhost. A custom domain is not pre-approved; see [CORS Notes](#cors-notes).

---

## Cloudflare Pages (Recommended)

Free hosting with automatic deployment from GitHub.

### Setup

1. Push your project to GitHub (can be private)
2. Go to Cloudflare Dashboard → Pages
3. Connect your GitHub repository
4. Configure build:
   - **Build command**: `npm run build`
   - **Output directory**: `dist`
5. Deploy

### Result

Your tool is live at `your-project.pages.dev`

### Environment Variables

In Cloudflare Pages dashboard → Settings → Environment variables:

```
VITE_ONLYWORLDS_API_KEY=ow_r_...
```

These are build-time variables: Vite compiles every `VITE_` variable into the public bundle. Only a read key (`ow_r_...`) belongs here, and only for a world anyone may read. Never set a PIN or a write key (`ow_w_...`, legacy 10-digit) as a build variable; a tool that writes asks the user at runtime (see Credential Handling below).

If the build fails on an old Node version, set `NODE_VERSION` to `22` in the same place.

### Custom Domains

1. Add domain in Cloudflare Pages settings
2. Set CNAME record pointing to `your-project.pages.dev`
3. Cloudflare handles SSL automatically

A custom domain is **not** on the API's CORS allowlist, so browser calls from it are refused until it is added. Request that at https://www.onlyworlds.com/feedback, or keep the tool on its `*.pages.dev` address.

---

## Vercel (Alternative)

Similar to Cloudflare Pages. Slightly different setup.

### Setup

1. Push to GitHub
2. Import project in Vercel dashboard
3. Configure:
   - **Framework**: Auto-detected or select manually
   - **Build command**: `npm run build`
   - **Output directory**: `dist`
4. Deploy

### Environment Variables

Vercel dashboard → Settings → Environment Variables

```
VITE_ONLYWORLDS_API_KEY=ow_r_...
```

Same rule as Cloudflare: a read key at most, never a PIN.

### Result

Live at `your-project.vercel.app`

---

## GitHub Pages (Alternative)

Free for public repos. Slightly more manual.

### Setup

1. Build locally: `npm run build`
2. Push `dist` folder to `gh-pages` branch (or configure in repo settings)
3. Enable GitHub Pages in repository settings

### Limitations

- Public repos only for free tier
- No server-side environment variables
- Manual or GitHub Actions for auto-deploy

### With GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

A project site is served under `/<repo-name>/`, so set `base: '/<repo-name>/'` in `vite.config.ts` or the built asset paths break.

---

## Credential Handling Patterns

The rule: a PIN never goes into a build (`../../../knowledge/principles.md` §6). Anything in a static site's bundle is readable by every visitor.

### User-Provided Credentials (tools that write)

The user enters their own key and PIN when the session starts; the tool keeps them in memory only.

```typescript
const apiKey = prompt('OnlyWorlds API key:') ?? '';
const apiPin = prompt('World PIN (needed to save changes):') ?? '';

const client = new OwV2Client({ apiKey, apiPin });
```

A real UI uses a password field rather than `prompt()`. Do not save the PIN to `localStorage`: any script on the page can read it, and it outlives the tab. If the tool remembers a credential between sessions, make it a read key.

### Build-Time Read Key (read-only tools)

For a viewer of a world that is meant to be public. Only a read key goes into the build.

```typescript
// Vite: VITE_ONLYWORLDS_API_KEY=ow_r_...
const client = new OwV2Client({ apiKey: import.meta.env.VITE_ONLYWORLDS_API_KEY });
```

Anyone inspecting the bundle can use this key to read the world, and nothing more: read keys cannot write, and prefixed keys read without a PIN.

### Hybrid Pattern

A built-in read key for browsing, with the user's own credentials asked for only when they choose to edit:

```typescript
let client = new OwV2Client({ apiKey: import.meta.env.VITE_ONLYWORLDS_API_KEY });

function enableEditing() {
  const apiKey = prompt('Your write key (ow_w_...):') ?? '';
  const apiPin = prompt('World PIN:') ?? '';
  client = new OwV2Client({ apiKey, apiPin });
}
```

---

## Project Structure

Let `npm create vite` write the project, so its Vite, React and TypeScript versions are current. It needs a current Node LTS (20 or 22). The `--template` flag skips the interactive prompts:

```bash
npm create vite@latest my-app -- --template react-ts   # or vanilla-ts for no framework
cd my-app && npm install && npm install @onlyworlds/sdk
```

`npm install @onlyworlds/sdk` records the current major (`^4.x`) in `package.json`; keep it pinned to a major, not `latest`.

```
my-app/
├── index.html          # at the project root, not in src/
├── src/
│   ├── App.tsx
│   └── main.tsx
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## CORS Notes

The API accepts browser requests from an allowlist of common static hosts, over HTTPS:

- `*.pages.dev` (Cloudflare), `*.vercel.app`, `*.netlify.app`, `*.github.io`, `*.gitlab.io`, `*.surge.sh`, `*.onrender.com`, `*.up.railway.app`, `*.fly.dev`, `*.web.app` / `*.firebaseapp.com`, `*.amplifyapp.com`, `*.herokuapp.com`, and a few online sandboxes
- `http://localhost` and `http://127.0.0.1` on any port (development)

A **custom domain is not pre-approved**: browser calls from it are refused until it is added server-side. Request it at https://www.onlyworlds.com/feedback. Scripts and servers are not affected by CORS.

---

## Deployment Checklist

- [ ] Build succeeds locally (`npm run build`)
- [ ] **Test production build locally before deploying**:
  ```bash
  npm run build
  npx serve dist
  # Open http://localhost:3000 and test all functionality
  ```
  Dev server behavior differs from production. Runtime fetches, paths, and bundling can break in dist. Always verify locally first.
- [ ] No credentials in committed code
- [ ] No PIN or write key in any `VITE_` variable or build setting: the host's build variables hold at most an `ow_r_` key, and `grep -r "ow_w_" dist/` finds nothing (that grep cannot see a legacy 10-digit key or a PIN, so check the variables themselves)
- [ ] Environment variables set in hosting platform (a read key at most)
- [ ] Test API connection after deploy
- [ ] Verify CORS works from deployed URL

---

*For SDK usage patterns, see the dev skill SKILL.md. For API operations, use the api skill.*
