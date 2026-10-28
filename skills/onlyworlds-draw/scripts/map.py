"""Draw a world folder's maps, with their pins and zones: map.html.

Reads a world folder with graph.py's reader and writes one page into the output folder, never
into the world. Every Map element is a canvas: its image_url, width x height pixels. A Pin sits
at its integer x, y counted from the map's BOTTOM-LEFT corner (the page flips y) and names the
element it places (element_type + element_id); its label is that element's name. A Zone is its
Markers on that map, in `order` (markers without one keep the order they were made in), joined
by the zone's `shape`: polygon (closed, the default) or line (open). Atlas's own `atlas_shape`
and a supertype `line` are read when `shape` is not set. Maps nest by parent_map; the page
lists them as a tree and shows one at a time.

Nothing is placed by guess: a pin or marker without integer x and y, or on a map the folder
lacks, is counted as not placed. A map with no width and height takes its image's own size
when the image loads; with neither, its pins are not placed. Room, proposed and hidden
elements (and pins that place one) are left out unless a flag asks for them; the three
reading aids (graph.py's docstring) are left out always and said once in the foot.

A folder with no Map element gets no page: the script says so and prints the parent_location
tree as an outline instead.

Usage:
    python map.py WORLD_FOLDER [--out DIR] [--no-image] [--room] [--proposed] [--hidden]
                  [--offline] [--presentation PATH]

    --no-image   draw the bare frame, without loading the map images (the page's only outside
                 requests are the maps' own image_url)

Python 3, stdlib only. Exit 0 on a page or an outline, 2 when the folder cannot be read.
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from graph import (FAMILY_ORDER, VIEW_JS, aids_line, count_line, fold, head_line, label,  # noqa: E402
                   left_out_reason, open_folder, out_folder, presentation, write_page)


def whole(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return None


def shape_of(z):
    for v in (z.get("shape"), z.get("atlas_shape")):
        if isinstance(v, str) and v.strip():
            return "line" if v.strip().lower() == "line" else "polygon"
    return "line" if fold(z.get("supertype")) == "line" else "polygon"


def outline(elements, kept_ids):
    """The parent_location tree as Markdown, for a world with no map."""
    locs = {i: e for i, e in elements.items() if e["_type"] == "location" and i in kept_ids}
    kids = {}
    for i, e in locs.items():
        p = e.get("parent_location")
        kids.setdefault(p if p in locs else None, []).append(i)
    lines = []

    def walk(i, depth, seen):
        lines.append("  " * depth + f"- {label(locs[i])}")
        for k in sorted(kids.get(i, []), key=lambda k: fold(label(locs[k]))):
            if k not in seen:
                walk(k, depth + 1, seen | {k})
    for root in sorted(kids.get(None, []), key=lambda k: fold(label(locs[k]))):
        walk(root, 0, {root})
    return lines


MAP_CSS = """
#maps a{display:block;padding:2px 0;cursor:pointer}#maps a.on{font-weight:600;color:var(--hi)}
"""

MAP_JS = VIEW_JS + r"""
const M=D.maps,byId=Object.fromEntries(M.map(m=>[m.id,m])),t0=performance.now();let cur=null;
function draw(m){cur=m;svg.textContent='';const w=m.w,hh=m.h;
 if(!w||!hh){if(m.image&&!m.tried&&!D.noImage){m.tried=1;const im=new Image();im.onload=()=>{m.w=im.naturalWidth;m.h=im.naturalHeight;m.sized=1;draw(m)};im.onerror=()=>panel(m,'The image did not load and the map states no size: nothing is placed.');im.src=m.image}
  else panel(m,'This map states no width and height and has no image: its pins and zones are not placed.');return}
 const vp=el('g',{},svg);el('rect',{x:0,y:0,width:w,height:hh,fill:dark?'#20201e':'#efefea',stroke:dark?'#55554f':'#c4c4bd'},vp);
 if(m.image&&!D.noImage)el('image',{href:m.image,x:0,y:0,width:w,height:hh,preserveAspectRatio:'none'},vp);
 const u=Math.max(w,hh)/250;
 for(const z of m.zones){const pts=z.pts.map(p=>p[0]+','+(hh-p[1])).join(' ');const c=col(z.family);
  const s=el(z.shape==='line'?'polyline':'polygon',{points:pts,fill:z.shape==='line'?'none':c,'fill-opacity':.18,stroke:c,'stroke-width':u*.8,'stroke-linejoin':'round'},vp);
  h('title',z.name+' ('+z.shape+', '+z.pts.length+' markers)',s);s.dataset.z=z.i}
 for(const p of m.pins){const g=el('g',{},vp),y=hh-p.y;el('circle',{cx:p.x,cy:y,r:u*1.8,fill:col(p.family),stroke:dark?'#121211':'#fff','stroke-width':u*.5},g);
  const t=el('text',{x:p.x+u*2.6,y:y+u*1.2,'font-size':u*4.2,fill:dark?'#fff':'#111',stroke:dark?'#000':'#fff','stroke-width':u*.9,'paint-order':'stroke'},g);t.textContent=p.label;
  h('title',p.label+(p.type?' ('+p.type+')':'')+' at '+p.x+', '+p.y,g)}
 fitTo(-w*.03,-hh*.03,w*1.03,hh*1.03);panel(m,null)}
