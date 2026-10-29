"""Draw a world folder as a graph: graph.json in the platform's own shape, and graph.html.

Reads a world folder (world.json + elements/<type>/*.json, plus a legacy spatial/ folder, keyed
on the id inside each file) and writes two files into the output folder, never into the world:

    graph.json   {name, nodes:[{id,name,type,family,sup,desc}], edges:[[a,b,field]]}, the shape
                 the platform's graph page draws: a and b index into nodes, one edge per link
                 field and direction held (a link held on both ends is two edges)
    graph.html   one page, inline JS, no network: a force layout, the group colours, a search,
                 a legend that hides a type, and a panel with the clicked element's links;
                 a name is drawn only where it meets no name already placed (greedy, by degree),
                 a hidden one shows on hover and on a click, and the head counts them

Map, Pin, Marker and Zone are placement, not a graph: never a node. Room elements (the room
profile: one of its nine type-and-supertype pairs AND the mark x_room_of), proposed elements
(x_review_proposed) and hidden ones (hidden: true) are left out unless a flag asks for them.
The three reading aids (the charter profile: a Law with supertype Charter, a Construct with
supertype Guide or Domain, AND the mark x_charter_of) are left out and said once in the foot;
no flag draws them, since a world's front door is where they show, never a lore graph. Either
mark counts when its value is not null, a string only when something is left after trimming.
A link is a schema field (no x_, atlas_ or shadow_ prefix) whose value is an id, or a list of
ids, of a node; a link to a left-out element draws nothing. Every left-out count is printed.

Colours come from schema-dist's presentation.json, fetched at run time (the only network the
script uses): four colour groups named by their colours (blue, green, pink, amber), a visual
aid, not part of the standard. Offline, or on a file that does not read, four neutral greys; a
file whose colour word is not in its own order stops the script, naming the word.

Usage:
    python graph.py WORLD_FOLDER [--out DIR] [--focus NAME_OR_ID ...] [--depth N]
                    [--type TYPE ...] [--room] [--proposed] [--hidden]
                    [--offline] [--presentation PATH]

    --out DIR         where the two files go (default: draw/ beside the world folder)
    --focus X         keep X (a name or an id; repeatable) and what lies within --depth links
    --depth N         link steps from the focus (default 1; a large N gives X's whole cluster)
    --type T          keep only these types (repeatable; lowercase, as in the folder)
    --room, --proposed, --hidden   draw those elements too
    --offline         skip the fetch: neutral greys
    --presentation P  read presentation.json from a local file instead

The map and timeline scripts beside this one import its reader, leave-out rules, colours and
page writer. Python 3, stdlib only. Exit 0 when the files are written, 2 when the folder cannot
be read or the output folder is refused.
"""
import argparse
import datetime
import json
import re
import sys
import urllib.request
from pathlib import Path

# Placement, not a graph: count.py in the read skill names the same four, so the two counts agree.
PLACEMENT = {"map", "pin", "marker", "zone"}
EXT_PREFIXES = ("x_", "atlas_", "shadow_")
NOT_LINKS = {"id", "world", "type", "element_id"}
# The four colour groups, named by their colours (schema-dist serial 86, 2026-10-28): a visual
# aid for drawing the 22 types, not part of the standard, and never shown as a label. The wire
# key on a node stays `family`.
FAMILY_ORDER = ("blue", "green", "pink", "amber")
PRESENTATION_URL = "https://raw.githubusercontent.com/OnlyWorlds/schema-dist/main/presentation.json"
# The groups as presentation.json listed them at serial 86: used only when the fetch fails, so a
# node still has a group; the colours then fall back to greys.
OFFLINE_FAMILY = {
    "character": "blue", "collective": "blue", "creature": "blue", "family": "blue",
    "institution": "blue", "species": "blue",
    "location": "green", "map": "green", "marker": "green", "object": "green", "pin": "green",
    "zone": "green",
    "construct": "pink", "language": "pink", "law": "pink", "title": "pink", "trait": "pink",
    "ability": "amber", "event": "amber", "narrative": "amber", "phenomenon": "amber",
    "relation": "amber",
}
GREYS = {"blue": ("#3d3d3d", "#e0e0e0"), "green": ("#5f5f5f", "#bdbdbd"),
         "pink": ("#818181", "#9a9a9a"), "amber": ("#a3a3a3", "#777777")}
