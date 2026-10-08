#!/usr/bin/env python3
"""GODOT_KNOWLEDGE 结构逻辑审计（只读，不改库）。"""
import json, os, re, yaml, itertools
from collections import Counter, defaultdict

B = '/home/ubuntu/GODOT_KNOWLEDGE'
DOMAINS = ["GDSCRIPT","NODE","LIFECYCLE","SCENE","SIGNAL","RESOURCE",
           "PHYSICS","INPUT","RENDERING","ANIMATION","UI","PERFORMANCE","DEBUGGING"]
PREFIX = {"PERFORMANCE":"PERF","DEBUGGING":"DEBUG"}
LEVELS = {"MUST","SHOULD","MAY","SHOULD_NOT","MUST_NOT"}
findings = []   # (severity, msg)

def load(p):
    with open(p, encoding='utf-8') as f: return yaml.safe_load(f)

def urls(s):
    if isinstance(s, list): return [x for x in s if isinstance(x,str) and x.startswith('http')]
    return [s] if isinstance(s,str) and s.startswith('http') else []

# ---------- 1. 结构完整性 ----------
spec_dirs = ["GDSCRIPT","NODE","SCENE","SIGNAL","RESOURCE","LIFECYCLE","PHYSICS",
             "RENDERING","UI","INPUT","ANIMATION","PERFORMANCE","DEBUGGING","VERSION","CHECKPOINTS"]
for d in spec_dirs:
    if not os.path.isdir(f'{B}/{d}'): findings.append(('HIGH', f'缺少规范目录 {d}/'))
for f_ in ["README.md","GODOT_VERSION_RULES.yaml","GODOT_API_INDEX.yaml",
           "GODOT_BEST_PRACTICES.yaml","GODOT_ANTI_PATTERNS.yaml","LEARNING_REPORT.md"]:
    if not os.path.isfile(f'{B}/{f_}'): findings.append(('HIGH', f'缺少规范文件 {f_}'))
for d in DOMAINS:
    for f_ in ["RULES.yaml","API.yaml","ANTI_PATTERNS.yaml","NOTES.md"]:
        if not os.path.isfile(f'{B}/{d}/{f_}'): findings.append(('HIGH', f'{d} 缺 {f_}'))
cps = set(os.listdir(f'{B}/CHECKPOINTS'))
for d in DOMAINS + ["VERSION"]:
    if f'CHECKPOINT_{d}.md' not in cps:
        findings.append(('HIGH', f'缺 CHECKPOINT_{d}.md'))
extra = set(os.listdir(B)) - set(spec_dirs) - {
    "README.md","LEARNING_REPORT.md","GODOT_VERSION_RULES.yaml","GODOT_API_INDEX.yaml",
    "GODOT_BEST_PRACTICES.yaml","GODOT_ANTI_PATTERNS.yaml"}
if extra: findings.append(('INFO', f'规范外附加项（README 已声明用途）: {sorted(extra)}'))

# ---------- 2. 读取全部源头 ----------
rules, apis, antis, vrules = [], [], [], []
for d in DOMAINS:
    for e in (load(f'{B}/{d}/RULES.yaml') or {}).get('rules', []):
        e['_d']=d; rules.append(e)
    for e in (load(f'{B}/{d}/API.yaml') or {}).get('api', []):
        e['_d']=d; apis.append(e)
    for e in (load(f'{B}/{d}/ANTI_PATTERNS.yaml') or {}).get('anti_patterns', []):
        e['_d']=d; antis.append(e)
vrules = (load(f'{B}/VERSION/VERSION_RULES.yaml') or {}).get('version_rules', [])

# ---------- 3. ID 唯一性与序号连续性 ----------
ids = [r['id'] for r in rules]
dups = [i for i,c in Counter(ids).items() if c>1]
if dups: findings.append(('HIGH', f'规则 ID 重复: {dups}'))
by = defaultdict(list)
for r in rules:
    m = re.match(r'([A-Z]+)-(\d+)$', r['id'])
    if not m: findings.append(('HIGH', f'ID 格式非法: {r["id"]}')); continue
    by[r['_d']].append(int(m.group(2)))
