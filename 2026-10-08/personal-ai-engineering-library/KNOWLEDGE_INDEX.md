# Knowledge Index

> Status: ACTIVE — Phase 4（BATCH2 Skill→Knowledge Ingestion 完成）
> Knowledge Unit count: 57 | Source count: 46 | Queue count: 2
> Machine registry: `_REGISTRY/KNOWLEDGE_REGISTRY.yaml`
> Rules: `KNOWLEDGE_RULES.md` | Spec: `KNOWLEDGE_INGESTION_SPEC.md`

检索维度（Spec §19）：
Domain / Topic / Technology / Version / Confidence / Source / Capability / Project

---

## By Domain
## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|---|---:|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |

## By Confidence
## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|---|---:|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |

## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |

## Knowledge Units
## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|---|---|---|---|---|---|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |
|## By Status

| Status | Count |
|---|---:|
| Candidate | 24 |
| Ingesting | 0 |
| Reviewed | 7 |
| Validated | 0 |
| Active | 0 |
| Deprecated | 0 |
| REJECTED | 26 |

内容文件：Godot/Unity/Unreal → `02_GAME_ENGINES/<Engine>/Knowledge/`（Engine Isolation §9）；其余 → `01_KNOWLEDGE/<Domain>/`

---

## AI Retrieval 要求（Spec §20）

AI 不应"读取整个 Knowledge Library"，而应走管线：

```
用户需求 → Task Classification → Knowledge Retrieval → Capability Retrieval
→ Dependency Retrieval → Implementation Retrieval → Execution
```

Knowledge Retrieval 必须支持：关键词、语义、Domain、Version、Source、Confidence、Related Capability。