NO_FAMILY = ("#9e9e9e", "#8a8a8a")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
# The room profile's nine pairs (schema-dist profiles/room.md; principles §4). count.py in the
# read skill holds the same table and rule: a skill installs alone, so the two cannot share a
# module, and testing/test_room_pairs.py keeps them equal and runs the profile's fixture.
ROOM_PAIRS = {("narrative", "message"), ("narrative", "board"), ("relation", "work item"),
              ("construct", "spec"), ("relation", "heart"), ("relation", "take"),
              ("relation", "vote"), ("event", "sitting"), ("character", "member")}
# The charter profile's three reading aids (schema-dist profiles/charter.md), matched like the
# room's pairs with the mark x_charter_of; count.py holds the same table, kept equal by the test.
CHARTER_PAIRS = {("law", "charter"), ("construct", "guide"), ("construct", "domain")}
# Trimmed as the room profile defines it: exactly Unicode's White_Space code points, so a file
# separator (U+001C, which str.strip() also removes) or a byte order mark stays in the word.
ROOM_WS = ("\t\n\x0b\x0c\r \x85\xa0         "
           "       　")


# ---------------------------------------------------------------- reading
# read_json and load_world are copied from the read skill's scripts/consistency.py (its folder
# reader), so the three skills that read folders read them the same way.

def read_json(path):
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return json.loads(fh.read())


def load_world(folder):
    world = {}
    if (folder / "world.json").exists():
        world = read_json(folder / "world.json")
    elements, skipped = {}, []
    for base in ("elements", "spatial"):
        for f in sorted((folder / base).glob("*/*.json")):
            try:
                d = read_json(f)
            except (ValueError, OSError) as e:
                skipped.append(f"{f.relative_to(folder).as_posix()}: does not parse ({e})")
                continue
            if not isinstance(d, dict) or not d.get("id"):
                skipped.append(f"{f.relative_to(folder).as_posix()}: no id")
                continue
            t = str(d.get("type") or f.parent.name).lower()
            rel = f.relative_to(folder).as_posix()
            if rel.startswith("elements/"):
                rel = rel[len("elements/"):]
            if d["id"] in elements:
                skipped.append(f"{rel}: id {d['id']} also in {elements[d['id']]['_file']}")
                continue
            d["_type"], d["_file"] = t, rel
            # Atlas's older pin and marker spellings (world-folder.md, writer rules)
            for old, new in (("map_id", "map"), ("zone_id", "zone")):
                if old in d and new not in d:
                    d[new] = d[old]
            elements[d["id"]] = d
    return world, elements, skipped


def open_folder(path):
    """(folder, world, elements, skipped), or exit 2 when there is no world to read."""
    folder = Path(path).resolve()
    if not folder.is_dir():
        sys.exit(f"Not a folder: {path}")
    world, elements, skipped = load_world(folder)
    if not world and not elements:
        print(f"No world.json and no elements/ in {folder}", file=sys.stderr)
        sys.exit(2)
    return folder, world, elements, skipped


def fold(v):
    return str(v).strip().casefold() if isinstance(v, str) else ""


def room_word(v):
    return v.strip(ROOM_WS).casefold() if isinstance(v, str) else ""


def mark_present(value):
    """The profiles' presence rule: null is absent, a string counts only when something is left
    after trimming, any other value (a number, an object) counts; the value is never compared."""
    return value is not None and (not isinstance(value, str) or value.strip(ROOM_WS) != "")


def pair_of(e):
    return room_word(e.get("type") or e["_type"]), room_word(e.get("supertype"))


def is_room(e):
    return pair_of(e) in ROOM_PAIRS and mark_present(e.get("x_room_of"))


def is_reading_aid(e):
    """The charter profile's reader rule: one of the three pairs AND the mark x_charter_of."""
    return pair_of(e) in CHARTER_PAIRS and mark_present(e.get("x_charter_of"))