function panel(m,note){side.textContent='';h('h2',m.name,side);h('div',(m.w&&m.h?m.w+' × '+m.h+' px'+(m.sized?' (from its image)':''):'no stated size')+(m.loc?' · '+m.loc:''),side,'k');
 if(note)h('p',note,side);if(m.desc)h('p',m.desc,side);
 h('p',m.pins.length+' pins, '+m.zones.length+' zones placed'+(m.unplaced?'; '+m.unplaced+' not placed':''),side,'k');
 if(m.zones.length){h('b','Zones',side);const ul=h('ul',null,side);for(const z of m.zones){const li=h('li',null,ul),s=h('span',null,li,'sw');s.style.background=col(z.family);li.append(z.name+' ('+z.shape+')')}}
 if(m.pins.length){h('b','Pins',side);const ul=h('ul',null,side);for(const p of m.pins){const li=h('li',null,ul),s=h('span',null,li,'sw');s.style.background=col(p.family);li.append(p.label+(p.type?' · '+p.type:''))}}
 h('b','Maps',side);const nav=h('div',null,side);nav.id='maps';
 (function tree(parent,depth){for(const c of M.filter(x=>(x.parent||null)===parent)){const a=h('a',c.name,nav);a.style.paddingLeft=depth*14+'px';if(c===cur)a.className='on';a.onclick=()=>draw(c);if(depth<12)tree(c.id,depth+1)}})(null,0)}