for d, ns in by.items():
    ns.sort()
    if ns != list(range(1, len(ns)+1)):
        findings.append(('MED', f'{d} ID 不连续: 1..{max(ns)} 缺 {sorted(set(range(1,max(ns)+1))-set(ns))}'))
for d in DOMAINS:
    pre = PREFIX.get(d,d)
    bad = [r['id'] for r in rules if r['_d']==d and not r['id'].startswith(pre+'-')]
    if bad: findings.append(('HIGH', f'{d} ID 前缀错: {bad[:3]}'))

# ---------- 4. 置信度 vs 来源数 ----------
for r in rules:
    n = len(urls(r.get('source')))
    if r.get('confidence')=='high' and n < 2:
        findings.append(('HIGH', f'{r["id"]} 标 high 但只有 {n} 个来源'))
    if r.get('confidence')=='medium' and n >= 2:
        findings.append(('INFO', f'{r["id"]} medium 但有 {n} 个来源（偏保守，无害）'))
    if n == 0:
        findings.append(('HIGH', f'{r["id"]} 无来源 URL'))

# ---------- 5. 钉版声明 vs 来源版本 ----------
for r in rules:
    vs = str(r.get('version_scope',''))
    src = urls(r.get('source'))
    if vs in ('Godot 4.6+','Godot 4.6.2') and src and not any('/4.6' in u for u in src):
        findings.append(('MED', f'{r["id"]} 声明 {vs} 但来源无 /en/4.6/ 版本页: {src[0][:70]}'))
print('version_scope 分布:', dict(Counter(str(r.get("version_scope")) for r in rules)))

# ---------- 6. 规则重复（跨领域语义重叠）----------
def norm(t): return re.sub(r'[^a-z0-9\u4e00-\u9fff]+','', str(t).lower())
seen = defaultdict(list)
for r in rules: seen[norm(r['rule'])].append(r['id'])
for k,v in seen.items():
    if len(v)>1: findings.append(('MED', f'完全重复规则 {v}'))

def bigrams(s): return set(s[i:i+2] for i in range(len(s)-1))
near = []
norms = {r['id']: bigrams(norm(r['rule'])) for r in rules}
for a,b in itertools.combinations(norms,2):
    A,Bs = norms[a],norms[b]
    if not A or not Bs: continue
    j = len(A&Bs)/len(A|Bs)
    if j >= 0.6: near.append((a,b,round(j,2)))
if near:
    findings.append(('MED', f'近似重复规则 {len(near)} 对（语义重叠，下游可能双计）: {near[:10]}'))

# ---------- 7. 顶层库 vs 源头一致性 ----------
def L(p,k): return len(load(p)[k])
checks = [
    (f'{B}/GODOT_BEST_PRACTICES.yaml','best_practices',
     sum(1 for r in rules if r['level'] in ('MUST','SHOULD','MAY'))),
    (f'{B}/GODOT_ANTI_PATTERNS.yaml','anti_patterns',
     len(antis)+sum(1 for r in rules if r['level'] in ('MUST_NOT','SHOULD_NOT'))),
    (f'{B}/GODOT_VERSION_RULES.yaml','version_rules',
     len(vrules)+sum(1 for r in rules if r['category']=='VERSION')),
]
for p,k,exp in checks:
    got = L(p,k)
    if got != exp: findings.append(('HIGH', f'{os.path.basename(p)} 条数 {got} != 源头重算 {exp}'))
# API 去重是否丢失信息
g = defaultdict(list)
for a in apis: g[(str(a.get('class','')).lower(), str(a.get('member','')).lower())].append(a)
lost = 0
for k,v in g.items():
    if len(v)>1:
        descs = {str(x.get('description','')) for x in v}
        cms = {str(x.get('common_mistakes','')) for x in v}
        if len(descs)>1 or len(cms)>1: lost += 1
if lost: findings.append(('MED', f'API 去重丢弃了 {lost} 组跨领域不同描述（合并只保留首个领域版本）'))