def left_out_reason(e, room=False, proposed=False, hidden=False):
    """Why an element is not drawn (reading aid, room, proposed, hidden), or None. A reading aid
    has no flag: the front door shows it, a lore view never does."""
    if is_reading_aid(e):
        return "reading aid"
    if not room and is_room(e):
        return "room"
    if not proposed and e.get("x_review_proposed") not in (None, False, "", [], {}):
        return "proposed"
    if not hidden and e.get("hidden") is True:
        return "hidden"
    return None


def label(e):
    return e.get("name") or f"(unnamed {str(e['id'])[:8]})"


def first_sentence(s, n=160):
    """The platform's own cut of a description (keel's web/public_page.first_sentence)."""
    s = re.sub(r"\s+", " ", (s or "").strip())
    m = re.match(r"(.{20,%d}?[.!?])(\s|$)" % n, s)
    return m.group(1) if m else (s[:n].rstrip() + ("..." if len(s) > n else ""))


# ---------------------------------------------------------------- colours

def presentation(offline=False, path=None):
    """({type: family}, {family: [light, dark]}, a line saying where they came from)."""
    raw, source = None, None
    if path:
        try:
            raw, source = read_json(Path(path)), f"presentation.json from {path}"
        except (ValueError, OSError) as e:
            source = f"neutral greys ({path} does not read: {e})"
    elif not offline:
        try:
            req = urllib.request.Request(PRESENTATION_URL, headers={"User-Agent": "onlyworlds-draw"})
            with urllib.request.urlopen(req, timeout=8) as r:
                raw = json.loads(r.read(1_000_000).decode("utf-8"))
            source = "schema-dist presentation.json, fetched " + now()
        except (OSError, ValueError) as e:
            source = f"neutral greys (presentation.json not fetched: {e.__class__.__name__})"
    else:
        source = "neutral greys (offline)"
    fam_of, colors = dict(OFFLINE_FAMILY), {f: list(GREYS[f]) for f in FAMILY_ORDER}
    try:
        types = raw["types"]
        fams = raw["colors"]["families"]
        order = list(raw["colors"]["order"])
        # A word the file's own order does not list fails loudly, never a default colour
        # (the lens profile's rule, serial 87): a silent grey would hide a drifted reader.
        for t in OFFLINE_FAMILY:
            word = types[t].get("family")
            if word not in order:
                sys.exit(f"presentation.json gives {t} the colour group {word!r}, which its "
                         f"colors.order ({', '.join(order)}) does not list; nothing drawn.")
        read_fam = {t: types[t]["family"] for t in OFFLINE_FAMILY}
        read_col = {f: [fams[f]["light"], fams[f]["dark"]] for f in order}
        if not all(HEX.match(c) for v in read_col.values() for c in v):
            raise ValueError("unexpected shape")
        fam_of, colors = read_fam, read_col
    except (TypeError, KeyError, AttributeError, ValueError):
        if raw is not None:
            source = "neutral greys (presentation.json has an unexpected shape)"
    colors["_none"] = list(NO_FAMILY)
    return fam_of, colors, source


# ---------------------------------------------------------------- output

def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def out_folder(folder, out):
    """The output folder: draw/ beside the world unless --out names one; never inside the
    world's elements/, spatial/ or records/."""
    target = Path(out).resolve() if out else folder.parent / "draw"
    for inner in ("elements", "spatial", "records"):
        guard = folder / inner
        if target == guard or guard in target.parents:
            print(f"Refused: {target} is inside the world's {inner}/; output never goes there",
                  file=sys.stderr)
            sys.exit(2)
    target.mkdir(parents=True, exist_ok=True)
    return target


def head_line(folder, world):
    """The world and the folder's own name, never a path: a page may be shared."""
    slice_ = world.get("exported_as")
    s = f"{world.get('name') or folder.name}: true as of {now()}, read from the folder {folder.name}"
    return s + (f" (the {slice_} slice of the world)" if isinstance(slice_, str) and slice_ else "")


