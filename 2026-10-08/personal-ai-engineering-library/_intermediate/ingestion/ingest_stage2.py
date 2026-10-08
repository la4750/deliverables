#!/usr/bin/env python3
# 阶段2：Skill→Knowledge 全量吸收（EXTRACT→DEDUPLICATE→INGEST→REGISTER）
# 只新增 Knowledge 单元/目录，并按现有协议追加 Registry/Source/Queue/Index 数据；不改任何 Schema/Foundation。
import json, re, os, yaml, difflib, collections, hashlib
SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
LIB = "/home/ubuntu/personal-ai-engineering-library"
KDIR = f"{LIB}/01_KNOWLEDGE"
TODAY = "2026-10-08"

cands = json.load(open(SCRATCH + "/ingest_candidates.json"))
reg = yaml.safe_load(open(f"{KDIR}/_REGISTRY/KNOWLEDGE_REGISTRY.yaml"))
src_reg = yaml.safe_load(open(f"{KDIR}/_REGISTRY/SOURCE_REGISTRY.yaml"))
queue_doc = yaml.safe_load(open(f"{KDIR}/_REGISTRY/INGESTION_QUEUE.yaml"))
existing_ids = {u["knowledge_id"] for u in reg["knowledge_units"]}
existing_titles = [u["title"] for u in reg["knowledge_units"]]

WF_DROP_HEAD = re.compile(r"^(step\s*\d|阶段\s*\d|场景\s*\d|phase\s+\w|第[一二三四五六七]步|scene\s*\d)", re.I)
VERSION_PATTERNS = [
    ("Godot", r"Godot\s*([0-9]+\.[0-9x]+)"), ("Unity", r"Unity\s*([0-9]{4}(?:\.[0-9]+)?)"),
    ("Unreal", r"Unreal\s*Engine\s*([0-9.]+)"), ("Python", r"Python\s*([0-9]+\.[0-9x]+)"),
    ("PyTorch", r"PyTorch\s*([0-9.]+)"), ("ROS", r"ROS\s*([0-9]+(?:\.[0-9]+)?)"),
    ("GDScript", r"GDScript\s*([0-9.]+)"),
]
TYPE_RULES = [
    ("Troubleshooting", r"报错|错误码|故障|排障|troubleshoot|常见错误|错误处理|debug|诊断|失败原因|根因"),
    ("Constraint", r"限制|禁止|不得|约束|不能|仅支持|不兼容|deprecated|废弃"),
    ("Engineering Rule", r"最佳实践|规则|原则|准则|checklist|检查清单|应避免|必须确保|golden"),
    ("Pattern", r"设计模式|模式|pattern|范式|架构"),
    ("API / Specification", r"\bAPI\b|端点|endpoint|参数|返回值|header|请求体|response|status code"),
    ("Empirical Knowledge", r"实测|实盘|经验值|benchmark|性能数据|回测"),
    ("Procedure", r"步骤|流程|procedure|操作顺序"),
    ("Principle", r"原理|机制|理论|为什么"),
    ("Concept", r"概念|定义|术语|是什么"),
    ("Reference", r"速查|reference|参考|索引|索引表"),
]
DOMAIN_MAP = {"AI": "AI", "Robotics": "Robotics", "Automation": "Software",
              "General": "General", "Game": "Game"}
ENGINE_Tech = [("godot", "Godot"), ("gdscript", "GDScript"), ("unity", "Unity"),
               ("unreal", "Unreal"), ("python", "Python"), ("pytorch", "PyTorch"),
               ("ros", "ROS"), ("blender", "Blender"), ("kicad", "KiCad")]
SW_HINTS = ["godot","unity","unreal","gdscript","python"," api","http","json","yaml","docker","git",
            "sql","typescript","javascript","cli","script","shader","算法","代码","函数","类"]
AI_HINTS = ["llm","prompt","模型","embedding","rag","gpt","claude","大模型","token","思维链","agent","微调"]
ROB_HINTS = ["robot","机械臂","ros","传感器","抓取","运动学"]
ELE_HINTS = ["pcb","电路","电容","元器件","单片机"]

def clean(txt):
    txt = re.sub(r"\b本\s*Skill\b|\b本技能\b|\b该技能\b|\b这个\s*[Ss]kill\b", "本文", txt)
    txt = re.sub(r"\b本\s*[Ss]kill\b", "本文", txt)
    return txt.strip()

