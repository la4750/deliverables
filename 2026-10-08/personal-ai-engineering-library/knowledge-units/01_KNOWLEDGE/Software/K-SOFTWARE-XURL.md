# K-SOFTWARE-XURL — Raw API Access

- **Domain**: Software / General | **Type**: API / Specification
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: low | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-018（Agent Skill: xurl）| **Extracted**: 2026-10-08

## 知识正文

The shortcuts cover common operations. For anything else, use raw curl-style mode against any X API v2 endpoint:

```bash
# GET
xurl /2/users/me

# POST with JSON body
xurl -X POST /2/tweets -d '{"text":"Hello world!"}'

# DELETE / PUT / PATCH
xurl -X DELETE /2/tweets/1234567890

# Custom headers
xurl -H "Content-Type: application/json" /2/some/endpoint

# Force streaming
xurl -s /2/tweets/search/stream

# Full URLs also work
xurl https://api.x.com/2/users/me
```

---

## Provenance

- source_skill_id: `SKILL-GEN-XURL`
- source_skill_path: `/home/ubuntu/.hermes/hermes-agent/skills/social-media/xurl/SKILL.md`
- source_name: `xurl`
- original_section: `Raw API Access`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
