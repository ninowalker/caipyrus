import cairo
import math

WHITE = (1,1,1,1)
BLACK = (0,0,0,1)
TRANSPARENT = (0,0,0,0)

class Canvas(object):
    def __init__(self, width, height, bounds = None, mode = 'png', fobj=None):
        if mode == 'png':
            self.s = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        elif mode == 'svg':
            self.s = cairo.SVGSurface(fobj, width, height)
        self.w = width
        self.h = height
        if bounds:
            self.bounds = bounds
        else:
            self.bounds = (0, 0, width, height)
        self.ctx = cairo.Context(self.s)
        self.scale_strokes(False)
        #self.set_font_face()
        #self.ctx.scale(width, height)

    @property
    def dx(self):
        return self.bounds[2] - self.bounds[0]

    @property
    def dy(self):
        return self.bounds[3] - self.bounds[1]

    @property
    def scale_x(self):
        return float(self.w) / self.dx

    @property
    def scale_y(self):
        return float(self.h) / self.dy

    def scale_strokes(self, yn=True):
        if yn:
            self._stroke_scalar = 1.0 / ( (self.scale_x + self.scale_y) / 2.0 )
        else:
            self._stroke_scalar = 1.0
        

    def write_to_png(self, filename):
        #self.ctx.rectangle(*self.bounds)
        #self.ctx.clip_extents(*self.bounds)
        self.s.write_to_png(filename)

    def write(self):
        self.s.flush()
        self.s.finish()

    def _draw(self, cstroke=None, stroke=None, cfill=None, cap=None):
        if cfill:
            self.ctx.set_source_rgba(*cfill)
            self.ctx.fill_preserve()
        if cap:
            self.ctx.set_line_cap(cap)
        if stroke:
            self.ctx.set_line_width(stroke*self._stroke_scalar)
            self.ctx.set_source_rgba(*cstroke)
            self.ctx.stroke()
        

    def line(self, coords=None, cstroke=BLACK, stroke=1, cap=cairo.LINE_CAP_ROUND):
        self.ctx.move_to(coords[0], coords[1])
        for i in range(2, len(coords), 2):
            self.ctx.line_to(coords[i], coords[i+1])

        self._draw(cstroke=cstroke, stroke=stroke, cap=cap)

    def circle(self, center=None, radius=None, cfill=WHITE, cstroke=BLACK, stroke=1):
        self.ctx.arc(center[0], center[1], radius, 0, 2 * math.pi)
        self._draw(cstroke=cstroke, stroke=stroke, cfill=cfill)

    def background(self, cfill=WHITE):
        self.ctx.rectangle(self.bounds[0], self.bounds[1], self.dx, self.dy)
        #self.ctx.rectangle(*self.bounds)
        self._draw(cfill=cfill)

    def rectangle(self, bounds=None, cfill=TRANSPARENT, cstroke=BLACK, stroke=1):
        self.ctx.rectangle(bounds[0], bounds[1], bounds[2] - bounds[0], bounds[3] - bounds[1])
        self._draw(cstroke=cstroke, stroke=stroke, cfill=cfill)

    def text(self, point=None, text=None, font_size=1, cfill=BLACK):
        self.ctx.select_font_face("Georgia",
                                  cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)

        self.ctx.set_font_size(1.2)
        self.ctx.move_to(*point)
        self.ctx.set_source_rgba(*cfill)
        self.ctx.show_text(text)

    def set_font_face(self, family="serif", slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL):
        self.ctx.select_font_face(family, slant, weight)
        #self.ctx.set_font_face(ff)
    
class GeographicCanvas(Canvas):
    def __init__(self, width, height, bounds, **kwargs):
        super(GeographicCanvas, self).__init__(width, height, bounds, **kwargs)
        self.scale_strokes(True)
        # flip the axes from upper left, to lower left, and shift the origin
        fx = 1.0 * self.scale_x
        fy = -1.0 * self.scale_y
        left = 0-bounds[0] 
        bottom = bounds[1]
        mtrx = cairo.Matrix(fx,0,0,fy,
                            left*self.scale_x,
                            height + bottom*self.scale_y)
        #print mtrx
        self.ctx.set_matrix(mtrx)
        self.ctx.rectangle(self.bounds[0],self.bounds[1],self.dx,self.dy)
        self.ctx.clip()



if __name__ == '__main__':
    r = Canvas(256,256)
    r.background(cfill=WHITE)
    r.circle((0,0), 10)
    r.line(coords=(0,0,50,50,50,100))
    r.circle((100,100), 10)
    r.write_to_png("canvas0.png")

    r = GeographicCanvas(256,256, (0,0,256,256))
    r.background(cfill=WHITE)
    r.circle((0,0), 10)
    r.line(coords=(0,0,50,50,50,100))
    r.circle((100,100), 10)
    r.rectangle((50,50,200,200))
    r.write_to_png("gcanvas0.png")

    r = GeographicCanvas(256,256, (45,45,90,90))
    r.background(cfill=WHITE)
    r.circle((0,0), 10)
    r.circle((45,45), 10)
    r.circle((90,90), 10)    
    r.line(coords=(45,45,90,90))
    r.rectangle((45,45,50,50), cfill=(1,0,0,1))
    r.scale_strokes(False)
    r.rectangle((45,45,90,90))
    r.write_to_png("gcanvas1.png")

    r = GeographicCanvas(256*2,256, (45,45,90,90))
    r.background(cfill=WHITE)
    r.circle((0,0), 10)
    r.circle((45,45), 10)
    r.circle((90,90), 10)    
    r.line(coords=(45,45,90,90))
    r.rectangle((45,45,50,50), cfill=(1,0,0,1))
    r.scale_strokes(False)
    r.rectangle((45,45,90,90))
    r.write_to_png("gcanvas2.png")

    r = GeographicCanvas(256*2,256, (-180,-90,180,90))
    r.background(cfill=WHITE)
    r.circle((0,0), 10)
    r.circle((45,45), 10)
    r.circle((90,90), 10)    
    r.line(coords=(45,45,90,90))
    r.rectangle((45,45,50,50), cfill=(1,0,0,1))
    r.scale_strokes(False)
    r.rectangle((45,45,90,90))
    r.write_to_png("gcanvas3.png")
    

