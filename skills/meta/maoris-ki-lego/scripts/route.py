#!/usr/bin/env python3
"""Local metadata retrieval and private experience logging. No network or model calls."""
import argparse
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import time

GROUPS = [
 ("excel", "xlsx", "csv", "spreadsheet", "spreadsheets", "таблица", "табель", "zeiterfassung"),
 ("pdf", "пдф"),
 ("document", "documents", "docx", "word", "документ"),
 ("presentation", "presentations", "pptx", "slides", "презентация", "слайды"),
 ("copywriting", "реклама", "рекламный", "advertising", "werbung", "маркетинг"),
 ("n8n", "workflow", "automation", "автоматизация", "автоматизировать"),
 ("invoice", "rechnung", "счет", "счёт", "xrechnung", "zugferd"),
 ("image", "imagegen", "изображение", "картинка", "иллюстрация"),
 ("seo", "сео", "поисковый"),
]
NATIVE = [
 ("Spreadsheets", "excel xlsx csv spreadsheet таблица табель zeiterfassung"),
 ("pdf", "pdf пдф печать"),
 ("documents", "document docx word документ"),
 ("Presentations", "presentation pptx slides презентация слайды"),
 ("copywriting", "copywriting реклама advertising werbung"),
 ("n8n-workflow-patterns", "n8n workflow automation автоматизация"),
 ("maoris-e-rechnung", "invoice rechnung счет счёт"),
 ("imagegen", "image imagegen изображение иллюстрация"),
 ("ns-cleaning-kalkulator", "уборка kalkulation cleaning angebot"),
]
STOP = {"для", "наш", "наши", "этот", "with", "from", "this", "the", "and"}

def tokens(value):
    parts = set(re.findall(r"[\w-]+", value.lower().replace("ё", "е")))
    return (parts | {piece for word in parts for piece in word.split("-")}) - STOP

def expanded(value):
    result = tokens(value)
    folded = value.lower().replace("ё", "е")
    stems = {"таблиц":"excel", "табел":"zeiterfassung", "презентац":"presentation", "реклам":"copywriting", "автоматизац":"automation", "изображен":"image", "иллюстрац":"image"}
    for word in tuple(result):
        for stem, target in stems.items():
            if word.startswith(stem):
                result.add(target)
    phrases = [(r"(?:учет|отработан\w*|рабоч\w*)\s+(?:рабоч\w*\s+)?(?:час\w*|времен\w*)|arbeitszeit\w*|stunden(?:zettel|nachweis|erfassung)", "zeiterfassung"), (r"(?:коммерческ\w*|рекламн\w*)\s+предложен\w*|sales copy", "copywriting")]
    if result & {"счета", "счетов", "счету", "счетом", "счете"}:
        result.add("invoice")
    for pattern, target in phrases:
        if re.search(pattern, folded):
            result.add(target)
    for group in GROUPS:
        terms = tokens(" ".join(group))
        if result & terms:
            result |= terms
    return result

def score(query, name="", description="", tags=""):
    title, desc, tag = tokens(name), tokens(description), tokens(tags)
    return 6*len(query & title) + len(query & desc) + 3*len(query & tag)

def read_events(root):
    path = root / "memory/experience.jsonl"
    records = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
                if isinstance(item, dict) and isinstance(item.get("event_id"), str):
                    records[item["event_id"]] = item
            except ValueError:
                continue
    return records

def valid_note(item):
    return (item.get("event_type", "note") == "note"
            and item.get("scope") in ("NS", "MDL", "general")
            and item.get("status") in ("candidate", "confirmed")
            and isinstance(item.get("tags"), list)
            and bool(item["tags"])
            and all(isinstance(tag, str) for tag in item["tags"])
            and all(isinstance(item.get(key), str) for key in ("observation", "recommendation")))