# ---------- 8. 顶层库互斥性 ----------
bp = load(f'{B}/GODOT_BEST_PRACTICES.yaml')['best_practices']
ap = load(f'{B}/GODOT_ANTI_PATTERNS.yaml')['anti_patterns']
bad = [e['id'] for e in bp if e['priority'] in ('MUST_NOT','SHOULD_NOT')]
if bad: findings.append(('HIGH', f'最佳实践混入负向规则 {bad}'))
bad2 = [e['origin'] for e in ap if e.get('origin','').startswith('RULES:') and
        next((r['level'] for r in rules if 'RULES:'+r['id']==e['origin']), '') in ('MUST','SHOULD','MAY')]
if bad2: findings.append(('HIGH', f'反模式混入正向规则 {bad2}'))
miss_pref = sum(1 for e in ap if not e.get('preferred_pattern'))
if miss_pref: findings.append(('INFO', f'反模式 {miss_pref}/{len(ap)} 条无 preferred_pattern（可接受但提示下游：不是每条都有替代写法）'))

# ---------- 9. checkpoint 声明数 vs 实际 ----------
for d in DOMAINS + ['VERSION']:
    p = f'{B}/CHECKPOINTS/CHECKPOINT_{d}.md'
    txt = open(p, encoding='utf-8').read()
    m = re.search(r'rules_written:\s*(\d+)', txt)
    actual = len((load(f'{B}/{d}/RULES.yaml') or {}).get('rules', [])) if d!='VERSION' else None
    if m and actual is not None and int(m.group(1)) != actual:
        findings.append(('MED', f'{d} checkpoint 声称 {m.group(1)} 条规则，实际 {actual}'))
    if 'status: complete' not in txt: findings.append(('MED', f'{d} checkpoint 未标 complete'))

# ---------- 10. 语言混杂 ----------
cjk = sum(1 for r in rules if re.search(r'[\u4e00-\u9fff]', str(r['rule'])))
eng = len(rules)-cjk
findings.append(('INFO', f'规则语言混杂: 中文 {cjk} / 纯英文 {eng}（下游 Agent 均可读，但检索关键词需双语）'))

# ---------- 11. 工具链逻辑漏洞 ----------
src = open(f'{B}/tools/merge_kb.py', encoding='utf-8').read()
if re.search(r'DOMAINS = \[', src):
    findings.append(('MED', 'tools/merge_kb.py 的领域清单写死 13 个目录：未来新增领域（如 AUDIO/）建目录后不会被合并，也无报错'))
st = json.load(open(f'{B}/_stats.json'))
if st.get('domains') == {}: findings.append(('INFO', '_stats.json 的 domains 字段恒为空（死字段，统计实际在 by_domain）'))
# VERSION 双文件
if os.path.exists(f'{B}/VERSION/VERSION_RULES.yaml') and os.path.exists(f'{B}/GODOT_VERSION_RULES.yaml'):
    findings.append(('INFO', '版本规则存在两处: VERSION/VERSION_RULES.yaml（源头）与顶层 GODOT_VERSION_RULES.yaml（生成物+4条领域VERSION规则）；README 已声明只改源头'))

# ---------- 12. category 使用合理性 ----------
print('category x domain 交叉:')
cross = Counter((r['_d'], r['category']) for r in rules)
cat_primary = {}
for d in DOMAINS:
    top = Counter(r['category'] for r in rules if r['_d']==d).most_common(1)
    if top: cat_primary[d]=top[0][0]
odd = [(d,c,n) for (d,c),n in cross.items() if cat_primary.get(d) and c!=cat_primary[d]]
for d,c,n in sorted(odd, key=lambda x:-x[2])[:12]:
    print(f'   {d}: {c} x{n}')

print('\n===== 审计发现 =====')
order={'HIGH':0,'MED':1,'INFO':2}
for sev,msg in sorted(findings,key=lambda x:order[x[0]]):
    print(f'[{sev}] {msg}')
print(f'合计: HIGH={sum(1 for s,_ in findings if s=="HIGH")} MED={sum(1 for s,_ in findings if s=="MED")} INFO={sum(1 for s,_ in findings if s=="INFO")}')
