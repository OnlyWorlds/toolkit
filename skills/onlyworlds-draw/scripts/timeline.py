"""Draw a world folder's dated elements on a timeline: timeline.html.

Reads a world folder with graph.py's reader and writes one page into the output folder, never
into the world. Every integer date field is placed, in the world's time_basic_unit: start_date
and end_date, grant_date and revoke_date (spans), birth_date, founding_date, formation_date and
date (points). Rows are grouped by type in the family order; the world's time_current is a line.
Eras are Constructs with both a start_date and an end_date, drawn as bands behind the rows.

The axis runs over the world's time_range_min..time_range_max (over the dates themselves when
the world sets no range); a date outside it is counted, never drawn, and a span crossing an edge
is cut there. An element with no date is counted as not placed, never placed. A span whose end
comes before its start is drawn at its start and counted.

A calendar (atlas_calendar, schema-dist profiles/calendar.md) labels the dates when one reads:
the only one in the world, or the one --calendar names. A value that is not a calendar leaves
the dates as bare numbers, and the script says so. The axis itself counts plain steps. The
calendar is read by the onlyworlds package (onlyworlds.calendar), never by a copy here.

Room, proposed and hidden elements are left out unless a flag asks for them.

Usage:
    python timeline.py WORLD_FOLDER [--out DIR] [--type TYPE ...] [--calendar NAME_OR_ID]
                       [--room] [--proposed] [--hidden] [--offline] [--presentation PATH]

Python 3.12+; the standard library and the onlyworlds package (>=0.68.1, for the calendar).
Exit 0 on a page, 2 when the folder cannot be read or the package is missing.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from graph import (BASE_JS, FAMILY_ORDER, count_line, fold, head_line, label,  # noqa: E402
                   left_out_reason, open_folder, out_folder, presentation, write_page)

try:
    from onlyworlds.calendar import format_step, read_calendar_value  # noqa: E402
except ImportError:
    print('The timeline reads calendars through the onlyworlds package, which is missing or too old: '
          'run pip install "onlyworlds>=0.68.1" (Python 3.12+) and draw again.', file=sys.stderr)
    sys.exit(2)

SPANS = (("start_date", "end_date"), ("grant_date", "revoke_date"))
POINTS = ("birth_date", "founding_date", "formation_date", "date")


def _whole(v):
    """An integer date: a whole number that is not a boolean."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return False
    return not isinstance(v, float) or v.is_integer()


# ---------------------------------------------------------------- the timeline

def dated(e):
    """(field_a, a, field_b, b) for each date group the element holds; b is None for a point."""
    out = []
    for fa, fb in SPANS:
        a = e.get(fa) if _whole(e.get(fa)) else None
        b = e.get(fb) if _whole(e.get(fb)) else None
        if a is not None or b is not None:
            out.append((fa, None if a is None else int(a), fb, None if b is None else int(b)))
    for f in POINTS:
        if _whole(e.get(f)):
            out.append((f, int(e[f]), None, None))
    return out


def pick_calendar(kept, want):
    """(the element, the calendar) the page speaks, or (None, None); and the lines to say."""
    found = [(e, read_calendar_value(e["atlas_calendar"])) for e in kept.values()
             if e.get("atlas_calendar") is not None]
    found.sort(key=lambda ec: (fold(label(ec[0])), str(ec[0]["id"])))
    notes = [f"{label(e)} carries an atlas_calendar that is not a calendar: its dates stay numbers"
             for e, c in found if c is None]
    readable = [(e, c) for e, c in found if c]
    if want:
        hit = [(e, c) for e, c in readable if e["id"] == want or fold(label(e)) == fold(want)]
        if not hit:
            notes.append(f"No readable calendar named or with id {want!r}: the dates stay numbers")
            return None, None, notes
        readable = hit
    if not readable:
        return None, None, notes
    if len(readable) > 1:
        notes.append(f"{len(readable)} calendars read; this page speaks {label(readable[0][0])} "
                     f"(--calendar names another: {', '.join(label(e) for e, _ in readable[1:])})")
    return readable[0][0], readable[0][1], notes