def count_line(counts):
    """The left-out counts per reason; the reading aids are said apart, once (aids_line)."""
    return ", ".join(f"{n} {why}" for why, n in counts.items() if n and why != "reading aid") or "nothing"


def aids_line(counts):
    """The charter profile's sentence beside a lore view's count, once, when the world has aids."""
    n = counts.get("reading aid", 0)
    return f" The three reading aids are not drawn ({n} element{'' if n == 1 else 's'})." if n else ""


def embed(data):
    """JSON safe inside a <script> element: no '<' survives, and no raw non-ASCII."""
    return json.dumps(data, ensure_ascii=True, separators=(",", ":")).replace("<", "\\u003c")


PAGE_CSS = """
:root{color-scheme:light dark;--bg:#fafaf8;--fg:#1d1d1b;--muted:#6b6b66;--line:#d6d6d0;--panel:#ffffff;--hi:#c2410c}
@media (prefers-color-scheme:dark){:root{--bg:#121211;--fg:#ecece8;--muted:#9a9a94;--line:#3a3a37;--panel:#1c1c1a;--hi:#fb923c}}
*{box-sizing:border-box}html,body{margin:0;height:100%}
body{background:var(--bg);color:var(--fg);font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;display:flex;flex-direction:column}
header,footer{padding:8px 16px;color:var(--muted);font-size:12.5px}
header b{color:var(--fg);font-size:15px;margin-right:8px}
footer{border-top:1px solid var(--line)}
main{flex:1;display:flex;min-height:0}
#stage{flex:1;min-width:0;position:relative}
svg{width:100%;height:100%;display:block;cursor:grab;touch-action:none}
aside{width:300px;max-width:42vw;border-left:1px solid var(--line);background:var(--panel);overflow:auto;padding:12px 14px}
aside h2{font-size:15px;margin:0 0 2px}aside .k{color:var(--muted);font-size:12px}
aside ul{list-style:none;padding:0;margin:6px 0}aside li{padding:2px 0}
aside a{color:inherit;cursor:pointer;text-decoration:underline;text-decoration-color:var(--line)}
input{width:100%;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font:inherit}
.sw{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px;vertical-align:baseline}
label{display:block;cursor:pointer;font-size:13px}
header{overflow-wrap:anywhere}
@media (max-width:699px){html,body{height:auto}body{display:block}main{display:block}#stage{height:72vh;min-height:320px}
aside{width:auto;max-width:none;border-left:0;border-top:1px solid var(--line);overflow:visible}}
"""


def write_page(path, title, head, foot, data, css, js):
    """One HTML file: the data inline as JSON, the script inline, no outside request of its own."""
    foot_html = "".join(f"<div>{html_text(x)}</div>" for x in foot)
    page = ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            f"<title>{html_text(title)}</title><style>{PAGE_CSS}{css}</style></head><body>"
            f"<header><b>{html_text(title)}</b>{html_text(head)}</header>"
            "<main><div id=\"stage\"><svg id=\"g\"></svg></div><aside id=\"side\"></aside></main>"
            f"<footer>{foot_html}<div id=\"ms\"></div></footer>"
            f"<script id=\"data\" type=\"application/json\">{embed(data)}</script>"
            f"<script>{js}</script></body></html>\n")
    Path(path).write_text(page, encoding="utf-8", newline="\n")


