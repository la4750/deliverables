#!/usr/bin/env python3
# 终版：人工复核定类 + skill_id/domain + 使用数据 + 粒度 + 质量聚合 + 重叠分析
import json, re, collections, os, difflib, datetime

SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
logical = json.load(open(SCRATCH + "/skill_logical_classified.json"))
items = json.load(open(SCRATCH + "/skill_inventory_raw.json"))

# ============ 人工复核覆盖表（逐条通读 358 条后确定） ============
OVR = {
 # AGENT_WORKFLOW 修正
 "Email Management":"WORKFLOW_SKILL","accelerate":"TOOL_WRAPPER","ai-presenter-video":"WORKFLOW_SKILL",
 "antigravity-cli":"TOOL_WRAPPER","bioinformatics":"META_SKILL","delivery-workflow":"WORKFLOW_SKILL",
 "doubt-driven-development":"WORKFLOW_SKILL","dream-loop":"WORKFLOW_SKILL","grill-me":"WORKFLOW_SKILL",
 "honcho":"TOOL_WRAPPER","ip-as-logo":"WORKFLOW_SKILL","lambda-labs":"TOOL_WRAPPER","modal":"TOOL_WRAPPER",
 "novel-writing":"WORKFLOW_SKILL","oss-forensics":"WORKFLOW_SKILL","pr-lens":"WORKFLOW_SKILL",
 "pytorch-lightning":"KNOWLEDGE_WRAPPER","requesting-code-review":"WORKFLOW_SKILL",
 "rules-knowledge-base":"WORKFLOW_SKILL","spike":"WORKFLOW_SKILL","stable-diffusion":"TOOL_WRAPPER",
 "system-atlas":"WORKFLOW_SKILL","vertical-slice":"WORKFLOW_SKILL","web-pentest":"WORKFLOW_SKILL",
 # KNOWLEDGE 修正
 "ast-grep":"TOOL_WRAPPER","awesome-novel":"WORKFLOW_SKILL","baoyu-comic":"WORKFLOW_SKILL","box":"TOOL_WRAPPER",
 "bug-triage":"WORKFLOW_SKILL","code-wiki":"WORKFLOW_SKILL","decision-questionnaire":"WORKFLOW_SKILL",
 "detect-loop":"WORKFLOW_SKILL","documentation-and-adrs":"WORKFLOW_SKILL","game-studio-localize":"WORKFLOW_SKILL",
 "humanizer":"WORKFLOW_SKILL","memory-recording":"WORKFLOW_SKILL","novel-chapter":"WORKFLOW_SKILL",
 "novel-setup":"WORKFLOW_SKILL","osint-investigation":"WORKFLOW_SKILL","pokemon-player":"TOOL_WRAPPER",
 "prompt-audit":"WORKFLOW_SKILL","qa-plan":"WORKFLOW_SKILL","qdrant":"TOOL_WRAPPER","roleplay-sandbox":"WORKFLOW_SKILL",
 "setup-engine":"WORKFLOW_SKILL","short-analyze":"WORKFLOW_SKILL","short-plan":"WORKFLOW_SKILL",
 "short-polish":"WORKFLOW_SKILL","short-write":"WORKFLOW_SKILL","soak-test":"WORKFLOW_SKILL",
 "style-distill":"WORKFLOW_SKILL","tencentcloud-lighthouse-skill":"TOOL_WRAPPER","updater-archive":"WORKFLOW_SKILL",
 "volume-writing":"WORKFLOW_SKILL",
 # META 修正
 "agent-browser":"TOOL_WRAPPER","dcf-model":"WORKFLOW_SKILL","game-studio-create-architecture":"WORKFLOW_SKILL",
 "game-studio-review-all-gdds":"WORKFLOW_SKILL","pptx-author":"WORKFLOW_SKILL","sdlc-review":"WORKFLOW_SKILL",
 # OBSOLETE/PROJECT 修正
 "novel-archive":"WORKFLOW_SKILL","game-dev-lessons":"KNOWLEDGE_WRAPPER","godot-kb":"KNOWLEDGE_WRAPPER",
 "ai-engineering-library":"PROJECT_SPECIFIC",
 # TOOL 修正
 "auteur":"WORKFLOW_SKILL","baoyu-article-illustrator":"WORKFLOW_SKILL","cn-market-data-failover":"WORKFLOW_SKILL",
 "context-engineering":"WORKFLOW_SKILL","creative-ideation":"WORKFLOW_SKILL","domain-intel":"WORKFLOW_SKILL",
 "excel-author":"WORKFLOW_SKILL","fitness-nutrition":"WORKFLOW_SKILL","comps-analysis":"WORKFLOW_SKILL",
 "grounded-citations":"WORKFLOW_SKILL","merger-model":"WORKFLOW_SKILL","weekly-review-planning":"WORKFLOW_SKILL",
 "systematic-debugging":"WORKFLOW_SKILL","blocked-page-recovery":"WORKFLOW_SKILL",
 # UNKNOWN 定类
 "adversarial-ux-test":"WORKFLOW_SKILL","archify":"TOOL_WRAPPER","architecture-review":"WORKFLOW_SKILL",
 "balance-check":"WORKFLOW_SKILL","changelog":"WORKFLOW_SKILL","consistency-check":"WORKFLOW_SKILL",
 "day-one-patch":"WORKFLOW_SKILL","design-review":"WORKFLOW_SKILL","dev-story":"WORKFLOW_SKILL",
 "draw-your-font":"TOOL_WRAPPER","game-studio-architecture-review":"WORKFLOW_SKILL",
 "game-studio-bug-report":"WORKFLOW_SKILL","game-studio-map-systems":"WORKFLOW_SKILL",
 "game-studio-quick-design":"WORKFLOW_SKILL","game-studio-start":"WORKFLOW_SKILL","git-helper":"TOOL_WRAPPER",
 "github":"TOOL_WRAPPER","godot-class-name-checker":"TOOL_WRAPPER","impeccable":"KNOWLEDGE_WRAPPER",
 "lbo-model":"WORKFLOW_SKILL","neuroskill-bci":"TOOL_WRAPPER","novel-migrate":"WORKFLOW_SKILL",
 "openclaw-migration":"META_SKILL","popular-web-designs":"KNOWLEDGE_WRAPPER","python-web-scraper":"TOOL_WRAPPER",
 "regression-suite":"WORKFLOW_SKILL","scrollcraft":"WORKFLOW_SKILL","security-audit":"WORKFLOW_SKILL",
 "short-scan":"TOOL_WRAPPER","simple-english":"WORKFLOW_SKILL","sketch":"WORKFLOW_SKILL",
 "smoke-check":"WORKFLOW_SKILL","songsee":"TOOL_WRAPPER","songwriting-and-ai-music":"KNOWLEDGE_WRAPPER",
 "sprint-status":"WORKFLOW_SKILL","story-done":"WORKFLOW_SKILL","tech-debt":"WORKFLOW_SKILL",
 "telephony":"TOOL_WRAPPER","test-flakiness":"WORKFLOW_SKILL","test-helpers":"WORKFLOW_SKILL",
 "typer":"KNOWLEDGE_WRAPPER","updater-rollback":"WORKFLOW_SKILL","ux-review":"WORKFLOW_SKILL",
 "web-tools-guide":"KNOWLEDGE_WRAPPER","yuanbao":"TOOL_WRAPPER",
 # WORKFLOW 修正（工具/知识误判）
 "apple-reminders":"TOOL_WRAPPER","audiocraft-audio-generation":"TOOL_WRAPPER","axolotl":"TOOL_WRAPPER",
 "chroma":"TOOL_WRAPPER","clip":"TOOL_WRAPPER","codebase-inspection":"TOOL_WRAPPER","codex":"AGENT_WORKFLOW",
 "docker-management":"TOOL_WRAPPER","dspy":"KNOWLEDGE_WRAPPER","evaluating-llms-harness":"TOOL_WRAPPER",
 "evm":"TOOL_WRAPPER","excalidraw":"TOOL_WRAPPER","faiss":"TOOL_WRAPPER","fastapi":"KNOWLEDGE_WRAPPER",
 "findmy":"TOOL_WRAPPER","flash-attention":"KNOWLEDGE_WRAPPER","git-essentials":"KNOWLEDGE_WRAPPER",
 "google-workspace":"TOOL_WRAPPER","guidance":"TOOL_WRAPPER","harness-anything-mac":"TOOL_WRAPPER",
 "heartmula":"TOOL_WRAPPER","huggingface-tokenizers":"TOOL_WRAPPER","hyperframes":"TOOL_WRAPPER",
 "hyperliquid":"TOOL_WRAPPER","imessage":"TOOL_WRAPPER","instructor":"KNOWLEDGE_WRAPPER",
 "llava":"TOOL_WRAPPER","meme-generation":"TOOL_WRAPPER","obliteratus":"TOOL_WRAPPER","outlines":"TOOL_WRAPPER",
 "pdf":"CAPABILITY_WRAPPER","peft":"TOOL_WRAPPER","pinecone":"TOOL_WRAPPER","pinecone-research":"KNOWLEDGE_WRAPPER",
 "pretext":"TOOL_WRAPPER","pytorch-fsdp":"KNOWLEDGE_WRAPPER","reddit-reading":"TOOL_WRAPPER",
 "saelens":"TOOL_WRAPPER","segment-anything-model":"TOOL_WRAPPER","sherlock":"TOOL_WRAPPER","slime":"TOOL_WRAPPER",
 "solana":"TOOL_WRAPPER","stocks":"TOOL_WRAPPER","stripe-projects":"TOOL_WRAPPER","torchtitan":"TOOL_WRAPPER",
 "trl-fine-tuning":"TOOL_WRAPPER","unbroker":"WORKFLOW_SKILL","unsloth":"TOOL_WRAPPER","watchers":"TOOL_WRAPPER",
 "weights-and-biases":"TOOL_WRAPPER","whisper":"TOOL_WRAPPER","godmode":"WORKFLOW_SKILL",
}
# 知识型 Godot 遗产技能 → KNOWLEDGE_WRAPPER（逐个）
for g in ["godot-clear-children","godot-gdscript-grammar","godot-global-variables","godot-packedscene",
          "godot-scene-skill","godot-serialization-pattern","godot-singleton-pattern","godot-tscn-format",
          "godot-unix-timestamp-fix","godot-knowledge","godot-coding-patterns"]:
    OVR[g] = "KNOWLEDGE_WRAPPER"