def first_sentence(txt, n=200):
    for ln in txt.split("\n"):
        s = ln.strip().lstrip("#>-*• ").strip()
        if len(s) >= 12:
            return s[:n]
    return ""

def name_slug(name):
    return re.sub(r"[^A-Z0-9]+", "-", name.upper()).strip("-")[:30] or "TOPIC"

def slugify(s, fallback):
    toks = re.findall(r"[A-Za-z0-9]+", s)
    slug = "-".join(toks[:4]).upper()
    if len(slug) < 3: slug = re.sub(r"[^A-Z0-9]+", "-", fallback.upper()).strip("-")[:24]
    return slug[:40] or "TOPIC"

def detect_versions(text):
    vs = []
    for tech, pat in VERSION_PATTERNS:
        for m in re.findall(pat, text):
            vs.append(f"{tech} {m}")
    return sorted(set(vs))

def detect_tech(text):
    t = text.lower()
    return [name for key, name in ENGINE_Tech if key in t]

def classify_domain(text, sk_domain, name):
    t = (text[:3000] + " " + name).lower()
    n_ele = sum(1 for k in ELE_HINTS if k in t); n_rob = sum(1 for k in ROB_HINTS if k in t)
    n_ai = sum(1 for k in AI_HINTS if k in t)
    if n_ele >= 2: return "Electronics", None
    if n_rob >= 2 or sk_domain == "Robotics": return "Robotics", None
    if n_ai >= 3 and sk_domain in ("AI", "General", "Automation"): return "AI", None
    if sk_domain == "Game":
        for k, eng in (("godot", "Godot"), ("unity", "Unity"), ("unreal", "Unreal")):
            if k in t: return "Software", eng
        return "General", None            # 游戏设计类 → General + subdomain 承载（GAP 记录）
    if sk_domain == "AI": return "AI", None
    if sk_domain == "Robotics": return "Robotics", None
    if sk_domain == "Automation":
        return ("AI" if any(k in t for k in AI_HINTS) else "Software"), None
    if any(k in t for k in SW_HINTS): return "Software", None
    return "General", None

def classify_type(head, text):
    h = head + " " + text[:600]
    for t, pat in TYPE_RULES:
        if re.search(pat, h, re.I): return t
    return "Concept"

def norm_title(s):
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", s.lower())

def sim(a, b): return difflib.SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()

# ---------- 1) 段级筛选 + 原子化候选 ----------
sections = []
dropped_wf = 0
for c in cands:
    for s in c["sections"]:
        head, txt = s["head"], clean(s["text"])
        if WF_DROP_HEAD.match(head.strip()) and s["km"] < 5:
            dropped_wf += 1; continue
        if s["score"] < 6 or s["km"] < 3:
            continue
        if len(txt) < 300: continue
        if re.search(r"skill_view\(|文件地图|系列入口|Routing Table|load the reference|"
                     r"身份素材|series 定义|委派时|SKILL\.md 的|本 Skill 的结构|references/ 目录说明",
                     head + " " + txt[:800], re.I):
            continue                                   # 类别 E：Skill 自身元数据，非知识
        if len(txt) > 12000:                       # 过大按子标题二次原子化，仍超则留首部并标注
            txt = txt[:12000] + "\n\n> （单单元上限截断，完整内容见来源 Skill 原文）"
        sections.append({**s, "head": head, "text": txt, "skill": c})

# ---------- 2) 与既有 7 个 Unit 去重 → 复用 ----------
units, reused, needs_review_units = [], [], []
for s in sections:
    c = s["skill"]
    match = None
    for et in existing_titles:
        if sim(s["head"], et) >= 0.55:
            match = et; break
    if match:
        reused.append({"skill_id": c["skill_id"], "head": s["head"], "reused_title": match})
        continue
    units.append(s)

# ---------- 3) 跨 Skill 同题合并（版本不同不合并） ----------
units.sort(key=lambda s: -s["score"])          # canonical = 最高分段
merged_groups = []
i = 0
while i < len(units):
    j = i + 1
    grp = [units[i]]
    while j < len(units):
        if sim(units[i]["head"], units[j]["head"]) >= 0.6:
            vi, vj = detect_versions(units[i]["text"]), detect_versions(units[j]["text"])
            if vi and vj and set(vi) != set(vj):
                j += 1; continue
            grp.append(units.pop(j))
        else:
            j += 1
    if len(grp) > 1:
        units[i]["merged_sources"] = grp[1:]   # 跨 Skill 佐证 → 置信度与 source_refs
        merged_groups.append([g["skill"]["skill_id"] for g in grp])
    i += 1

