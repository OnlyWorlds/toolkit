"""Draw a world folder's maps, with their pins and zones: map.html.

Reads a world folder with graph.py's reader and writes one page into the output folder, never
into the world. A Map element is a canvas when it has a size: its image_url, width x height
pixels. A Pin sits at its integer x, y counted from the map's BOTTOM-LEFT corner (the page flips
y) and names the element it places (element_type + element_id); its label is that element's
name. A Zone is its Markers on that map, in `order` ascending (a marker without a whole-number order comes after
every ordered one; ties go by id), joined by the zone's `shape` as written: `line` is an open
path, any other value or none a closed polygon. These are the map-space profile's rules (§2,
§4: profiles/map-space.md in github.com/OnlyWorlds/schema-dist). Maps nest by parent_map; the
page lists them as a tree and shows one at a time.

Nothing is placed by guess: a pin or marker without integer x and y, or on a map the folder
lacks, is counted as not placed. A map missing its width or height takes the missing one from
its placed points (the largest x or y among its pins and its zones' markers), and the page says
the size was measured. A map has a canvas when its width and height, stated or measured, are both
greater than 0; that is decided once per map (placement()) and every sentence about placement,
in the summary and on the page, reads it. A map with no canvas and an image (and no --no-image)
takes both its width and its height from the image if it loads, and the summary counts its points
in neither total but on a line of their own; with no image, or with --no-image, its pins and
zones are counted as not placed, on a map with no size. Room, proposed and hidden
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
                   left_out_reason, listed_hidden, open_folder, out_folder, presentation, stand_ins,
                   unread_page_line, unread_terminal_lines, write_page)


def whole(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return None


def id_in(v):
    """A link field's id as a key: a string, else None (a list, an object or a number names no
    element, as a missing one does)."""
    return v if isinstance(v, str) else None


def shape_of(z):
    """The Zone's own `shape`, read as written: `line` is an open path, anything else a polygon."""
    return "line" if z.get("shape") == "line" else "polygon"


def older_line_mark(z):
    """A Zone with no `shape` that carries a line mark in an older key (`atlas_shape` or a
    supertype `line`): drawn closed by shape_of, and named in the summary (older-shape-keys)."""
    s = z.get("shape")
    if s is not None and not (isinstance(s, str) and not s.strip()):
        return False
    a = z.get("atlas_shape")
    return (isinstance(a, str) and a.strip().lower() == "line") or fold(z.get("supertype")) == "line"


def frame(m, points):
    """The Map's width and height, and which were measured ("", "width", "height" or "size" for
    both): a missing slot is the largest x (or y) among the points placed on that Map, its Pins
    and its zones' Markers."""
    w, h = whole(m.get("width")), whole(m.get("height"))
    mw, mh = bool(points) and w is None, bool(points) and h is None
    if mw:
        w = max(p[0] for p in points)
    if mh:
        h = max(p[1] for p in points)
    return w, h, "size" if mw and mh else "width" if mw else "height" if mh else ""


def placement(w, h, image, no_image):
    """Where a Map's points stand, decided once here and carried in the page's data. `canvas`:
    both slots are greater than 0, so its points are placed. With no canvas: `image`, the page takes
    the size from the map's image if it loads; `unloaded`, it has an image but --no-image keeps it
    out; `none`, no image to take a size from. The page adds `failed` when the image does not load
    or gives no size."""
    if (w or 0) > 0 and (h or 0) > 0:
        return "canvas"
    if image:
        return "unloaded" if no_image else "image"
    return "none"


def size_words(w, h, measured, place):
    """A Map's size in words, their one home: the summary's per-map line and the page's panel both
    show this. A canvas: which slots were measured from its points (frame's `measured`), or nothing
    when both are stated; the page adds no words about how a size was found but "(from its image)",
    which only the browser can know. No canvas: "no stated size" only when it states neither slot
    and has no placed point to measure one from; otherwise "no size" and each slot as stated,
    measured or missing."""
    if place == "canvas":
        return f"{measured} measured from its points" if measured else ""
    if w is None and h is None:
        return "no stated size"
    slots = []
    for slot, v in (("width", w), ("height", h)):
        slots.append(f"no {slot}" if v is None else f"{slot} {v}" + (" measured" if measured in (slot, "size") else ""))
    return "no size: " + ", ".join(slots)