for r in logical:
    if r["name"] in OVR:
        r["category"] = OVR[r["name"]]

# ============ 真实使用数据（Hermes usage.json） ============
usage = json.load(open(os.path.expanduser("~/.hermes/skills/.usage.json")))
for r in logical:
    u = usage.get(r["name"])
    if u and r["tier"] in ("A_user_hermes","C_plugin"):
        r["usage"] = {"use_count": u.get("use_count",0), "last_used_at": u.get("last_used_at"),
                      "patch_count": u.get("patch_count",0), "state": u.get("state")}
    else:
        r["usage"] = None

# ============ 嵌套检测（最近祖先 SKILL.md） ============
for r in logical:
    p = os.path.expanduser(r["path"])
    d = os.path.dirname(p)
    r.pop("nested_in", None)
    while True:
        d = os.path.dirname(d)
        if os.path.exists(os.path.join(d, "SKILL.md")):
            r["nested_in"] = os.path.basename(d); break
        if d.count("/") <= 2: break

# ============ skill_id 与 domain ============
def dom_of(r):
    t = (r["name"] + " " + r["path"] + " " + r["description"]).lower()
    if re.search(r"godot|game-|gdd|sprint|epic\b|playtest|gameplay|游戏|关卡|level-design|平衡|balance-check|day-one|launch-check|ux-design|art-bible|asset-(audit|spec)|qa-plan|story|sprint|hotfix|vertical-slice|regression-suite|smoke-check|tech-debt|test-flakiness|dev-story|changelog|bug-triage|bug-report", t):
        return "Game"
    if re.search(r"agent|llm|subagent|prompt|fine-?tun|torch|pytorch|mcp|hermes|openclaw|model|training|inference|tokeniz|embedding|rag\b|dspy|axolotl|peft|trl\b|vllm|tensorrt|flash-attention|faiss|chroma|qdrant|pinecone|stable-diffusion|whisper|llava|clip\b|saelens|slime|unsloth|guidance|outlines|instructor|simpo|accelerate|nemo-curator|darwinian|evaluating-llms", t):
        return "AI"
    if re.search(r"monitor|watch|deploy|docker|tunnel|scrap|crawl|rss|triage|inbox|email|calendar|reminder|meeting|automation|polling|watchers|blogwatcher|price-monitor|news-monitor|cloudflare|pinggy|publish-site", t):
        return "Automation"
    return "General"