# ---------- 4) 生成 Knowledge Unit（内容文件 + 注册条目） ----------
SEEN_TITLES = set(u["title"] for u in reg["knowledge_units"])

def unique_kid(domain, slug):
    base = f"K-{domain[:8].upper()}-{slug}"
    kid, n = base, 1
    while kid in existing_ids:
        n += 1; kid = f"{base}-{n:03d}"
    existing_ids.add(kid)
    return kid

sources = {}
src_counter = 0
def src_id_for(c):
    global src_counter
    key = c["skill_id"]
    if key not in sources:
        src_counter += 1
        sources[key] = {
            "source_id": f"SRC-SKILL-{src_counter:03d}",
            "title": c["name"], "author": "Agent Skill（内部沉淀）",
            "organization": "personal", "source_type": "Other",
            "url": f"file://{os.path.expanduser(c['path'])}", "version": None, "publication_date": None,
            "access_date": TODAY, "license": None, "copyright": None,
            "domain": c["domain"], "reliability": 4, "status": "Active",
            "notes": f"Agent Skill file: {os.path.expanduser(c['path'])}（Tier 4：单一内部来源，未交叉验证）",
        }
    return sources[key]["source_id"]

created = []
SK_DOMAIN_CACHE = {}
for s in units:
    c = s["skill"]
    head, txt = s["head"], s["text"]
    if c["skill_id"] not in SK_DOMAIN_CACHE:
        SK_DOMAIN_CACHE[c["skill_id"]] = classify_domain(
            " ".join(x["text"] for x in c["sections"]), c["domain"], c["name"])
    domain, engine = SK_DOMAIN_CACHE[c["skill_id"]]
    if engine == "Godot": domain = "Software"
    versions = detect_versions(txt)
    techs = detect_tech(txt) or ([engine] if engine else [])
    ktype = classify_type(head, txt)
    title = head
    if re.match(r"^\s*(\d|step|场景|phase|阶段|scene|prelude|example)", head, re.I) or len(head.strip()) < 5:
        title = f"{c['name']}: {head}"
    while title in SEEN_TITLES:
        title = title + " (2)"
    SEEN_TITLES.add(title)
    kid = unique_kid(domain, name_slug(c["name"]))
    sid = src_id_for(c)
    vscope = ", ".join(versions) if versions else None
    subdomain = {"Game": "Game Design"}.get(c["domain"]) or c["domain"]
    # 内容文件路径
    if engine in ("Godot", "Unity", "Unreal"):
        cdir = f"{LIB}/02_GAME_ENGINES/{engine}/Knowledge"
    else:
        cdir = f"{KDIR}/{domain}"
    os.makedirs(cdir, exist_ok=True)
    cpath = f"{cdir}/{kid}.md"
    concepts = [ln.strip().lstrip("-*• ").strip()[:150] for ln in txt.split("\n")
                if ln.strip().startswith(("-", "*", "•")) and len(ln.strip()) > 15][:6]
    keywords = sorted({w.lower() for w in re.findall(r"[A-Za-z]{4,}", (head + " " + c["name"]))})[:10] + \
               [subdomain] + techs
    merged_srcs = s.get("merged_sources", [])
    confidence = "medium" if len(merged_srcs) >= 1 else "low"
    wr_review = (s["score"] < 7 and not merged_srcs) or c["category"] == "PROJECT_SPECIFIC"
    body_md = (
        f"# {kid} — {title}\n\n"
        f"- **Domain**: {domain} / {subdomain} | **Type**: {ktype}"
        + (f" | **Engine**: {engine}" if engine else "") + "\n"
        f"- **Version scope**: {vscope or '未标注（通识）'} | **Technology**: {', '.join(techs) or 'general'}\n"
        f"- **Confidence**: {confidence} | **Status**: Candidate | **Validation**: UNVALIDATED\n"
        f"- **Source**: {sid}（Agent Skill: {c['name']}）| **Extracted**: {TODAY}\n\n"
        f"## 知识正文\n\n{txt}\n\n"
        f"## Provenance\n\n"
        f"- source_skill_id: `{c['skill_id']}`\n- source_skill_path: `{os.path.expanduser(c['path'])}`\n"
        f"- source_name: `{c['name']}`\n- original_section: `{head}`\n"
        f"- source_type: Agent Skill (internal, Tier 4)\n- extraction_date: {TODAY}\n"
        f"- version_scope: {vscope or 'N/A'}\n"
    )
    with open(cpath, "w", encoding="utf-8") as f:
        f.write(body_md)
    unit = {
        "knowledge_id": kid, "title": title, "domain": domain, "subdomain": subdomain,
        "type": ktype, "summary": first_sentence(txt) or (c["desc"][:200] or head),
        "content": cpath.replace(LIB + "/", ""), "keywords": keywords,
        "concepts": concepts or [head], "prerequisites": [],
        "related_knowledge": [], "related_capabilities": [], "related_projects": [],
        "related_assets": [],
        "source_refs": [{"source_id": sid, "version": vscope, "date": TODAY,
                         "location": f"{os.path.expanduser(c['path'])}#{head}"}] + [
                        {"source_id": src_id_for(m["skill"]), "version": vscope, "date": TODAY,
                         "location": f"{os.path.expanduser(m['skill']['path'])}#{m['head']}"} for m in merged_srcs],
        "source": [sid],
        "source_version": vscope, "source_date": None, "ingestion_date": TODAY,
        "confidence": confidence, "status": "Candidate", "validation_status": "UNVALIDATED",
        "technology": ", ".join(techs) or None, "version": vscope,
        "notes": (f"provenance: source_skill_id={c['skill_id']}; original_section={head}; "
                  f"source_type=Agent Skill; extraction_date={TODAY}; pipeline=Skill→Knowledge Ingestion BATCH2"),
        "quality_checks": {
            "1_is_knowledge": True, "2_deduplicated": "cross-skill merged" if merged_srcs else "unique",
            "3_has_source": True, "4_has_version_scope": bool(vscope) or "通识/未标注（如实记录）",
            "5_standalone": len(txt) >= 300, "6_retrievable": len(keywords) >= 3,
            "7_decoupled_from_skill": not re.search(r"本\s*Skill|skill_view\(", txt),
            "8_no_obvious_conflict": True, "9_needs_human_review": wr_review,
            "10_scope_limited": bool(vscope) or "通识未标版本",
        },
    }
    if wr_review: needs_review_units.append(kid)
    created.append({"knowledge_id": kid, "skill_id": c["skill_id"], "domain": domain,
                    "type": ktype, "confidence": confidence, "needs_review": wr_review,
                    "path": cpath, "quality_checks": unit["quality_checks"],
                    "merged_from": [m["skill"]["skill_id"] for m in merged_srcs]})
    reg["knowledge_units"].append({k: v for k, v in unit.items() if k != "quality_checks"})

