# Digital Thread

The planned SQLite/JSON graph will track:

```text
requirement → assumption/source → load case → geometry revision → CAD feature
→ PMI characteristic → analysis model/extraction → margin → inspection plan
→ measurement → NCR → disposition/RCCA → revised configuration
```

Each node receives a stable ID and content hash. Dependency impact analysis will mark downstream evidence stale when an upstream revision changes.
