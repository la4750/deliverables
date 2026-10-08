#!/usr/bin/env python3
# 阶段1：全量 358 Skill 正文分段 + 知识候选打分（READ，产出 candidates.json 供审阅后入库）
import json, re, os, collections
SCRATCH = "/home/ubuntu/.hermes/cache/scratch"
logical = json.load(open(SCRATCH + "/skill_final.json"))

KNOW_MARKERS = [
    "API", "参数", "属性", "方法", "限制", "注意", "常见错误", "报错", "错误码", "异常", "最佳实践",
    "原理", "机制", "版本", "区别", "差异", "陷阱", "坑", "已知问题", "troubleshooting", "排障",
    "概念", "设计模式", "模式", "规范", "约束", "性能", "内存", "线程", "缓存", "序列化", "生命周期",
    "返回值", "类型", "回调", "事件", "信号", "状态机", "算法", "公式", "权衡", "兼容", "废弃",
    "deprecated", "behavior", "配置项", "选项", "flag", "端点", "endpoint", "header", "限流",
    "rate limit", "错误处理", "重试", "幂等", "编码", "格式", "规则", "原则", "checklist", "速查",
]
WF_MARKERS = ["需求分析", "步骤", "Step ", "workflow", "流程", "阶段", "先", "然后", "接着", "执行以下",
              "按顺序", "pipeline", "运行命令", "install", "安装", "setup", "配置步骤", "操作步骤"]
WF_HEAD = ["安装", "快速开始", "使用", "usage", "how to", "getting started", "install", "quick start",
           "配置流程", "操作", "workflow", "步骤"]
KNOW_HEAD = ["api", "参考", "reference", "参数", "限制", "注意", "错误", "故障", "排障", "troubleshoot",
             "原理", "概念", "最佳实践", "陷阱", "坑", "版本", "差异", "性能", "模式", "规则", "检查清单",
             "checklist", "设计", "faq", "常见问题"]

def sections(text):
    # 按 ##/### 切分
    lines = text.split("\n")
    out, cur, buf = [], ("(prelude)", []), []
    for ln in lines:
        m = re.match(r"^(#{2,4})\s+(.*)", ln)
        if m:
            if buf: out.append((cur[0], "\n".join(buf).strip()))
            cur, buf = (m.group(2).strip(), []), []
        else:
            buf.append(ln)
    if buf: out.append((cur[0], "\n".join(buf).strip()))
    return out

def score(head, body):
    h = head.lower(); b = body
    s = 0
    km = sum(1 for k in KNOW_MARKERS if k.lower() in b)
    wm = sum(1 for k in WF_MARKERS if k.lower() in b)
    s += min(km, 8)
    if any(k in h for k in KNOW_HEAD): s += 3
    if any(k in h for k in WF_HEAD): s -= 3
    n = len(body)
    if 300 <= n <= 8000: s += 2
    elif n < 200: s -= 3
    elif n > 12000: s -= 2
    if re.search(r"^\s*[|\-].*[|]", b, re.M): s += 1      # 表格/参数表
    if re.search(r"`\w+`|\w+\(.*\)", b): s += 1           # 代码/API 引用
    if wm >= 3 and km < 3: s -= 3
    if n > 150 and km == 0: s -= 4
    return s, km, wm

cands = []
stats = collections.Counter()
for r in logical:
    stats["total"] += 1
    if r["tier"] == "B3_":
        stats["skip_b3"] += 1; continue
    try:
        raw = open(os.path.expanduser(r["path"]), encoding="utf-8", errors="replace").read()
    except Exception:
        stats["skip_unreadable"] += 1; continue
    body = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.S)
    secs = sections(body)
    picked = []
    for head, txt in secs:
        if len(txt) < 300: continue
        s, km, wm = score(head, txt)
        if s >= 5:
            picked.append({"head": head[:90], "score": s, "km": km, "wm": wm,
                           "len": len(txt), "text": txt})
    picked.sort(key=lambda x: -x["score"])
    picked = picked[:3]                       # 每技能最多 3 段，防泛滥
    if picked:
        stats["skills_with_candidates"] += 1
        stats["sections"] += len(picked)
        cands.append({"skill_id": r["skill_id"], "name": r["name"], "category": r["category"],
                      "domain": r["domain"], "tier": r["tier"], "path": r["path"],
                      "desc": (r["description"] or "")[:200], "sections": picked})
    else:
        stats["skills_no_knowledge_section"] += 1

json.dump(cands, open(SCRATCH + "/ingest_candidates.json", "w"), ensure_ascii=False, indent=1)
print(dict(stats))
print("candidate skills by domain:", collections.Counter(c["domain"] for c in cands))
print("candidate skills by category:", collections.Counter(c["category"] for c in cands))
print("score distribution:", collections.Counter(s["score"] for c in cands for s in c["sections"]).most_common(12))
print("\n--- 抽样候选段标题（前 40，按分数）---")
flat = sorted([(s["score"], c["name"], s["head"]) for c in cands for s in c["sections"]], reverse=True)[:40]
for sc, nm, hd in flat: print(f"{sc:>3} {nm[:28]:<28} {hd}")
