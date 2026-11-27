# A world through a lens

How a tool shows a world through a lens, and reads the world's door, with the packages' readers.
Open it when a tool resolves a lens or a Charter; a plain read of a world needs only `../SKILL.md`.

## A World Through a Lens

A tool that shows a world through a lens (a saved reading: a Construct with supertype `Lens`, its links the anchors, its `x_lens` the recipe) resolves it with the package, never with its own walk: `resolveLens(world, lens, reader, { asOf, clock })` in the SDK, `resolve_lens(world, lens, reader, as_of=None, clock=None)` in the Python package, beside `isLens`, `isTemplate`, `lensesInUse` and `worldGraph` for the lens's reading as nodes and edges (snake case in Python). The reader is one pure function over the reader's own view of the world: it never writes, never reaches past what that reader may see, and reports what it cut as counts by reason, the owner-only reasons left out for everyone else. The world's door is read the same way: `charterOf(world, reader)` answers the Charter, the Guide and the Domains, the elements carrying the mark `x_charter_of` (`profiles/charter.md`). Never write `x_served_trimmed` on a lens; the server sets it. A reader of your own conforms only when it passes every case in `lens.fixture.json`, beside the profile: `profiles/lens.md` in github.com/OnlyWorlds/schema-dist. The package version that carries a reader is one you read from npm or PyPI this session.
