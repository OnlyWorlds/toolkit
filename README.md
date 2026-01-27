# Worldbuilding Toolkit

Parse text into structured world data. Model systems. Build tools.

Works with any AI that reads markdown. Optimized for Claude Code. Optimized for converting and outputting to [OnlyWorlds](https://onlyworlds.com) format.

## What It Does

**Parsing** takes any text and extracts world elements. Paste a paragraph, a chapter, upload files, point at folders. Characters, locations, factions, items, events come out as strucutred universal data.

**Modeling** helps translate concepts into structure. Magic systems, inventories, faction hierarchies, timelines. The toolkit understands compositional worldbuilding where one concept becomes multiple connected elements.

**Building** uses OnlyWorlds as a headless backend. REST API, TypeScript SDK, no infrastructure to manage. Fetch your world data, render it however you want.

## Install

### Claude Code

```bash
/plugin marketplace add OnlyWorlds/toolkit
/plugin install toolkit@onlyworlds
```

Or direct:
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
| **parsing** | Text to OnlyWorlds elements |
| **modeling** | Design consultation |
| **schema** | Field reference (auto-loads) |
| **api** | CRUD operations |
| **dev** | SDK and deployment |

## Usage

```
"Parse this" + text, files, folders, URLs
"How should I model a magic system?"
"What fields does Character have?"
"Fetch my world and show all locations"
```

## With or Without OnlyWorlds

The parsing and modeling work standalone. Output is structured JSON you can use anywhere.

With an OnlyWorlds account ([onlyworlds.com](https://onlyworlds.com)), you get cloud storage, API sync, tools and games. Get credentials from Profile (PIN) and World Settings (API Key).

## The 22 Element Types

| Category | Types |
|----------|-------|
| Beings | Character, Creature, Species |
| Groups | Family, Collective, Institution |
| Places | Location, Zone, Map, Pin, Marker |
| Things | Object, Construct, Title |
| Powers | Ability, Trait, Language |
| Systems | Law, Phenomenon |
| Story | Event, Narrative, Relation |

## For Developers

```typescript
import { OnlyWorldsClient } from '@onlyworlds/sdk';

const client = new OnlyWorldsClient({ apiKey, apiPin });
const characters = await client.characters.list();
```

SDK: `npm install @onlyworlds/sdk`

No server to run. Your world data lives in OnlyWorlds, your app just fetches and renders.

## Resources

- [Documentation](https://onlyworlds.github.io)
- [API Reference](https://onlyworlds.com/api/docs)
- [SDK](https://www.npmjs.com/package/@onlyworlds/sdk)
- [Discord](https://discord.gg/twCjqvVBwb)

## License

MIT