def norm_name(n):
    n = n.lower().strip()
    n = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", n).strip("-")
    return n[:60] or "unnamed"

used_ids = collections.Counter()
for r in logical:
    r["domain"] = dom_of(r)
    base = "SKILL-" + {"Game":"GAME","AI":"AI","Automation":"AUTO","General":"GEN"}[r["domain"]] + "-" + norm_name(r["name"]).upper().replace("-", "-")
    used_ids[base] += 1
    r["skill_id"] = base if used_ids[base] == 1 else f"{base}-{used_ids[base]}"

# ============ 粒度 ============
children = collections.Counter(r.get("nested_in") for r in logical if r.get("nested_in"))
for r in logical:
    steps = len(re.findall(r"^\s*(\d+\.|- \[ \]|###? Step|阶段\s*\d)", r.get("body_preview","") or "", re.M)) if r.get("body_preview") else 0
    n_child = children.get(r["name"], 0)
    flags = []
    if n_child >= 5: flags.append("PARENT_PACK")          # 过粗候选（含大量嵌套子技能）
    if r["body_bytes"] < 1800 and n_child == 0: flags.append("TOO_FINE_CANDIDATE")
    if r["body_bytes"] > 40000: flags.append("OVERSIZED")
    r["granularity"] = flags

# ============ 质量聚合 ============
qstat = collections.Counter()
for r in logical:
    q = r["quality"]
    if not q["has_description"]: qstat["missing_description"] += 1
    if not q["description_triggers"]: qstat["weak_trigger"] += 1
    if q["oversized"]: qstat["oversized"] += 1
    if q["knowledge_heavy"]: qstat["knowledge_heavy"] += 1
    if q["broken_refs"]: qstat["broken_refs"] += 1
    if not q["has_inputs"]: qstat["no_inputs"] += 1
    if not q["has_outputs"]: qstat["no_outputs"] += 1
    if not q["has_completion"]: qstat["no_completion"] += 1
    if not q["has_validation"]: qstat["no_validation"] += 1
    if q["runtime_binding"]: qstat["runtime_bound"] += 1
    if q["llm_binding"]: qstat["llm_bound"] += 1
    if q["deprecated_tool"]: qstat["deprecated_tool"] += 1
    if not q["references_present"]: qstat["no_refs"] += 1
