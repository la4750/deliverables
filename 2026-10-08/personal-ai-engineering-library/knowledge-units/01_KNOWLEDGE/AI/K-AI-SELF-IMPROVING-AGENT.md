# K-AI-SELF-IMPROVING-AGENT — Pattern-Key Taxonomy

- **Domain**: AI / AI | **Type**: Pattern
- **Version scope**: 未标注（通识） | **Technology**: Python
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-027（Agent Skill: self-improving-agent）| **Extracted**: 2026-10-08

## 知识正文

`Pattern-Key` is the stable dedup and recurrence key for entries in all three
log files: keyword grep misses semantically identical but differently-worded
entries, a shared key does not — and reliable keys are what make
`Recurrence-Count` and the promotion rule work.

**Format**: `area.symptom` — exactly two levels, lowercase, hyphenated
(e.g. `deps.module-not-found`). Keep symptoms generic enough to recur: no
file names, versions, or hostnames in keys.

| Area | Scope | Example Keys |
|------|-------|--------------|
| `api` | External API/service behavior | `api.rate-limit`, `api.schema-mismatch`, `api.missing-endpoint` |
| `auth` | Credentials, tokens, scopes | `auth.token-expired`, `auth.missing-scope` |
| `build` | Compilation, bundling, CI | `build.type-error`, `build.missing-artifact` |
| `config` | Config files, env vars, settings | `config.missing-env`, `config.invalid-json` |
| `deps` | Package managers, dependencies | `deps.module-not-found`, `deps.npm-error`, `deps.version-conflict` |
| `fs` | Filesystem | `fs.no-such-file`, `fs.permission-denied` |
| `net` | Network connectivity | `net.connection-refused`, `net.timeout` |
| `runtime` | Language/runtime errors not covered above | `runtime.type-error`, `runtime.python-exception` |
| `shell` | Shell/CLI mechanics | `shell.command-not-found`, `shell.nonzero-exit` |
| `vcs` | Git and other version control | `vcs.fatal-error`, `vcs.merge-conflict` |
| `simplify` / `harden` | Code-quality patterns from the simplify-and-harden feed | `simplify.dead_code`, `harden.input_validation` |

**Rules:**

1. **Reuse before minting**: `grep -rh "Pattern-Key:" .learnings/ | sort -u` —
   a near-match beats a new key.
2. **One key per manual entry**; auto-swept OpenClaw entries may carry
   several — reduce to one when triaging.
3. **Mint new areas sparingly** — only when several entries would share one.
4. **Generic sweep keys** (`runtime.error`, `runtime.failure`) mean
   "unclassified" — replace with a specific key during triage.

## Provenance

- source_skill_id: `SKILL-AI-SELF-IMPROVING-AGENT-3`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/skills/@pskoett/self-improving-agent/SKILL.md`
- source_name: `self-improving-agent`
- original_section: `Pattern-Key Taxonomy`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
