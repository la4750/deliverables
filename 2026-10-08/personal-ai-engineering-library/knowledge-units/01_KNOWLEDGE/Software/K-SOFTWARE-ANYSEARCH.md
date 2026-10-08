# K-SOFTWARE-ANYSEARCH — Scenarios

- **Domain**: Software / General | **Type**: API / Specification
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-026（Agent Skill: anysearch）| **Extracted**: 2026-10-08

## 知识正文

| Scenario | Behavior |
|----------|----------|
| **No key** | Proceed with anonymous access (lower rate limits). Optionally inform the user that a key provides higher limits. |
| **Has key** | Key is sent via `Authorization: Bearer <key>` header. Higher rate limits. |
| **Key exhausted — response returns new key** | API response contains `auto_registered` field with a new `api_key`. Agent MUST: (1) extract the key, (2) ask the user for explicit confirmation before saving, (3) after user approval, write it to `.env` file, (4) retry the failed call. |
| **Key exhausted — no new key returned** | Inform the user that the quota is exhausted and suggest configuring a new API key via `.env` or environment variable. |

**Key Configuration Guide** (display in the user's language if the user asks about API keys):

> **Optional: Configure an AnySearch API Key for higher rate limits.**
>
> To configure a key:
> 1. Visit https://anysearch.com/console/api-keys to create a free API key
> 2. Add it to your `.env` file: `ANYSEARCH_API_KEY=<your_api_key_here>`
> 3. Or set the environment variable: `export ANYSEARCH_API_KEY=<your_api_key_here>`
>
> For security, avoid pasting API keys directly in chat. Anonymous access remains available with lower limits.

## Provenance

- source_skill_id: `SKILL-GEN-ANYSEARCH`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/Agent/scholar-series/skills/anysearch/SKILL.md`
- source_name: `anysearch`
- original_section: `Scenarios`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
