# Neural Codex architecture

Neural Codex has two layers: a repository marketplace and one installable
plugin. This mirrors Codex's current distribution model and keeps authoring,
installation, and runtime paths unambiguous.

```text
repository
├── .agents/plugins/marketplace.json
└── plugins/neural-codex
    ├── .codex-plugin/plugin.json
    ├── skills
    │   ├── discover
    │   ├── spec
    │   ├── craft
    │   ├── vet
    │   └── exercise
    └── hooks
        ├── hooks.json
        └── *.py
```

## Marketplace boundary

`.agents/plugins/marketplace.json` is the catalog entry Codex adds from this
repository. Its local source path is `./plugins/neural-codex`; installation and
authentication policies are explicit.

## Plugin boundary

The manifest identifies the package and points only to `./skills/`. Codex
auto-discovers the conventional `hooks/hooks.json`, so the manifest does not
duplicate that path. All manifest paths are relative, begin with `./`, and stay
inside the plugin root.

## Workflow boundary

The five skills have intentionally different authority:

1. `$discover` gathers unknowns and stops.
2. `$spec` writes an approvable contract and stops.
3. `$craft` implements only an approved contract.
4. `$vet` evaluates in fresh context and returns `SHIP` or `HOLD`.
5. `$exercise` runs tests and drives observable user behavior.

No skill silently collapses planning, implementation, review, and exercise into
one self-certifying step.

## Hook boundary

Hook commands resolve their handlers through `${PLUGIN_ROOT}`. They do not
assume the user's current repository contains Neural Codex. Handler code uses
the Python standard library, receives JSON on stdin, and emits Codex-compatible
stdout/stderr and exit codes.

Hooks remain untrusted until the user reviews them. They complement Codex
approval and sandbox policy; they do not replace either boundary.

## Configuration boundary

The plugin never changes model, reasoning effort, approvals, sandbox policy,
network policy, MCP servers, or global configuration. `docs/CONFIGURATION.md`
contains examples only, which keeps installation reversible and policy-neutral.