def load_memory(root):
    events = read_events(root)
    notes = {key:item for key,item in events.items() if valid_note(item)}
    hidden = set()
    for item in events.values():
        target = item.get("target_id") if item.get("event_type") == "retirement" and isinstance(item.get("reason"), str) else item.get("supersedes") if valid_note(item) else None
        if isinstance(target, str) and target in notes and item.get("scope") == notes[target]["scope"]:
            hidden.add(target)
    active = {}
    for key,item in notes.items():
        if key in hidden:
            continue
        expiry = item.get("expires_on")
        if expiry:
            try:
                if date.fromisoformat(expiry) < datetime.now(timezone.utc).date():
                    continue
            except (ValueError, TypeError):
                continue
        active[key] = item
    return active

def require_private(root):
    try:
        private = json.loads((root / "references/source.json").read_text()).get("private_experience") is True
    except (OSError, ValueError):
        private = False
    if not private:
        raise ValueError("private experience marker missing; refuse to log in a public source checkout")

def append_event(root, note):
    note["date"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    path = root / "memory/experience.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY|os.O_CREAT|os.O_APPEND, 0o600)
    try:
        payload = (json.dumps(note, ensure_ascii=False)+"\n").encode()
        if os.write(fd, payload) != len(payload):
            raise OSError("incomplete event write")
    finally:
        os.close(fd)
    return {"status":"recorded_locally", "event_id":note["event_id"], "durable_save_required":True}

def retire(root, event_id, reason):
    require_private(root)
    events = read_events(root)
    if event_id not in events or not valid_note(events[event_id]):
        raise ValueError("unknown lesson event_id")
    if not 1 <= len(reason) <= 400:
        raise ValueError("invalid retirement reason")
    key = "retire:"+hashlib.sha256((event_id+"\n"+reason).encode()).hexdigest()[:24]
    if key in events:
        return {"status":"already_recorded", "event_id":key, "durable_save_required":True}
    return append_event(root, {"event_id":key,"event_type":"retirement","target_id":event_id,"scope":events[event_id]["scope"],"reason":reason})

def personal_candidates(root):
    for path in sorted(root.parent.glob("skill-*/SKILL.md")):
        if path.parent == root:
            continue
        try:
            with path.open(encoding="utf-8") as stream:
                head = stream.read(8192).split("---", 2)
            if len(head) < 3:
                continue
            name = re.search(r"(?m)^name:\s*(.+)$", head[1])
            desc = re.search(r"(?ms)^description:\s*(.*?)(?=\n\S|\Z)", head[1])
            if name:
                yield {"name":name[1].strip(" \"'"), "description":re.sub(r"\s+", " ", desc[1]).strip(" \"'") if desc else "", "path":str(path), "kind":"personal_metadata"}
        except OSError:
            continue

def search(root, query, scope):
    started = time.perf_counter()
    q = expanded(query)
    index = {}
    try:
        index = json.loads((root / "references/catalog.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    candidates = []
    for name, tags in NATIVE:
        candidates.append({"name":name, "description":tags, "kind":"native_candidate"})
    candidates.extend(personal_candidates(root))
    for item in index.get("materials", []):
        if isinstance(item, dict) and item.get("name") != "maoris-ki-lego":
            candidates.append({**item, "kind":"repository_metadata"})
    ranked = {}
    for item in candidates:
        name = str(item.get("name", ""))[:100]
        if name == "maoris-ki-lego":
            continue
        if scope == "MDL" and name == "ns-cleaning-kalkulator":
            continue
        aliases = next((tags for key,tags in NATIVE if key.lower()==name.lower()), "")
        points = score(q, name, str(item.get("description", "")), aliases)
        if points <= 0:
            continue
        key = name.lower()
        priority = {"personal_metadata":3, "native_candidate":2, "repository_metadata":1}[item["kind"]]
        prev = ranked.get(key)
        if prev and (priority, points) <= (prev["_priority"], prev["_score"]):
            continue
        ranked[key] = {"name":name, "description":str(item.get("description", ""))[:140], "kind":item["kind"],
                       **{k:str(item[k])[:350] for k in ("path", "sha", "url") if item.get(k)},
                       "_score":points, "_priority":priority}
    best = max((x["_score"] for x in ranked.values()), default=0)
    selected = sorted((x for x in ranked.values() if x["_score"] >= max(2,best*0.2)), key=lambda x:(-x["_score"], -x["_priority"], x["name"]))[:3]
    for item in selected:
        item["score"] = item.pop("_score")
        item.pop("_priority")
    lessons = []
    for item in load_memory(root).values():
        if item.get("scope") not in ("general", scope) or item.get("status") not in ("candidate", "confirmed"):
            continue
        points = score(q, tags=" ".join(item.get("tags", [])))
        if points > 0:
            lessons.append((points, item))
    lessons.sort(key=lambda x:(x[0], x[1].get("status")=="confirmed", x[1].get("date", "")), reverse=True)
    return {"candidates":selected,
            "lessons":[{k:str(n.get(k, ""))[:220] for k in ("event_id","scope","observation","recommendation","status")} for _,n in lessons[:3]],
            "index_checked_on":index.get("checked_on"), "index_commit":index.get("commit"),
            "elapsed_ms":round((time.perf_counter()-started)*1000, 1),
            "notice":"Metadata and advisory lessons only; read chosen instructions and verify current access."}

def learn(root, item):
    require_private(root)
    if not isinstance(item, dict):
        raise ValueError("note must be an object")
    event_id = item.get("event_id", "")
    if not isinstance(event_id, str) or not re.fullmatch(r"[a-zA-Z0-9_.:-]{1,80}", event_id):
        raise ValueError("invalid event_id")
    if item.get("scope") not in ("NS", "MDL", "general"):
        raise ValueError("invalid scope")
    if item.get("status") not in ("candidate", "confirmed"):
        raise ValueError("invalid status")
    if item.get("evidence_kind") not in ("observation","user_instruction","tested_result"):
        raise ValueError("invalid evidence_kind")
    if item.get("status")=="confirmed" and item.get("evidence_kind")=="observation":
        raise ValueError("ordinary observation must remain candidate")
    tags = item.get("tags")
    if not isinstance(tags, list) or not 1 <= len(tags) <= 12 or any(not isinstance(t,str) or len(t)>40 for t in tags):
        raise ValueError("invalid tags")
    for key in ("observation","recommendation"):
        if not isinstance(item.get(key),str) or not 1 <= len(item[key]) <= 400:
            raise ValueError("invalid "+key)
    events = read_events(root)
    if event_id in events:
        return {"status":"already_recorded","event_id":event_id,"durable_save_required":True}
    note = {k:item[k] for k in ("event_id","scope","tags","observation","recommendation","status","evidence_kind")}
    if "supersedes" in item:
        target = item["supersedes"]
        if not isinstance(target,str) or target not in events or not valid_note(events[target]) or events[target]["scope"] != item["scope"]:
            raise ValueError("supersedes must reference an existing lesson in the same scope")
        note["supersedes"] = target
    expiry = item.get("expires_on")
    if expiry is not None:
        try:
            note["expires_on"] = date.fromisoformat(expiry).isoformat()
        except (ValueError, TypeError):
            raise ValueError("expires_on must be YYYY-MM-DD")
    elif item["status"] == "candidate":
        note["expires_on"] = (datetime.now(timezone.utc).date()+timedelta(days=30)).isoformat()
    return append_event(root, note)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root",type=Path,default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="command",required=True)
    find = sub.add_parser("search")
    find.add_argument("--query",required=True)
    find.add_argument("--scope",choices=("NS","MDL","general"),default="general")
    sub.add_parser("learn")
    remove = sub.add_parser("retire")
    remove.add_argument("--event-id", required=True)
    remove.add_argument("--reason", required=True)
    args = parser.parse_args()
    try:
        if args.command == "search":
            result = search(args.root,args.query,args.scope)
        elif args.command == "retire":
            result = retire(args.root,args.event_id,args.reason)
        else:
            result = learn(args.root,json.load(sys.stdin))
    except (OSError,ValueError,TypeError) as exc:
        print("FAIL: "+str(exc),file=sys.stderr)
        return 1
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))
    return 0

if __name__=="__main__":
    sys.exit(main())