# The page's note for a map with no canvas, by its `place` (placement(); `failed` is set by the page
# when the image does not load or gives no size). They ride in the page's data, as each map's size
# words do (size_words()): the page's script writes no note of its own, and no words about how a
# size was found but "(from its image)". Its count line ("N pins, M zones placed") is built in the
# script and reads `place`.
NOTES = {"image": "Its image is loading: its pins and zones are placed if it loads and gives a size.",
         "unloaded": "The map images are not loaded (--no-image), so its image cannot give a size: "
                     "its pins and zones are not placed.",
         "none": "It has no image to take a size from: its pins and zones are not placed.",
         "failed": "Its image did not load or gave no size: its pins and zones are not placed."}


def n(k, word):
    """A count and its noun, agreeing: 1 pin, 2 pins."""
    return f"{k} {word}" + ("" if k == 1 else "s")


def outline(elements, kept_ids):
    """The parent_location tree as Markdown, for a world with no map."""
    locs = {i: e for i, e in elements.items() if e["_type"] == "location" and i in kept_ids}
    kids = {}
    for i, e in locs.items():
        p = id_in(e.get("parent_location"))
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
function draw(m){cur=m;svg.textContent='';
 if(m.place!=='canvas'){if(m.place==='image'&&!m.tried){m.tried=1;const im=new Image();
   im.onload=()=>{if(im.naturalWidth>0&&im.naturalHeight>0){m.w=im.naturalWidth;m.h=im.naturalHeight;m.sized=1;m.place='canvas'}else m.place='failed';if(cur===m)draw(m)};
   im.onerror=()=>{m.place='failed';if(cur===m)draw(m)};im.src=m.image}
  panel(m,D.notes[m.place]);return}
 const w=m.w,hh=m.h,vp=el('g',{},svg);el('rect',{x:0,y:0,width:w,height:hh,fill:dark?'#20201e':'#efefea',stroke:dark?'#55554f':'#c4c4bd'},vp);
 if(m.image&&!D.noImage)el('image',{href:m.image,x:0,y:0,width:w,height:hh,preserveAspectRatio:'none'},vp);
 const u=Math.max(w,hh)/250;
 for(const z of m.zones){const pts=z.pts.map(p=>p[0]+','+(hh-p[1])).join(' ');const c=col(z.family);
  const s=el(z.shape==='line'?'polyline':'polygon',{points:pts,fill:z.shape==='line'?'none':c,'fill-opacity':.18,stroke:c,'stroke-width':u*.8,'stroke-linejoin':'round'},vp);
  h('title',z.name+' ('+z.shape+', '+z.pts.length+' markers)',s);s.dataset.z=z.i}
 for(const p of m.pins){const g=el('g',{},vp),y=hh-p.y;el('circle',{cx:p.x,cy:y,r:u*1.8,fill:col(p.family),stroke:dark?'#121211':'#fff','stroke-width':u*.5},g);
  const t=el('text',{x:p.x+u*2.6,y:y+u*1.2,'font-size':u*4.2,fill:dark?'#fff':'#111',stroke:dark?'#000':'#fff','stroke-width':u*.9,'paint-order':'stroke'},g);t.textContent=p.label;
  h('title',p.label+(p.type?' ('+p.type+')':'')+' at '+p.x+', '+p.y,g)}
 fitTo(-w*.03,-hh*.03,w*1.03,hh*1.03);panel(m,null)}