for(const m of M)if(m.parent&&!byId[m.parent])m.parent=null;
if(M.length)draw(M.find(m=>!m.parent)||M[0]);
const ms=Math.round(performance.now()-t0);document.body.dataset.ms=ms;document.getElementById('ms').textContent='Drawn in '+ms+' ms.';
"""


def main(argv):
    ap = argparse.ArgumentParser(description="Draw a world folder's maps.")
    ap.add_argument("folder")
    ap.add_argument("--out")
    ap.add_argument("--no-image", action="store_true")
    ap.add_argument("--room", action="store_true")
    ap.add_argument("--proposed", action="store_true")
    ap.add_argument("--hidden", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--presentation")
    a = ap.parse_args(argv)

    folder, world, elements, skipped = open_folder(a.folder)
    name = world.get("name") or folder.name
    left = {"reading aid": 0, "room": 0, "proposed": 0, "hidden": 0}
    kept = {}
    for i, e in elements.items():
        why = left_out_reason(e, a.room, a.proposed, a.hidden)
        if why:
            left[why] += 1
        else:
            kept[i] = e
    maps = {i: e for i, e in kept.items() if e["_type"] == "map"}
    if not maps:
        print(f"# Maps of {name}\n\nNo Map element in {folder}: there is nothing to place pins "
              "or zones on, and no coordinates are invented. The places as an outline "
              "(the parent_location tree):\n")
        print("\n".join(outline(elements, set(kept))) or "(no Location elements either)")
        return 0

    fam_of, colors, colour_source = presentation(a.offline, a.presentation)
    not_placed = {"pins without integer x and y": 0, "pins on no map in the folder": 0,
                  "pins placing a left-out element": 0, "markers without integer x and y": 0,
                  "markers on no map in the folder": 0, "markers with no zone in the folder": 0}
    pins_by, markers_by = {m: [] for m in maps}, {m: {} for m in maps}
    order_made = {i: n for n, i in enumerate(sorted(
        kept, key=lambda i: (str(kept[i].get("created_at") or ""), kept[i]["_file"])))}
    for e in kept.values():
        if e["_type"] == "pin":
            m = e.get("map")
            if m not in maps:
                not_placed["pins on no map in the folder"] += 1
                continue
            x, y = whole(e.get("x")), whole(e.get("y"))
            if x is None or y is None:
                not_placed["pins without integer x and y"] += 1
                maps[m].setdefault("_unplaced", 0)
                maps[m]["_unplaced"] += 1
                continue
            target = elements.get(e.get("element_id"))
            if target is not None and target["id"] not in kept:
                not_placed["pins placing a left-out element"] += 1
                continue
            t = target["_type"] if target else str(e.get("element_type") or "").lower()
            pins_by[m].append({"x": x, "y": y, "label": label(target) if target else label(e),
                               "type": t, "family": fam_of.get(t, "")})
        elif e["_type"] == "marker":
            m, z = e.get("map"), e.get("zone")
            if m not in maps:
                not_placed["markers on no map in the folder"] += 1
            elif z not in kept or kept[z]["_type"] != "zone":
                not_placed["markers with no zone in the folder"] += 1
            elif whole(e.get("x")) is None or whole(e.get("y")) is None:
                not_placed["markers without integer x and y"] += 1
            else:
                markers_by[m].setdefault(z, []).append(e)
    data_maps = []
    zone_i = 0
    for mid, m in sorted(maps.items(), key=lambda kv: (whole(kv[1].get("hierarchy")) or 0, fold(label(kv[1])))):
        zones = []
        for zid, ms in markers_by[mid].items():
            ms.sort(key=lambda e: (whole(e.get("order")) is None, whole(e.get("order")) or 0, order_made[e["id"]]))
            z = kept[zid]
            zones.append({"i": zone_i, "name": label(z), "shape": shape_of(z), "family": fam_of.get("zone", ""),
                          "pts": [[whole(e["x"]), whole(e["y"])] for e in ms]})
            zone_i += 1
        loc = kept.get(m.get("location"))
        data_maps.append({"id": mid, "name": label(m), "parent": m.get("parent_map") if m.get("parent_map") in maps else None,
                          "image": m.get("image_url") if isinstance(m.get("image_url"), str) and m.get("image_url") else "",
                          "w": whole(m.get("width")), "h": whole(m.get("height")),
                          "loc": label(loc) if loc else "", "desc": m.get("description") or "",
                          "pins": pins_by[mid], "zones": zones, "unplaced": m.get("_unplaced", 0)})

    out = out_folder(folder, a.out)
    head = head_line(folder, world)
    n_pins = sum(len(m["pins"]) for m in data_maps)
    n_zones = sum(len(m["zones"]) for m in data_maps)
    foot = [f"{len(data_maps)} maps, {n_pins} pins and {n_zones} zones placed. Left out: {count_line(left)}.{aids_line(left)} "
            f"Not placed: {count_line(not_placed)}.",
            "Pins and markers are drawn where their x and y say, counted from the map's bottom-left corner. "
            + ("The map images are not loaded (--no-image)." if a.no_image
               else "The map images load from their image_url; the page makes no other outside request."),
            f"Colours: {colour_source}."]
    if skipped:
        foot.append(f"{len(skipped)} files not read: " + "; ".join(skipped[:5]) + (" ..." if len(skipped) > 5 else ""))
    data = {"maps": data_maps, "colors": colors, "families": list(FAMILY_ORDER), "noImage": a.no_image}
    write_page(out / "map.html", f"{name}: maps", head, foot, data, MAP_CSS, MAP_JS)

    print(f"# Maps of {name}\n\n{head}\n")
    for line in foot:
        print(f"- {line}")
    for m in data_maps:
        print(f"- {m['name']}: {len(m['pins'])} pins, {len(m['zones'])} zones"
              + ("" if m["w"] and m["h"] else " (no stated size)"))
    print(f"\nWrote {out / 'map.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