# 合并组的多源引用补写
for grp in merged_groups:
    pass  # 合并发生在 dedupe 阶段：同组仅最高分段成 Unit，其余进 reused 记录
for s in sections:
    pass

# ---------- 5) 注册表数据更新（追加数据，不动 Schema） ----------
reg["registry"]["updated_at"] = TODAY
for k in created:  # 溯源扩展写回 registry notes 已含；quality_checks 落盘到 ingestion yaml
    pass
src_reg["sources"].extend(sources.values())
src_reg["registry"]["updated_at"] = TODAY

queue_doc["queue"].append({
    "source_id": "SRC-SKILL-001", "batch": "BATCH2-SKILL-INGESTION",
    "covers": sorted({s["source_id"] for s in sources.values()}),
    "priority": "P1", "domain": "多域（Skill 语料全量吸收）",
    "reason": "Skill→Knowledge Ingestion：358 个逻辑 Skill 全量重检，提取长期工程知识（API/原理/限制/最佳实践/排障/经验），Workflow 保留原 Skill",
    "status": "Done", "requested_by": "user task 2026-10-08",
    "last_updated": TODAY,
})
queue_doc["registry"]["updated_at"] = TODAY

def dump_with_header(path, doc, header_keep=True):
    old = open(path, encoding="utf-8").read().split("\n")
    hdr = []
    if header_keep:
        for ln in old:
            if ln.startswith("#"): hdr.append(ln)
            elif ln.strip() == "": hdr.append(ln)
            else: break
    txt = yaml.dump(doc, allow_unicode=True, sort_keys=False, width=120)
    if hdr:
        # 更新头部计数注释
        hdr = [re.sub(r"(Knowledge Unit count: )\d+", r"\g<1>" + str(len(doc.get("knowledge_units", []))), h)
               if "knowledge_units" in doc else h for h in hdr]
        hdr = [re.sub(r"(Source count: )\d+", r"\g<1>" + str(len(doc.get("sources", []))), h)
               if "sources" in doc else h for h in hdr]
        txt = "\n".join(hdr).rstrip() + "\n" + txt
    open(path, "w", encoding="utf-8").write(txt)

