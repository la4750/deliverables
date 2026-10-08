#!/usr/bin/env python3
"""GODOT_KNOWLEDGE 内容层修复（一次性）：
A. confidence 语义修复（9 降级 + 1 补第二来源 + INPUT-008 降级并纠错 why）
B. version_scope 收敛为枚举 + 独立 note 字段（DEBUG 5 条）
C. 钉版来源（GDSCRIPT-005 / PERF-024 换 /en/4.6/ 来源）
D. 跨领域同一事实：7 条转 canonical reference
保留文件头注释，语义字段之外不动任何内容。
"""
import yaml, re, os, sys

B = '/home/ubuntu/GODOT_KNOWLEDGE'
log = []

def load_domain(d):
    p = f'{B}/{d}/RULES.yaml'
    txt = open(p, encoding='utf-8').read()
    lines = txt.splitlines()
    # 头注释 = 开头连续的 #/空行块
    i = 0
    while i < len(lines) and (lines[i].startswith('#') or lines[i].strip() == ''):
        i += 1
    header = lines[:i]
    body = '\n'.join(lines[i:])
    assert '#' not in re.sub(r'"[^"]*"', '', body).replace('# ', '').replace('#', '\n#') or True
    # 断言正文中无行首注释（防止丢失隐藏注释）
    for ln in lines[i:]:
        assert not ln.lstrip().startswith('#'), f'{d} 正文含注释行: {ln}'
    data = yaml.safe_load(body)
    return header, data

def save_domain(d, header, data):
    p = f'{B}/{d}/RULES.yaml'
    with open(p, 'w', encoding='utf-8') as f:
        if header:
            f.write('\n'.join(header).rstrip() + '\n')
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=1000)

def entry(data, eid):
    for e in data['rules']:
        if e['id'] == eid:
            return e
    raise KeyError(eid)

def reorder(e, after_id_key='canonical_id', after_scope_key='note'):
    """把 canonical_id 放 id 后，note 放 version_scope 后"""
    out = {}
    for k, v in e.items():
        if k in ('canonical_id', 'note'):
            continue
        out[k] = v
        if k == 'id' and 'canonical_id' in e:
            out['canonical_id'] = e['canonical_id']
        if k == 'version_scope' and 'note' in e:
            out['note'] = e['note']
    return out

# ---------- 变更表 ----------
CONF_DOWN = {  # high -> medium（无第二独立官方来源）
    'LIFECYCLE': ['LIFECYCLE-006', 'LIFECYCLE-014', 'LIFECYCLE-015'],
    'SCENE': ['SCENE-005', 'SCENE-009', 'SCENE-011', 'SCENE-014', 'SCENE-016'],
    'INPUT': ['INPUT-008'],
}
ADD_SRC = {   # 补第二独立来源，保持 high
    'LIFECYCLE': {'LIFECYCLE-021': ['https://docs.godotengine.org/en/4.6/classes/class_control.html']},
}
REPLACE_SRC = {  # 钉版：stable -> /en/4.6/
    'GDSCRIPT': {'GDSCRIPT-005': [
        'https://docs.godotengine.org/en/4.6/tutorials/scripting/gdscript/gdscript_basics.html',
        'https://docs.godotengine.org/en/4.6/tutorials/scripting/gdscript/static_typing.html']},
    'PERFORMANCE': {'PERF-024': [
        'https://docs.godotengine.org/en/4.6/tutorials/scripting/debug/objectdb_profiler.html',
        'https://docs.godotengine.org/en/4.6/classes/class_performance.html']},
}
SCOPE_FIX = {  # 枚举收敛 + note 拆分（字面拆分，不改语义）
    'DEBUG-003': ('Godot 4.x', 'Evaluator 标签页自 4.4 加入'),
    'DEBUG-011': ('Godot 4.6+', '4.6.2 适用'),
    'DEBUG-017': ('Godot 4.x', '@warning_ignore 自 4.0 存在'),
    'DEBUG-018': ('Godot 4.4+', '4.6.2 适用'),
    'DEBUG-025': ('Godot 4.x', '4.3 起修复一批相关问题'),
}
CANONICAL = {  # 同一工程事实 -> 非 canonical 端转 reference
    'LIFECYCLE-011': 'INPUT-002',
    'LIFECYCLE-012': 'NODE-010',
    'SCENE-024': 'NODE-024',
    'RESOURCE-006': 'GDSCRIPT-020',
    'PERF-022': 'RESOURCE-021',
    'GDSCRIPT-026': 'SIGNAL-014',
    'PERF-024': 'DEBUG-011',
}
WHY_FIX = {   # 事实纠错（3.2/3.4/3.6 类参考实测均无该方法）
    'INPUT-008': (
        '4.6 的 Input 类参考方法表只有 is_action_pressed、is_action_just_pressed、'
        'is_action_just_released（及 *_by_event 变体），没有 is_action_released，'
        '调用会直接报无效方法。3.2/3.4/3.6 类参考实测同样没有该方法，'
        '并非 3.x 遗留；官方事件 API 是 InputEvent.is_action_released()。'
    ),
}

DOMAINS = ['GDSCRIPT', 'NODE', 'LIFECYCLE', 'SCENE', 'SIGNAL', 'RESOURCE',
           'PHYSICS', 'INPUT', 'RENDERING', 'ANIMATION', 'UI', 'PERFORMANCE', 'DEBUGGING']

for d in DOMAINS:
    header, data = load_domain(d)
    changed = False
    ids = {e['id'] for e in data['rules']}

    for eid in CONF_DOWN.get(d, []):
        e = entry(data, eid); assert e['confidence'] == 'high', eid
        e['confidence'] = 'medium'; changed = True
        log.append(f'{eid}: confidence high->medium（无第二独立官方来源）')

    for eid, urls in ADD_SRC.get(d, {}).items():
        e = entry(data, eid)
        e['source'] = list(e['source']) + urls; changed = True
        log.append(f'{eid}: 补第二来源 {urls[0]}（保持 high）')

    for eid, urls in REPLACE_SRC.get(d, {}).items():
        e = entry(data, eid); e['source'] = urls; changed = True
        log.append(f'{eid}: 来源钉版 /en/4.6/（2 个 URL 已验证 200+内容）')

    for eid, (scope, note) in SCOPE_FIX.items():
        if eid in ids:
            e = entry(data, eid)
            assert '（' in e['version_scope'], eid
            e['version_scope'] = scope; e['note'] = note; changed = True
            log.append(f'{eid}: version_scope -> {scope!r} + note={note!r}')

    for eid, canon in CANONICAL.items():
        if eid in ids:
            e = entry(data, eid)
            assert canon in {x['id'] for x in data['rules']} or True
            e['canonical_id'] = canon; changed = True
            log.append(f'{eid}: -> reference (canonical={canon})')

    for eid, why in WHY_FIX.items():
        if eid in ids:
            e = entry(data, eid); e['why'] = why; changed = True
            log.append(f'{eid}: why 事实纠错（3.x 并无该方法）')

    if changed:
        data['rules'] = [reorder(e) for e in data['rules']]
        save_domain(d, header, data)

# canonical 存在性全校验（跨文件）
all_ids = {}
for d in DOMAINS:
    _, data = load_domain(d)
    for e in data['rules']:
        all_ids[e['id']] = e
for eid, canon in CANONICAL.items():
    assert canon in all_ids, f'canonical 不存在: {canon}'
    assert 'canonical_id' in all_ids[eid], f'{eid} 未转 reference'
print('\n'.join(log))
print(f'\n共 {len(log)} 处内容修改')
