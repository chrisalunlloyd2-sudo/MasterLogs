# 📋 MasterLogs

Centralized system logs, dependency trees, runtime errors, debug traces, KV snapshots, keyword lists, LoRA updates — auto-populated nightly by Aegis dream engine.

## Structure

```
MasterLogs/
├── docs/           # Auto-generated documentation from dream rounds
├── projects/       # Per-project dependency trees, runtime errors, debug logs
│   ├── ViperKernel/
│   ├── MoeGUI/
│   ├── GeneticFoundry/
│   └── ...
├── logs/           # System logs, heartbeat traces, error dumps
├── kv_snapshots/   # SOV KV store snapshots (big blocks)
├── keywords/       # Global keyword lists, KG node dumps
├── lora/           # LoRA training checkpoints and update history
└── gists/          # Gist wall — snippets, logit keystrokes, everything
```

## Gist Wall

Every snippet, logit entry, keystroke trace, and debug output gets posted as a GitHub Gist and linked here. The gist wall in the lakehouse displays them as scrolling terminals.

## Auto-Population

Nightly dream rounds:
1. Pull dependency trees from all repos
2. Collect runtime errors from GitHub Actions
3. Snapshot KV store and keyword lists
4. Log LoRA training checkpoints
5. Push to MasterLogs with commit messages
6. Create gists for all new entries

## Lakehouse Room

A server room / archive vault in the Mind Palace with:
- Wall-sized scrolling log displays
- Filing cabinets labeled by project
- Gist wall with live snippet feeds
- Big dream pages pinned to walls
