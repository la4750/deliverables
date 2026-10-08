# K-SOFTWARE-OSS-FORENSICS — API Rate Limiting

- **Domain**: Software / General | **Type**: API / Specification
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-016（Agent Skill: oss-forensics）| **Extracted**: 2026-10-08

## 知识正文

GitHub REST API enforces rate limits that will interrupt large investigations if not managed.

**Authenticated requests**: 5,000/hour (requires `GITHUB_TOKEN` env var or `gh` CLI auth)
**Unauthenticated requests**: 60/hour (unusable for investigations)

**Best practices**:
- Always authenticate: `export GITHUB_TOKEN=ghp_...` or use `gh` CLI (auto-authenticates)
- Use conditional requests (`If-None-Match` / `If-Modified-Since` headers) to avoid consuming quota on unchanged data
- For paginated endpoints, fetch all pages in sequence — don't parallelize against the same endpoint
- Check `X-RateLimit-Remaining` header; if below 100, pause for `X-RateLimit-Reset` timestamp
- BigQuery has its own quotas (10 TiB/day free tier) — always dry-run first
- Wayback Machine CDX API: no formal rate limit, but be courteous (1-2 req/sec max)

If rate-limited mid-investigation, record the partial results in the evidence store and note the limitation in the report.

---

## Provenance

- source_skill_id: `SKILL-GEN-OSS-FORENSICS`
- source_skill_path: `/home/ubuntu/.hermes/hermes-agent/optional-skills/security/oss-forensics/SKILL.md`
- source_name: `oss-forensics`
- original_section: `API Rate Limiting`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