print("== 质量问题计数(逻辑技能358基数) ==")
for k, v in qstat.most_common(): print(f"  {k}: {v}")

# ============ 重叠分析 ============
overlaps = []
# 1) exact copies already in copy_paths
exact_clusters = [r for r in logical if r["copy_paths"]]
# 2) same name, different content
by_name = collections.defaultdict(list)
for r in logical: by_name[r["name"].lower()].append(r)
same_name = {k: v for k, v in by_name.items() if len(v) > 1}
# 3) near-dup names
names = [r["name"] for r in logical]
near = []
for i in range(len(names)):
    for j in range(i+1, len(names)):
        ratio = difflib.SequenceMatcher(None, names[i].lower(), names[j].lower()).ratio()
        if ratio >= 0.82 and names[i].lower() != names[j].lower():
            near.append((names[i], names[j], round(ratio,2)))
# 4) same description hash
by_desc = collections.defaultdict(list)
for r in logical:
    if r["description"]: by_desc[r["description"][:80]].append(r["name"])
same_desc = {k[:40]: v for k, v in by_desc.items() if len(v) > 1}

print("\n== 重叠统计 ==")
print("exact-copy 簇(含副本):", len(exact_clusters), "涉及文件:", sum(r["copy_count"] for r in exact_clusters))
print("同名不同内容簇:", len(same_name), {k: len(v) for k, v in same_name.items()})
print("近似名对:", len(near)); [print("   ", a, "~", b, s) for a, b, s in near[:25]]
print("同描述簇:", len(same_desc))
print("\n分类分布:", dict(collections.Counter(r["category"] for r in logical)))
print("domain 分布:", dict(collections.Counter(r["domain"] for r in logical)))
print("粒度:", dict(collections.Counter(f for r in logical for f in r["granularity"])))

json.dump(logical, open(SCRATCH + "/skill_final.json", "w"), ensure_ascii=False, indent=1)
json.dump({"exact":[{"name":r["name"],"copies":r["copy_paths"]} for r in exact_clusters],
           "same_name":{k:[x["path"] for x in v] for k,v in same_name.items()},
           "near":near, "same_desc":same_desc},
          open(SCRATCH + "/overlap_raw.json", "w"), ensure_ascii=False, indent=1)
print("\nsaved skill_final.json + overlap_raw.json")
