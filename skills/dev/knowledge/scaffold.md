# Quick Start Scaffold

Complete project structure for an OnlyWorlds tool.

## Setup

```bash
mkdir my-ow-tool && cd my-ow-tool
npm init -y
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
import { OnlyWorldsClient } from '@onlyworlds/sdk';

const client = new OnlyWorldsClient({
  apiKey: prompt('API Key:') || '',
  apiPin: prompt('API PIN:') || ''
});

async function main() {
  const world = await client.worlds.get();
  document.body.innerHTML = `<h1>Connected to: ${world.name}</h1>`;

  const characters = await client.characters.list();
  console.log('Characters:', characters.results);
}

main();
```

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

Run with `npx vite` — building on OnlyWorlds data in under a minute.
