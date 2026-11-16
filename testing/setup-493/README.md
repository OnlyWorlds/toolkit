# The setup skill's tests

- `test_write_world.py` runs `skills/onlyworlds-setup/scripts/write_world.py` on every pack's test plan in every placement and checks what it writes; its header says what each test holds and what it needs.
- `plans/` holds those test plans, one per pack. A plan to copy is one of these.
- `cold-visit-checklist.md` is the list of questions test 10 holds the company pack's texts to.
- `company/`, `shape/`, `company-plan.json`, `shape-plan.json`, `company-bulk.json` and `shape-bulk.json` are the record of one trial setup on 2026-10-22, before toolkit 5.11.0: its plans and what the writer wrote then. No test reads them, and they keep that day's form (a description opening with a `Source:` line), which today's writer refuses.