TL_CSS = """
#stage{overflow:auto}#g{height:auto;cursor:grab}
.it{cursor:pointer}button{font:inherit;padding:3px 10px;margin:0 4px 6px 0;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);cursor:pointer}
"""

TL_JS = BASE_JS + r"""
const T=D.tl,t0=performance.now(),stage=document.getElementById('stage'),PL=20,PR=24,ROW=18;
const muted=getComputedStyle(document.body).getPropertyValue('--muted').trim(),hi=getComputedStyle(document.body).getPropertyValue('--hi').trim();
let d0=T.min,d1=T.max,sel=null;
const X=v=>PL+(v-d0)/(d1-d0)*(stage.clientWidth-PL-PR);
function nice(r){const p=Math.pow(10,Math.floor(Math.log10(r))),m=r/p;return(m<1.5?1:m<3.5?2:m<7.5?5:10)*p}
function when(it){return it.wa+(it.b!=null&&it.b!==it.a?' to '+it.wb:'')}
function render(){svg.textContent='';const w=stage.clientWidth,bands=el('g',{},svg),grid=el('g',{},svg),body=el('g',{},svg);let y=52;
 for(const g of T.groups){const hd=el('text',{x:PL,y:y,'font-weight':600,fill:'currentColor','font-size':13},body);hd.textContent=(g.label||g.type)+' ('+g.items.length+')';y+=6;
  const lanes=[];for(const it of g.items){const a=Math.max(it.a,T.min),b=it.b==null?a:Math.min(it.b,T.max),x1=X(a),x2=X(b),lw=it.name.length*6.6+16;
   let L=lanes.findIndex(e=>e<x1-6);if(L<0){L=lanes.length;lanes.push(0)}lanes[L]=Math.max(x1,x2)+lw;
   if(Math.max(x1,x2)+lw<0||x1>w)continue;
   const yy=y+L*ROW+10,c=col(g.family),gg=el('g',{class:'it'},body);gg.dataset.k=it.k;
   if(it.b!=null&&x2-x1>=2)el('rect',{x:x1,y:yy-5,width:x2-x1,height:10,rx:3,fill:c,stroke:it.k===sel?hi:'none','stroke-width':2},gg);
   else el('circle',{cx:x1,cy:yy,r:5,fill:c,stroke:it.k===sel?hi:'none','stroke-width':2},gg);
   const left=Math.max(x1,x2)+lw>w&&x1-lw>0,t=el('text',{x:left?x1-8:Math.max(x1,x2)+8,y:yy+4,fill:'currentColor','font-size':12,'text-anchor':left?'end':'start'},gg);t.textContent=it.name;h('title',it.name+': '+when(it),gg)}
  y+=Math.max(lanes.length,1)*ROW+18}
 const H=Math.max(y,stage.clientHeight-4);svg.setAttribute('width',w);svg.setAttribute('height',H);svg.style.height=H+'px';
 const st=Math.max(1,nice((d1-d0)/Math.max(2,Math.floor(w/110))));
 for(let v=Math.ceil(d0/st)*st;v<=d1;v+=st){const x=X(v);el('line',{x1:x,x2:x,y1:22,y2:H,stroke:muted,'stroke-opacity':.25},grid);const t=el('text',{x:x+3,y:16,'font-size':11,fill:muted},grid);t.textContent=v}
 for(const e of T.bands){const x1=X(Math.max(e.a,d0)),x2=X(Math.min(e.b,d1));if(x2<=x1)continue;
  el('rect',{x:x1,y:22,width:x2-x1,height:H-22,fill:col(T.groups[0].family),'fill-opacity':.07},bands)}
 if(T.current!=null&&T.current>=d0&&T.current<=d1){const x=X(T.current);el('line',{x1:x,x2:x,y1:22,y2:H,stroke:hi,'stroke-dasharray':'4 3'},grid);const t=el('text',{x:x+3,y:46,'font-size':11,fill:hi},grid);t.textContent='now: '+T.currentWords}}
function zoom(k,cx){const r=svg.getBoundingClientRect(),v=d0+((cx==null?r.width/2:cx-r.left)-PL)/(r.width-PL-PR)*(d1-d0);
 let s=Math.max((d1-d0)*k,4);d0=v-(v-d0)*s/(d1-d0);d1=d0+s;render()}
svg.addEventListener('wheel',ev=>{if(!ev.ctrlKey&&!ev.metaKey)return;ev.preventDefault();zoom(ev.deltaY>0?1.2:1/1.2,ev.clientX)},{passive:false});
let drag=null;svg.addEventListener('pointerdown',ev=>{drag=[ev.clientX,d0,d1,false]});
svg.addEventListener('pointermove',ev=>{if(!drag)return;const dx=ev.clientX-drag[0];if(Math.abs(dx)>3)drag[3]=true;if(!drag[3])return;
 const per=(drag[2]-drag[1])/(stage.clientWidth-PL-PR);d0=drag[1]-dx*per;d1=drag[2]-dx*per;render()});
svg.addEventListener('pointerup',ev=>{const moved=drag&&drag[3];drag=null;if(moved)return;const g=ev.target.closest('.it');sel=g?+g.dataset.k:null;render();g?detail(T.byK[sel]):panel()});
function controls(){const d=h('div',null,side);for(const[t,f]of[['+',()=>zoom(1/1.5)],['−',()=>zoom(1.5)],['All',()=>{d0=T.min;d1=T.max;render()}]]){const b=h('button',t,d);b.onclick=f}
 h('div','Drag to move along the line; Ctrl and the wheel zoom.',side,'k')}
function panel(){side.textContent='';controls();h('p',T.placed+' dates placed, in '+(T.unit||'steps')+(T.calendar?', read through the calendar '+T.calendar:'')+'.',side,'k');
 for(const g of T.groups){const d=h('div',null,side),s=h('span',null,d,'sw');s.style.background=col(g.family);d.append((g.label||g.type)+' ('+g.items.length+')')}
 if(T.eras)h('p','Eras are Constructs with a start and an end'+(T.bands.length?', shaded behind the rows.':'; they overlap, so they are not shaded.'),side,'k')}
function detail(it){side.textContent='';controls();const a=h('a','All dates',side);a.onclick=()=>{sel=null;render();panel()};
 h('h2',it.name,side);h('div',it.type+(it.sup?' · '+it.sup:''),side,'k');h('p',it.fa.replace('_',' ')+': '+it.wa+(it.b!=null?'; '+it.fb.replace('_',' ')+': '+it.wb:''),side);if(it.desc)h('p',it.desc,side)}
T.byK={};for(const g of T.groups)for(const it of g.items){it.type=g.type;T.byK[it.k]=it}
render();panel();addEventListener('resize',render);
const ms=Math.round(performance.now()-t0);document.body.dataset.ms=ms;document.getElementById('ms').textContent='Drawn in '+ms+' ms.';
"""


