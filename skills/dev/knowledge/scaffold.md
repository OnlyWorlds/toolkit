# Quick Start Scaffold

Complete project structure for a minimal OnlyWorlds tool (TypeScript, no framework). Needs a current Node LTS (20 or 22). For a React app, use `npm create vite@latest my-app -- --template react-ts` instead (see `deployment.md`, Project Structure).

## Setup

```bash
mkdir my-ow-tool && cd my-ow-tool
npm init -y
npm pkg set type=module
npm install @onlyworlds/sdk
npm install -D vite typescript
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true
  },
  "include": ["src"]
}
```

## vite.config.ts

```typescript
import { defineConfig } from 'vite';
export default defineConfig({
  server: { port: 3000 }
});
```

## src/main.ts

```typescript
import { OwV2Client } from '@onlyworlds/sdk';

// Asked at runtime, held in memory only. This example only reads, so no PIN;
// a tool that writes also asks for the PIN here. Never put a PIN in a VITE_ variable.
const client = new OwV2Client({
  apiKey: prompt('API key (ow_r_... is enough to read):') || ''
});

async function main() {
  const world = await client.getWorld();
  const h1 = document.createElement('h1');
  h1.textContent = `Connected to: ${world.name}`;  // world text is data: textContent, never innerHTML
  document.body.append(h1);

  // listAll walks every page; list() would return only the first 100
  for await (const ch of client.listAll('character')) {
    console.log(ch.name);
  }
}

main();
```

Credential rules for deployed builds: `deployment.md` and `../../../knowledge/principles.md` §6.

## index.html

```html
<!DOCTYPE html>
<html>
<head>
  <title>My OnlyWorlds Tool</title>
  <style>body { font-family: sans-serif; padding: 2rem; }</style>
</head>
<body>
  <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

`index.html` sits at the project root. Run with `npx vite`; build with `npx vite build`.
