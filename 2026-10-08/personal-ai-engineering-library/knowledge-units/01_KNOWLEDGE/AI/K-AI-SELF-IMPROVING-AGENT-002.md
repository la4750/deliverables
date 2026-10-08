# K-AI-SELF-IMPROVING-AGENT-002 — Evolution Priority Matrix

- **Domain**: AI / AI | **Type**: Troubleshooting
- **Version scope**: 未标注（通识） | **Technology**: general
- **Confidence**: medium | **Status**: Candidate | **Validation**: UNVALIDATED
- **Source**: SRC-SKILL-038（Agent Skill: self-improving-agent）| **Extracted**: 2026-10-08

## 知识正文

Trigger evolution when new reusable knowledge appears:

| Trigger | Target Skill | Priority | Action |
|---------|--------------|----------|--------|
| New PRD pattern discovered | prd-planner | High | Add to quality checklist |
| Architecture tradeoff clarified | architecting-solutions | High | Add to decision patterns |
| API design rule learned | api-designer | High | Update template |
| Debugging fix discovered | debugger | High | Add to anti-patterns |
| Review checklist gap | code-reviewer | High | Add checklist item |
| Perf/security insight | performance-engineer, security-auditor | High | Add to patterns |
| UI/UX spec issue | prd-planner, architecting-solutions | High | Add visual spec requirements |
| React/state pattern | debugger, refactoring-specialist | Medium | Add to patterns |
| Test strategy improvement | test-automator, qa-expert | Medium | Update approach |
| CI/deploy fix | deployment-engineer | Medium | Add to troubleshooting |

## Provenance

- source_skill_id: `SKILL-AI-SELF-IMPROVING-AGENT`
- source_skill_path: `/home/ubuntu/ai-heritage-library/workspace/Agent/game-series/skills/self-improving-agent/SKILL.md`
- source_name: `self-improving-agent`
- original_section: `Evolution Priority Matrix`
- source_type: Agent Skill (internal, Tier 4)
- extraction_date: 2026-10-08
- version_scope: N/A