def html_text(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


# The three pages' shared helpers (BASE_JS), and pan and zoom by the viewBox (VIEW_JS: the graph
# and the map; the timeline zooms its own axis).
BASE_JS = r"""
const NS='http://www.w3.org/2000/svg',svg=document.getElementById('g'),side=document.getElementById('side');
function el(t,a,p){const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function h(t,txt,p,cls){const e=document.createElement(t);if(txt!=null)e.textContent=txt;if(cls)e.className=cls;if(p)p.appendChild(e);return e}
const dark=matchMedia('(prefers-color-scheme: dark)').matches;
const D=JSON.parse(document.getElementById('data').textContent);
const col=f=>(D.colors[f]||D.colors._none)[dark?1:0];
"""
VIEW_JS = BASE_JS + r"""
let vb=[0,0,100,100];function setVB(){svg.setAttribute('viewBox',vb.join(' '))}
function fitTo(x0,y0,x1,y1){const r=svg.getBoundingClientRect(),w=Math.max(x1-x0,1),hh=Math.max(y1-y0,1),s=Math.max(w/Math.max(r.width,1),hh/Math.max(r.height,1));
 const W=r.width*s,H=r.height*s;vb=[x0-(W-w)/2,y0-(H-hh)/2,W,H];setVB()}
function toWorld(cx,cy){const r=svg.getBoundingClientRect();return[vb[0]+(cx-r.left)/r.width*vb[2],vb[1]+(cy-r.top)/r.height*vb[3]]}
svg.addEventListener('wheel',ev=>{ev.preventDefault();const[x,y]=toWorld(ev.clientX,ev.clientY),k=ev.deltaY>0?1.15:1/1.15;
 vb=[x-(x-vb[0])*k,y-(y-vb[1])*k,vb[2]*k,vb[3]*k];setVB()},{passive:false});
let drag=null;svg.addEventListener('pointerdown',ev=>{drag=[ev.clientX,ev.clientY,vb[0],vb[1],false];svg.setPointerCapture(ev.pointerId)});
svg.addEventListener('pointermove',ev=>{if(!drag)return;const r=svg.getBoundingClientRect(),dx=ev.clientX-drag[0],dy=ev.clientY-drag[1];
 if(Math.abs(dx)+Math.abs(dy)>3)drag[4]=true;vb[0]=drag[2]-dx/r.width*vb[2];vb[1]=drag[3]-dy/r.height*vb[3];setVB()});
svg.addEventListener('pointerup',ev=>{const moved=drag&&drag[4];drag=null;if(!moved&&window.onTap)onTap(ev)});
"""

GRAPH_JS = VIEW_JS + r"""
const G=D.graph,N=G.nodes.length,E=G.edges,t0=performance.now();
const deg=new Array(N).fill(0),inc=G.nodes.map(()=>[]);
E.forEach((e,i)=>{deg[e[0]]++;deg[e[1]]++;inc[e[0]].push(i);inc[e[1]].push(i)});
const X=new Float64Array(N),Y=new Float64Array(N),K=40,CUT=(6*K)*(6*K);
(function(){const it=N>800?60:N>300?150:300,dx=new Float64Array(N),dy=new Float64Array(N);let t=K*2;
 for(let i=0;i<N;i++){const a=i*2.399963,r=K*Math.sqrt(i+.5);X[i]=r*Math.cos(a);Y[i]=r*Math.sin(a)}
 for(let s=0;s<it;s++){dx.fill(0);dy.fill(0);
  for(let i=0;i<N;i++)for(let j=i+1;j<N;j++){let ex=X[i]-X[j],ey=Y[i]-Y[j];const d2=ex*ex+ey*ey+.01;if(d2>CUT)continue;const f=K*K/d2;ex*=f;ey*=f;dx[i]+=ex;dy[i]+=ey;dx[j]-=ex;dy[j]-=ey}
  for(const e of E){const a=e[0],b=e[1],ex=X[a]-X[b],ey=Y[a]-Y[b],f=Math.sqrt(ex*ex+ey*ey)/K;dx[a]-=ex*f;dy[a]-=ey*f;dx[b]+=ex*f;dy[b]+=ey*f}
  for(let i=0;i<N;i++){dx[i]-=X[i]*.03;dy[i]-=Y[i]*.03;const l=Math.hypot(dx[i],dy[i]);if(l>0){const m=Math.min(l,t)/l;X[i]+=dx[i]*m;Y[i]+=dy[i]*m}}
  t=Math.max(t*.97,1)}})();
const vp=el('g',{},svg),eg=el('g',{stroke:dark?'#55554f':'#c4c4bd','stroke-width':1},vp),ng=el('g',{},vp),lg=el('g',{'font-size':11,fill:'currentColor'},vp);
const R=i=>4+Math.min(10,Math.sqrt(deg[i])*1.6);
const lines=E.map(e=>el('line',{x1:X[e[0]],y1:Y[e[0]],x2:X[e[1]],y2:Y[e[1]]},eg));
const dots=G.nodes.map((n,i)=>{const c=el('circle',{cx:X[i],cy:Y[i],r:R(i),fill:col(n.family),stroke:dark?'#121211':'#fafaf8','stroke-width':1.2},ng);
 c.dataset.i=i;h('title',n.name+' ('+n.type+(n.sup?', '+n.sup:'')+')',c);return c});
const most=[...G.nodes.keys()].sort((a,b)=>deg[b]-deg[a]).slice(0,N<=60?N:40);
// Labels, greedy by degree: one is drawn only where it meets no label already placed; a hidden
// one shows on hover and when its node or a neighbour is clicked, and the head counts them.
const labs=new Map(),boxes=[];let clash=0;
for(const i of most){const t=el('text',{x:X[i]+R(i)+2,y:Y[i]+4},lg);t.textContent=G.nodes[i].name;const b=t.getBBox();
 if(boxes.some(q=>b.x<q.x+q.width&&q.x<b.x+b.width&&b.y<q.y+q.height&&q.y<b.y+b.height)){t.remove();clash++;continue}
 boxes.push({x:b.x,y:b.y,width:b.width,height:b.height});labs.set(i,t)}
const unlabelled=N-labs.size;
if(unlabelled){const hd=document.querySelector('header');hd.append(' · '+unlabelled+' label'+(unlabelled===1?'':'s')+' hidden ('+
 (clash?clash+' would overlap':'')+(clash&&unlabelled>clash?', ':'')+(unlabelled>clash?(unlabelled-clash)+' past the '+most.length+' most linked':'')+'): hover or click a dot')}
let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;for(let i=0;i<N;i++){x0=Math.min(x0,X[i]);y0=Math.min(y0,Y[i]);x1=Math.max(x1,X[i]);y1=Math.max(y1,Y[i])}
const fit=()=>N?fitTo(x0-60,y0-40,x1+120,y1+40):fitTo(0,0,100,100);fit();
const hiddenType=new Set(),HI=getComputedStyle(document.body).getPropertyValue('--hi').trim();
function shown(i){return!hiddenType.has(G.nodes[i].type)}
function paint(sel){const near=new Set();if(sel!=null){near.add(sel);for(const k of inc[sel]){near.add(E[k][0]);near.add(E[k][1])}}
 dots.forEach((c,i)=>{c.style.display=shown(i)?'':'none';c.style.opacity=sel==null||near.has(i)?1:.15});
 lines.forEach((l,k)=>{const e=E[k],on=shown(e[0])&&shown(e[1]);l.style.display=on?'':'none';
  const lit=sel!=null&&(e[0]===sel||e[1]===sel);l.style.opacity=sel==null?.7:lit?1:.06;if(lit)l.setAttribute('stroke',HI);else l.removeAttribute('stroke')});
 for(const[i,t]of labs)t.style.display=shown(i)&&(sel==null||near.has(i))?'':'none';
 for(const i of near)if(!labs.has(i)&&sel!=null){const t=el('text',{x:X[i]+R(i)+2,y:Y[i]+4},lg);t.textContent=G.nodes[i].name;t.dataset.tmp=1}
 if(sel==null)lg.querySelectorAll('[data-tmp]').forEach(t=>t.remove())}
function legend(){side.textContent='';h('input',null,side).placeholder='Find an element by name';const inp=side.firstChild;
 const dl=h('datalist',null,side);dl.id='names';inp.setAttribute('list','names');G.nodes.forEach(n=>{const o=h('option',null,dl);o.value=n.name});
 inp.addEventListener('change',()=>{const q=inp.value.trim().toLowerCase();let i=G.nodes.findIndex(n=>n.name.toLowerCase()===q);
  if(i<0)i=G.nodes.findIndex(n=>n.name.toLowerCase().includes(q));if(i>=0)select(i,true)});
 h('p',N+' elements, '+E.length+' links'+(unlabelled?'; '+unlabelled+' names hidden where they would crowd: hover or click a dot':''),side,'k');
 const byT={};G.nodes.forEach(n=>{(byT[n.type]=byT[n.type]||{n:0,f:n.family}).n++});
 for(const f of D.families){const ts=Object.keys(byT).filter(t=>byT[t].f===f);if(!ts.length)continue;
  const d=h('div',null,side);const s=h('span',null,d,'sw');s.style.background=col(f);h('b',f[0].toUpperCase()+f.slice(1),d);
  for(const t of ts){const lb=h('label',null,side),cb=h('input',null,lb);cb.type='checkbox';cb.checked=!hiddenType.has(t);cb.style.width='auto';
   lb.append(' '+t+' ('+byT[t].n+')');cb.addEventListener('change',()=>{cb.checked?hiddenType.delete(t):hiddenType.add(t);paint(null)})}}}
function select(i,center){paint(i);const n=G.nodes[i];side.textContent='';const back=h('a','All elements',side);back.onclick=()=>{paint(null);legend()};
 h('h2',n.name,side);h('div',n.type+(n.sup?' · '+n.sup:''),side,'k');if(n.desc)h('p',n.desc,side);
 const out=inc[i].filter(k=>E[k][0]===i),inn=inc[i].filter(k=>E[k][1]===i&&E[k][0]!==i);
 for(const[ttl,ks,other]of[['Links out',out,1],['Linked from',inn,0]]){if(!ks.length)continue;h('b',ttl+' ('+ks.length+')',side);const ul=h('ul',null,side);
  for(const k of ks){const j=E[k][other],li=h('li',null,ul);h('span',E[k][2]+': ',li,'k');const a=h('a',G.nodes[j].name,li);a.onclick=()=>select(j,true)}}
 if(center){const w=vb[2],hh=vb[3];vb=[X[i]-w/2,Y[i]-hh/2,w,hh];setVB()}}
dots.forEach((c,i)=>{c.addEventListener('pointerenter',()=>{if(labs.has(i)||c.style.display==='none')return;const t=el('text',{x:X[i]+R(i)+2,y:Y[i]+4},lg);t.textContent=G.nodes[i].name;t.dataset.hov=1});
 c.addEventListener('pointerleave',()=>lg.querySelectorAll('[data-hov]').forEach(t=>t.remove()))});
window.onTap=ev=>{const t=ev.target;if(t.tagName==='circle')select(+t.dataset.i,false);else{paint(null);legend()}};
legend();paint(null);
const ms=Math.round(performance.now()-t0);document.body.dataset.ms=ms;document.getElementById('ms').textContent='Laid out and drawn in '+ms+' ms.';
"""


# ---------------------------------------------------------------- the graph

def link_targets(e):
    """(field, [ids]) for every schema field whose value is an id or a list of them: the
    single-valued fields first, then the lists, each in the file's own key order."""
    singles, multis = [], []
    for k, v in e.items():
        if k.startswith("_") or k in NOT_LINKS or k.startswith(EXT_PREFIXES):
            continue
        if isinstance(v, str) and v:
            singles.append((k, [v]))
        elif isinstance(v, list) and v and all(isinstance(x, str) for x in v):
            multis.append((k, v))
    return singles + multis


def build_graph(world_name, kept, fam_of):
    order = {f: i for i, f in enumerate(FAMILY_ORDER)}
    kept = sorted(kept, key=lambda e: (order.get(fam_of.get(e["_type"]), 9), e["_type"],
                                       fold(e.get("name")), str(e["id"])))
    nodes = [{"id": str(e["id"]), "name": e.get("name") or "", "type": e["_type"],
              "family": fam_of.get(e["_type"], ""), "sup": e.get("supertype") or "",
              "desc": first_sentence(e["description"]) if isinstance(e.get("description"), str)
              and e["description"].strip() else ""} for e in kept]
    index = {n["id"]: i for i, n in enumerate(nodes)}
    edges = []
    for a, e in enumerate(kept):
        seen = set()
        for field, targets in link_targets(e):
            for t in targets:
                b = index.get(t)
                if b is None or b == a or (b, field) in seen:
                    continue
                seen.add((b, field))
                edges.append([a, b, field])
    return {"name": world_name, "nodes": nodes, "edges": edges}


def focus_ids(graph_nodes, graph_edges, focus, depth):
    """The node indices within `depth` links of any focus, or exit with what matched."""
    starts = set()
    for f in focus:
        hits = [i for i, n in enumerate(graph_nodes) if n["id"] == f or fold(n["name"]) == fold(f)]
        if not hits:
            near = [n["name"] for n in graph_nodes if fold(f) in fold(n["name"])][:10]
            print(f"No element named or with id {f!r}" + (f"; near: {', '.join(near)}" if near else ""),
                  file=sys.stderr)
            sys.exit(2)
        starts.update(hits)
    adj = {i: set() for i in range(len(graph_nodes))}
    for a, b, _ in graph_edges:
        adj[a].add(b)
        adj[b].add(a)
    seen, ring = set(starts), set(starts)
    for _ in range(depth):
        ring = {j for i in ring for j in adj[i]} - seen
        seen |= ring
    return seen


def main(argv):
    ap = argparse.ArgumentParser(description="Draw a world folder as a graph.")
    ap.add_argument("folder")
    ap.add_argument("--out")
    ap.add_argument("--focus", action="append", default=[])
    ap.add_argument("--depth", type=int, default=1)
    ap.add_argument("--type", action="append", default=[])
    ap.add_argument("--room", action="store_true")
    ap.add_argument("--proposed", action="store_true")
    ap.add_argument("--hidden", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--presentation")
    a = ap.parse_args(argv)

    folder, world, elements, skipped = open_folder(a.folder)
    fam_of, colors, colour_source = presentation(a.offline, a.presentation)
    left = {"placement (map, pin, marker, zone)": 0, "reading aid": 0, "room": 0, "proposed": 0,
            "hidden": 0, "outside --type": 0, "outside the focus": 0}
    kept = []
    for e in elements.values():
        if e["_type"] in PLACEMENT:
            left["placement (map, pin, marker, zone)"] += 1
            continue
        why = left_out_reason(e, a.room, a.proposed, a.hidden)
        if why:
            left[why] += 1
            continue
        if a.type and e["_type"] not in {t.lower() for t in a.type}:
            left["outside --type"] += 1
            continue
        kept.append(e)
    name = world.get("name") or folder.name
    graph = build_graph(name, kept, fam_of)
    if a.focus:
        keep = focus_ids(graph["nodes"], graph["edges"], a.focus, max(a.depth, 0))
        left["outside the focus"] = len(graph["nodes"]) - len(keep)
        graph = build_graph(name, [elements[graph["nodes"][i]["id"]] for i in sorted(keep)], fam_of)

    out = out_folder(folder, a.out)
    with open(out / "graph.json", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(graph, ensure_ascii=False, indent=2) + "\n")
    head = head_line(folder, world)
    foot = [f"{len(graph['nodes'])} elements and {len(graph['edges'])} links drawn, of "
            f"{len(elements)} in the folder. Left out: {count_line(left)}.{aids_line(left)}",
            f"Colours: {colour_source}. Colour carries the type's group, never a label; the type is in each node's "
            "title and the legend."]
    if skipped:
        foot.append(f"{len(skipped)} files not read: " + "; ".join(skipped[:5])
                    + (" ..." if len(skipped) > 5 else ""))
    data = {"graph": graph, "colors": colors, "families": list(FAMILY_ORDER)}
    write_page(out / "graph.html", f"{name}: graph", head, foot, data, "", GRAPH_JS)

    print(f"# Graph of {name}\n")
    print(head + "\n")
    for line in foot:
        print(f"- {line}")
    if len(graph["nodes"]) > 300 and not a.focus:
        print(f"- {len(graph['nodes'])} nodes: above about 300 the picture crowds; a focus "
              "(--focus NAME --depth 1) or a type (--type) reads better.")
    print(f"\nWrote {out / 'graph.json'}\nWrote {out / 'graph.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
