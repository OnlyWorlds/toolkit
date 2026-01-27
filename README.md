# OnlyWorlds Toolkit

Claude Code / local AI plugin for [OnlyWorlds](https://onlyworlds.com) - the open worldbuilding standard.

Parse text into structured world data. Get design help modeling your world. Build tools with the SDK. Manage worlds via API.

## Installation

```bash
git clone https://github.com/OnlyWorlds/toolkit
claude --plugin-dir ./toolkit
```

## Skills

**`/onlyworlds:parsing`** - Convert any text into OnlyWorlds elements. Paste a chapter, get structured JSON.

**`/onlyworlds:modeling`** - Design consultation. "How do I represent a magic system?" Get help translating concepts into OnlyWorlds structure.

**`/onlyworlds:api`** - Create, read, update, delete world elements. Sync parsed data to your world.

**`/onlyworlds:dev`** - Build OnlyWorlds tools. SDK setup, project scaffolding, deployment.

**schema** *(automatic)* - Field reference. AI loads this when answering schema questions or validating data.

## Try It

```
"Parse this into OnlyWorlds" + paste your worldbuilding text, files, folders, links
"How should I model a magic system?"
"What fields does Character have?"
"I want to build a journey tracker"
"I have a world in a game.."
```

## Setup (for API features)

1. Sign in at [onlyworlds.com](https://onlyworlds.com)
2. Get your PIN from Profile
3. Get your API Key from World Settings

## Resources

- [Documentation](https://onlyworlds.github.io)
- [API Docs](https://onlyworlds.com/api/docs)
- [SDK](https://www.npmjs.com/package/@onlyworlds/sdk): `npm install @onlyworlds/sdk`
- [Discord](https://discord.gg/twCjqvVBwb)

## For Other AIs

The knowledge files work with any markdown-capable AI:

- [onlyworlds-core.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/onlyworlds-core.md)
- [schema-reference.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/schema-reference.md)
- [modeling-patterns.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/modeling-patterns.md)

## License

MIT