function panel(m,note){side.textContent='';h('h2',m.name,side);const on=m.place==='canvas';
 h('div',(on?m.w+' × '+m.h+' px'+(m.sized?' (from its image)':m.size?' ('+m.size+')':''):m.size)+(m.loc?' · '+m.loc:''),side,'k');
 if(note)h('p',note,side);if(m.desc)h('p',m.desc,side);
 h('p',m.pins.length+' pins, '+m.zones.length+' zones '+(on?'placed'+(m.unplaced?'; '+m.unplaced+' not placed':''):'not placed'+(m.unplaced?', and '+m.unplaced+' more without integer x and y':'')),side,'k');
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
    listed = listed_hidden(world)
    elements = stand_ins(elements, skipped, a.room, a.proposed, a.hidden, listed)
    left = {"reading aid": 0, "room": 0, "proposed": 0, "hidden": 0, "outside the 22 types": 0}
    kept = {}
    for i, e in elements.items():
        why = left_out_reason(e, a.room, a.proposed, a.hidden, listed)
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

    fam_of, colors, colour_source, colour_said = presentation(a.offline, a.presentation)
    # "Drawn here": true whether the map or zone is absent from the folder or left out by this run,
    # and it names neither.
    not_placed = {"pins without integer x and y": 0, "pins on no map drawn here": 0,
                  "pins placing a left-out element": 0, "markers without integer x and y": 0,
                  "markers on no map drawn here": 0, "markers with no zone drawn here": 0}
    pins_by, markers_by = {m: [] for m in maps}, {m: {} for m in maps}
    for e in kept.values():
        if e["_type"] == "pin":
            m = id_in(e.get("map"))
            if m not in maps:
                not_placed["pins on no map drawn here"] += 1
                continue
            x, y = whole(e.get("x")), whole(e.get("y"))
            if x is None or y is None:
                not_placed["pins without integer x and y"] += 1
                maps[m].setdefault("_unplaced", 0)
                maps[m]["_unplaced"] += 1
                continue
            target = elements.get(id_in(e.get("element_id")))
            if target is not None and target["id"] not in kept:
                not_placed["pins placing a left-out element"] += 1
                continue
            t = target["_type"] if target else str(e.get("element_type") or "").lower()
            pins_by[m].append({"x": x, "y": y, "label": label(target) if target else label(e),
                               "type": t, "family": fam_of.get(t, "")})
        elif e["_type"] == "marker":
            m, z = id_in(e.get("map")), id_in(e.get("zone"))
            if m not in maps:
                not_placed["markers on no map drawn here"] += 1
            elif z not in kept or kept[z]["_type"] != "zone":
                not_placed["markers with no zone drawn here"] += 1
            elif whole(e.get("x")) is None or whole(e.get("y")) is None:
                not_placed["markers without integer x and y"] += 1
            else:
                markers_by[m].setdefault(z, []).append(e)
    data_maps = []
    zone_i = 0
    older = {}
    for mid, m in sorted(maps.items(), key=lambda kv: (whole(kv[1].get("hierarchy")) or 0, fold(label(kv[1])))):
        zones = []
        for zid, ms in markers_by[mid].items():
            ms.sort(key=lambda e: (whole(e.get("order")) is None, whole(e.get("order")) or 0, e["id"]))
            z = kept[zid]
            if older_line_mark(z):
                older[zid] = label(z)
            zones.append({"i": zone_i, "name": label(z), "shape": shape_of(z), "family": fam_of.get("zone", ""),
                          "pts": [[whole(e["x"]), whole(e["y"])] for e in ms]})
            zone_i += 1
        loc = kept.get(id_in(m.get("location")))
        parent = id_in(m.get("parent_map"))
        w, h, measured = frame(m, [(p["x"], p["y"]) for p in pins_by[mid]]
                               + [tuple(p) for z in zones for p in z["pts"]])
        image = m.get("image_url") if isinstance(m.get("image_url"), str) and m.get("image_url") else ""
        place = placement(w, h, image, a.no_image)
        data_maps.append({"id": mid, "name": label(m), "parent": parent if parent in maps else None,
                          "image": image, "w": w, "h": h, "measured": measured, "place": place,
                          "size": size_words(w, h, measured, place),
                          "loc": label(loc) if loc else "", "desc": m.get("description") or "",
                          "pins": pins_by[mid], "zones": zones, "unplaced": m.get("_unplaced", 0)})

    out = out_folder(folder, a.out)
    head = head_line(folder, world)
    # Every sentence about placement reads the map's `place` (placement()), never a test of its own:
    # the totals count the canvas maps; a map whose image may still give a size is in neither total
    # and has its own line; a map that cannot be placed counts its points under "Not placed".
    canvas = [m for m in data_maps if m["place"] == "canvas"]
    group = {p: [m for m in data_maps if m["place"] == p and (m["pins"] or m["zones"])]
             for p in ("image", "unloaded", "none")}
    n_pins = sum(len(m["pins"]) for m in canvas)
    n_zones = sum(len(m["zones"]) for m in canvas)
    # A kind's points on one map read "on a map with no size", on more than one "on maps with no size".
    lost = [m for p in ("unloaded", "none") for m in group[p]]
    no_size = [n(sum(len(m[key]) for m in on), kind) + (" on a map" if len(on) == 1 else " on maps") + " with no size"
               for kind, key in (("pin", "pins"), ("zone", "zones")) for on in [[m for m in lost if m[key]]] if on]
    older_kinds = count_line(not_placed)
    foot = [f"{len(data_maps)} maps, {n_pins} pins and {n_zones} zones placed. Left out: {count_line(left)}.{aids_line(left)} "
            f"Not placed: {', '.join(([] if older_kinds == 'nothing' else [older_kinds]) + no_size) or 'nothing'}.",
            "Pins and markers are drawn where their x and y say, counted from the map's bottom-left corner. "
            + ("The map images are not loaded (--no-image)." if a.no_image
               else "The map images load from their image_url; the page makes no other outside request."),
            "Colours: {}."]
    for p, ms in group.items():
        if not ms:
            continue
        np_, nz = sum(len(m["pins"]) for m in ms), sum(len(m["zones"]) for m in ms)
        one, single = np_ + nz == 1, len(ms) == 1
        names = sorted((m["name"] for m in ms), key=fold)
        head_ = (" and ".join(x for x in (np_ and n(np_, "pin"), nz and n(nz, "zone")) if x)
                 + (" sits on a map" if one else " sit on a map" if single else " sit on maps")
                 + f" with no size ({', '.join(names[:5])}{' and more' if len(names) > 5 else ''})")
        foot.append(head_ + {
            "image": f": the page places {'it' if one else 'them'} if "
                     + ("the map's image loads and gives a size." if single
                        else "each map's image loads and gives a size."),
            "unloaded": f" and {'is' if one else 'are'} not placed: the map images are not loaded (--no-image), so "
                        + ("its image cannot give a size." if single else "their images cannot give a size."),
            "none": f" and {'is' if one else 'are'} not placed: "
                    + ("the map has no image to take a size from." if single
                       else "the maps have no image to take a size from."),
        }[p])
    if older:
        names = sorted(older.values(), key=fold)
        foot.append(f"{len(older)} {'zone carries' if len(older) == 1 else 'zones carry'} a line mark in an older key (atlas_shape or a supertype "
                    f"line) and no shape, so {'it is' if len(older) == 1 else 'they are'} drawn closed: {', '.join(names[:5])}"
                    + (" ..." if len(names) > 5 else "") + ". Set shape to line on each to draw an open path.")
    data = {"maps": data_maps, "colors": colors, "families": list(FAMILY_ORDER), "noImage": a.no_image,
            "notes": NOTES}
    # The colour line, third in the foot, names a --presentation file on the page by its name alone
    # and in the terminal by its path as typed (graph.presentation).
    page_foot = foot[:2] + [foot[2].format(colour_source)] + foot[3:]
    write_page(out / "map.html", f"{name}: maps", head,
               page_foot + ([unread_page_line(skipped)] if skipped else []), data, MAP_CSS, MAP_JS)

    foot[2] = foot[2].format(colour_said)
    print(f"# Maps of {name}\n\n{head}\n")
    for line in foot:
        print(f"- {line}")
    if skipped:
        print("\n".join(unread_terminal_lines(skipped)))
    for m in data_maps:
        print(f"- {m['name']}: {len(m['pins'])} pins, {len(m['zones'])} zones"
              + (f" ({m['size']})" if m["size"] else "")
              + ("" if m["place"] == "canvas" or not (m["pins"] or m["zones"])
                 else ", placed if its image loads and gives a size" if m["place"] == "image"
                 else ", not placed"))
    print(f"\nWrote {out / 'map.html'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
