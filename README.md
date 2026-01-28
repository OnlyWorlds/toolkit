# Worldbuilding Toolkit

Claude Code / local AI plugin for [OnlyWorlds](https://onlyworlds.com), an [open worldbuilding standard](https://explorer.onlyworlds.com).

Works with any AI that reads markdown. Optimized for Claude Code. Optimized for converting and outputting to [OnlyWorlds](https://onlyworlds.com) format.

## What It Does

Expert worldbuilding support: not to build your worlds for you, but to manage data, develop tools, and make full use of the OnlyWorlds universal standard with specializd skills:

**Parsing** takes any text and extracts world elements. Paste a paragraph, a chapter, upload files, point at folders.  

**Modeling** helps translate concepts into structure. Magic systems, inventories, faction hierarchies, timelines.  

**Building** uses OnlyWorlds as a headless backend. REST API, TypeScript SDK, no infrastructure to manage.  

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
| **parsing** | Text (or files, links) to OnlyWorlds elements |
| **modeling** | Design consultation, data mapping |
| **schema** | Field reference (auto-loads) |
| **api** | CRUD operations through natural language |
| **dev** | development, SDK integration, and deployment |

## Usage

```
"Parse this" + text, files, folders, URLs
"How should I model a magic system?"
"What fields does Character have?"
"Fetch my world and show all locations"
"I am making a game with a world.."
```

## With or Without OnlyWorlds

The parsing and modeling work standalone. Output is structured JSON you can use anywhere.

With an OnlyWorlds account ([onlyworlds.com](https://onlyworlds.com)), you get cloud storage, API sync, tools and games. Get credentials from Profile (PIN) and World Settings (API Key).

## Resources

- [Documentation](https://onlyworlds.github.io)
- [API Reference](https://onlyworlds.com/api/docs)
- [SDK](https://www.npmjs.com/package/@onlyworlds/sdk)
- [Discord](https://discord.gg/twCjqvVBwb)

## License

MIT