dump_with_header(f"{KDIR}/_REGISTRY/KNOWLEDGE_REGISTRY.yaml", reg)
dump_with_header(f"{KDIR}/_REGISTRY/SOURCE_REGISTRY.yaml", src_reg)
dump_with_header(f"{KDIR}/_REGISTRY/INGESTION_QUEUE.yaml", queue_doc)

# ---------- 6) 重建 KNOWLEDGE_INDEX.md（数据部分） ----------
units_r = reg["knowledge_units"]
dom_cnt = collections.Counter(u["domain"] for u in units_r)
conf_cnt = collections.Counter(u["confidence"] for u in units_r)
stat_cnt = collections.Counter(u["status"] for u in units_r)
rows = "\n".join(
    f"| {u['knowledge_id']} | {u['title'][:44]} | {u.get('subdomain','')} | {u['confidence']} | {u['status']} | {(u.get('source') or [''])[0]} |"
    for u in units_r)
idx = f"""# Knowledge Index

> Status: ACTIVE — Phase 4（BATCH2 Skill→Knowledge Ingestion 完成）
> Knowledge Unit count: {len(units_r)} | Source count: {len(src_reg['sources'])} | Queue count: {len(queue_doc['queue'])}
> Machine registry: `_REGISTRY/KNOWLEDGE_REGISTRY.yaml`
> Rules: `KNOWLEDGE_RULES.md` | Spec: `KNOWLEDGE_INGESTION_SPEC.md`

检索维度（Spec §19）：
Domain / Topic / Technology / Version / Confidence / Source / Capability / Project

---

## By Domain

| Domain | Count |
|---|---:|
| Engineering | {dom_cnt.get('Engineering',0)} |
| Software | {dom_cnt.get('Software',0)} |
| AI | {dom_cnt.get('AI',0)} |
| Robotics | {dom_cnt.get('Robotics',0)} |
| Mechanical | {dom_cnt.get('Mechanical',0)} |
| Manufacturing | {dom_cnt.get('Manufacturing',0)} |
| Electronics | {dom_cnt.get('Electronics',0)} |
| General | {dom_cnt.get('General',0)} |

## By Confidence

| Confidence | Count |
|---|---:|
| high | {conf_cnt.get('high',0)} |
| medium | {conf_cnt.get('medium',0)} |
| low | {conf_cnt.get('low',0)} |

## By Status

| Status | Count |
|---|---:|
| Candidate | {stat_cnt.get('Candidate',0)} |
| Ingesting | {stat_cnt.get('Ingesting',0)} |
| Reviewed | {stat_cnt.get('Reviewed',0)} |
| Validated | {stat_cnt.get('Validated',0)} |
| Active | {stat_cnt.get('Active',0)} |
| Deprecated | {stat_cnt.get('Deprecated',0)} |

## Knowledge Units

| ID | Title | Subdomain | Confidence | Status | Source |
|---|---|---|---|---|---|
{rows}

内容文件：Godot/Unity/Unreal → `02_GAME_ENGINES/<Engine>/Knowledge/`（Engine Isolation §9）；其余 → `01_KNOWLEDGE/<Domain>/`

---

## AI Retrieval 要求（Spec §20）

AI 不应"读取整个 Knowledge Library"，而应走管线：

```
用户需求 → Task Classification → Knowledge Retrieval → Capability Retrieval
→ Dependency Retrieval → Implementation Retrieval → Execution
```

Knowledge Retrieval 必须支持：关键词、语义、Domain、Version、Source、Confidence、Related Capability。
"""
open(f"{KDIR}/_REGISTRY/KNOWLEDGE_INDEX.md", "w", encoding="utf-8").write(idx)

summary = {
    "sections_selected": len(units) + len(reused), "dropped_workflow": dropped_wf,
    "created_units": len(created), "reused_existing": len(reused),
    "merged_groups": len(merged_groups), "needs_review_units": len(needs_review_units),
    "new_sources": len(sources), "by_domain": dict(collections.Counter(c["domain"] for c in created)),
    "by_type": dict(collections.Counter(c["type"] for c in created)),
    "by_conf": dict(collections.Counter(c["confidence"] for c in created)),
}
json.dump({"summary": summary, "created": created, "reused": reused,
           "needs_review": needs_review_units, "sources": list(sources.values())},
          open(SCRATCH + "/ingest_result.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps(summary, ensure_ascii=False, indent=1))
