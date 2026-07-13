# Model and prompting guidance

Neural Codex does not install or edit Codex configuration. Review every example
against your own account, client version, approval, sandbox, network, and cost
policy.

## Model availability comes first

Do not copy `model = "gpt-5.6"` into Codex configuration solely because an
OpenAI API or ChatGPT guide discusses GPT-5.6. Model availability differs by
product, account, and client version.

The live plugin exercise on Codex CLI 0.142.5 with ChatGPT authentication
rejected that model ID with:

```text
The 'gpt-5.6' model is not supported when using Codex with a ChatGPT account.
```

With no model override, the same Codex client selected an available model and
completed the full Neural Codex workflow. Prefer the client default or a model
explicitly surfaced by your Codex installation. API model access does not imply
Codex client access.

## Balanced Codex policy

This example intentionally leaves `model` unset:

```toml
model_reasoning_effort = "medium"
model_reasoning_summary = "auto"
model_verbosity = "medium"
approval_policy = "on-request"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = false
```

## Task-based adjustments

| Work | Reasoning | Verbosity | Notes |
|---|---|---|---|
| Mechanical, well-specified edit | `low` | `low` | Keep acceptance narrow and run tests. |
| Normal feature or refactor | `medium` | `medium` | Recommended general starting point. |
| Architecture, security, difficult debugging | `high` or `xhigh` | `medium` | Pair with explicit invariants and independent review. |

Reasoning effort is not permission. Approval and sandbox boundaries should be
chosen independently of model capability.

## GPT-5.6 prompting principles

OpenAI's newest-model guidance is still useful for structuring work even when a
specific model ID is unavailable in Codex. Prefer:

1. a concrete outcome and scope;
2. repository evidence and current constraints;
3. explicit authority and forbidden side effects;
4. executable acceptance criteria;
5. a clear stopping condition.

The five Neural Codex skills encode this structure in durable artifacts. Avoid
duplicating the full plan in every message; point Codex at the source-of-truth
artifact and record material amendments there.

Verify current behavior against the official [Codex configuration reference](https://developers.openai.com/codex/config-reference/),
[OpenAI model catalog](https://developers.openai.com/api/docs/models/), and
[newest-model guide](https://developers.openai.com/api/docs/guides/latest-model/)
before adopting a model ID in a managed environment.
