from caipyrus import *
from graphserver.ext.osm.osmdb import OSMDB
import sys

def flatten(l, ltypes=(list, tuple)):
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)


if __name__ == '__main__':

    COLORS = {
        'motorway': ((1,0,0,1), 2),
        'motorway_link': ((1,0,0,1), 1.5),
        }
    
    out, filename, w, h = sys.argv[1:]
    db = OSMDB(filename)
    b = db.bounds()
    r = GeographicCanvas(int(w), int(h), b, mode='svg', fobj=open(out,'wb'))
    r.background()
    for way_id, parent_id, from_nd, to_nd, dist, geom, tags in db.edges():
        color, stroke = COLORS.get(tags.get('highway'),((0,0,0,.8),0.8))
        r.line(coords=flatten(geom), cstroke=color, stroke=stroke)

    #r.write_to_png(out)
