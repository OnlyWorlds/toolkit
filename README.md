# Worldbuilding Toolkit

Structure, organize, and build with your worlds. Powered by [OnlyWorlds](https://onlyworlds.com), an open standard for worldbuilding data.

Works with any AI that reads markdown. Optimized for Claude Code.

## What It Does

**Structure** — Parse any text into world elements. Paste a paragraph, a chapter, upload files, point at folders. Out comes structured JSON across 22 element types.

**Organize** — Connect to your world and manage it. Browse elements, clean up descriptions, design complex systems (magic, stories, timelines), export data.

**Build** — Use OnlyWorlds as a headless backend. REST API, TypeScript SDK, no infrastructure to manage.

## Install

### Claude Code

```bash
/plugin marketplace add OnlyWorlds/toolkit
/plugin install toolkit@onlyworlds
# Restart Claude Code to load
```

Or direct (no restart needed):
```bash
git clone https://github.com/OnlyWorlds/toolkit
claude --plugin-dir ./toolkit
```

### Other AIs

Point at the knowledge files:

- [onlyworlds-core.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/onlyworlds-core.md)
- [modeling-patterns.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/modeling-patterns.md)
- [schema-reference.md](https://raw.githubusercontent.com/OnlyWorlds/toolkit/main/knowledge/schema-reference.md)

## Skills

| Skill | Purpose |
|-------|---------|
| **onlyworlds-start** | Entry point — understands your situation, routes you forward |
| **parsing** | Text, files, or folders → structured OnlyWorlds elements |
| **modeling** | Design consultation for complex world systems |
| **schema** | Field reference across all 22 types |
| **api** | Fetch, create, update, delete — natural language CRUD |
| **dev** | SDK integration, project scaffolding, deployment |
| **project-setup** | Connect to an OnlyWorlds world (runs automatically when needed) |

## Usage

```
"I want to organize my world"
"Parse this" + text, files, folders
"How should I model a magic system?"
"What fields does Character have?"
"Fetch all my locations"
"I'm building a game with world data"
```

## With or Without an Account

Parsing, modeling, and schema work standalone — no account needed. Output is structured JSON you can use anywhere.

With a free OnlyWorlds account ([onlyworlds.com](https://onlyworlds.com)), you get cloud storage, API access, visual tools, and the growing ecosystem of apps and games. The toolkit connects to your world automatically.

## Resources

- [Documentation](https://onlyworlds.github.io)
- [API Reference](https://onlyworlds.com/api/docs)
- [SDK](https://www.npmjs.com/package/@onlyworlds/sdk)
- [Discord](https://discord.gg/twCjqvVBwb)

## License

MIT
