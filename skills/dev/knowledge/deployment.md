# OnlyWorlds Tool Deployment

Hosting patterns for OnlyWorlds tools. Static frontends calling the OnlyWorlds API.

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
- **CORS configured.** OnlyWorlds allows requests from `*.pages.dev` and common hosts.

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
VITE_ONLYWORLDS_API_KEY=your-key
VITE_ONLYWORLDS_API_PIN=your-pin
```

Note: These are build-time variables. For client-side apps, consider whether you want keys in the bundle or prompted from users.

### Custom Domains

1. Add domain in Cloudflare Pages settings
2. Set CNAME record pointing to `your-project.pages.dev`
3. Cloudflare handles SSL automatically

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
VITE_ONLYWORLDS_API_KEY=your-key
VITE_ONLYWORLDS_API_PIN=your-pin
```

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
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist
```

---

## Credential Handling Patterns

### User-Provided Credentials

Safest for shared tools. User enters their own API key and PIN.

```typescript
// Prompt or load from localStorage
const apiKey = localStorage.getItem('ow_api_key') || prompt('API Key:');
const apiPin = localStorage.getItem('ow_api_pin') || prompt('API PIN:');

const client = new OnlyWorldsClient({ apiKey, apiPin });
```

### Build-Time Credentials

For personal tools or demos. Key baked into build.

```typescript
// Vite
const client = new OnlyWorldsClient({
  apiKey: import.meta.env.VITE_ONLYWORLDS_API_KEY,
  apiPin: import.meta.env.VITE_ONLYWORLDS_API_PIN
});
```

**Warning**: Anyone inspecting your JS bundle can see these credentials. Only use for your own worlds.

### Hybrid Pattern

Build-time default with override capability:

```typescript
const apiKey = localStorage.getItem('ow_api_key')
  || import.meta.env.VITE_ONLYWORLDS_API_KEY;
const apiPin = localStorage.getItem('ow_api_pin')
  || import.meta.env.VITE_ONLYWORLDS_API_PIN;
```

---

## Project Structure Recommendations

### Minimal TypeScript Project

```
my-ow-tool/
├── src/
│   ├── main.ts
│   └── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── .gitignore
```

**package.json essentials**:
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "@onlyworlds/sdk": "latest"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "typescript": "^5.0.0"
  }
}
```

### With React

```
my-ow-tool/
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   └── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

Add React deps:
```json
{
  "dependencies": {
    "@onlyworlds/sdk": "latest",
    "react": "^18.0.0",
    "react-dom": "^18.0.0"
  }
}
```

---

## CORS Notes

OnlyWorlds API accepts requests from:

- `*.pages.dev` (Cloudflare)
- `*.vercel.app` (Vercel)
- `*.netlify.app` (Netlify)
- `localhost:*` (development)

If deploying elsewhere, requests should still work for most common patterns. If you hit CORS issues, the OnlyWorlds Discord can help.

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
- [ ] Environment variables set in hosting platform
- [ ] Test API connection after deploy
- [ ] Verify CORS works from deployed URL

---

*For SDK usage patterns, see the dev skill SKILL.md. For API operations, use the api skill.*