def main(argv):
    ap = argparse.ArgumentParser(description="Draw a world folder's dates on a timeline.")
    ap.add_argument("folder")
    ap.add_argument("--out")
    ap.add_argument("--type", action="append", default=[])
    ap.add_argument("--calendar")
    ap.add_argument("--room", action="store_true")
    ap.add_argument("--proposed", action="store_true")
    ap.add_argument("--hidden", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--presentation")
    a = ap.parse_args(argv)

    folder, world, elements, skipped = open_folder(a.folder)
    name = world.get("name") or folder.name
    left = {"room": 0, "proposed": 0, "hidden": 0, "outside --type": 0}
    kept = {}
    for i, e in elements.items():
        why = left_out_reason(e, a.room, a.proposed, a.hidden)
        if why:
            left[why] += 1
        elif a.type and e["_type"] not in {t.lower() for t in a.type}:
            left["outside --type"] += 1
        else:
            kept[i] = e
    cal_el, cal, notes = pick_calendar(
        {i: e for i, e in elements.items() if not left_out_reason(e, a.room, a.proposed, a.hidden)}, a.calendar)

    def say(v):
        return format_step(cal, int(v)) if cal and v is not None else ("" if v is None else str(v))

    rows, all_dates = [], []
    not_placed = {"with no date": 0, "dated outside the world's range": 0, "spans ending before they start": 0}
    for e in kept.values():
        if e["_type"] in ("map", "pin", "marker"):
            continue
        groups = dated(e)
        if not groups:
            not_placed["with no date"] += 1
            continue
        for fa, va, fb, vb in groups:
            if va is None:
                fa, va, fb, vb = fb, vb, None, None
            elif vb is not None and vb < va:
                not_placed["spans ending before they start"] += 1
                fb, vb = None, None
            era = e["_type"] == "construct" and fa == "start_date" and vb is not None
            rows.append((e, fa, va, fb, vb, era))
            all_dates += [v for v in (va, vb) if v is not None]
    lo, hi = world.get("time_range_min"), world.get("time_range_max")
    if _whole(lo) and _whole(hi) and lo < hi:
        rmin, rmax, range_from = int(lo), int(hi), "the world's time range"
    elif all_dates:
        rmin, rmax, range_from = min(all_dates), max(all_dates), "the dates themselves (the world sets no range)"
        if rmin == rmax:
            rmin, rmax = rmin - 1, rmax + 1
    else:
        rmin, rmax, range_from = 0, 1, "no dates"
    fam_of, colors, colour_source = presentation(a.offline, a.presentation)
    order = {f: i for i, f in enumerate(FAMILY_ORDER)}
    by_type, eras, k = {}, [], 0
    for e, fa, va, fb, vb, era in sorted(rows, key=lambda r: (r[2], fold(label(r[0])))):
        end = va if vb is None else vb
        if end < rmin or va > rmax:
            not_placed["dated outside the world's range"] += 1
            continue
        desc = e.get("description") if isinstance(e.get("description"), str) else ""
        (eras if era else by_type.setdefault(e["_type"], [])).append({
            "k": k, "name": label(e), "sup": e.get("supertype") or "", "desc": desc[:300],
            "fa": fa, "a": va, "fb": fb, "b": vb, "wa": say(va), "wb": say(vb)})
        k += 1
    groups = [{"type": t, "family": fam_of.get(t, ""), "items": its}
              for t, its in sorted(by_type.items(), key=lambda kv: (order.get(fam_of.get(kv[0]), 9), kv[0]))]
    if eras:
        groups.insert(0, {"type": "construct", "label": "eras", "family": fam_of.get("construct", ""), "items": eras})
    placed = sum(len(g["items"]) for g in groups) - len(eras)
    apart = all(x["b"] < y["a"] for x, y in zip(eras, eras[1:], strict=False))
    cur = world.get("time_current") if _whole(world.get("time_current")) else None
    unit = world.get("time_basic_unit") if isinstance(world.get("time_basic_unit"), str) else ""
    tl = {"min": rmin, "max": rmax, "unit": unit, "current": cur, "currentWords": say(cur),
          "calendar": label(cal_el) if cal_el else "", "placed": placed, "groups": groups,
          "eras": len(eras), "bands": eras if apart else []}

    out = out_folder(folder, a.out)
    head = head_line(folder, world)
    foot = [f"{placed} dated elements and {len(eras)} eras placed on {rmin}..{rmax} {unit or 'steps'} "
            f"(from {range_from}). Not placed: {count_line(not_placed)}. Left out: {count_line(left)}.",
            ("Dates read through the calendar " + label(cal_el) + "; the axis counts plain steps.") if cal_el
            else "Dates are the world's plain integers (no calendar reads).",
            f"Colours: {colour_source}."] + notes
    if skipped:
        foot.append(f"{len(skipped)} files not read: " + "; ".join(skipped[:5]) + (" ..." if len(skipped) > 5 else ""))
    write_page(out / "timeline.html", f"{name}: timeline", head, foot, {"tl": tl, "colors": colors}, TL_CSS, TL_JS)

    print(f"# Timeline of {name}\n\n{head}\n")
    for line in foot:
        print(f"- {line}")
    print(f"\nWrote {out / 'timeline.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
