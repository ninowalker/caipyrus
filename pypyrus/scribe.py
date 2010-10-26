import cairo
import math

WHITE = (1,1,1,1)
BLACK = (0,0,0,1)

class Canvas(object):
    def __init__(self, width, height, bounds = None):
        self.s = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        self.w = width
        self.h = height
        if bounds:
            self.bounds = bounds
        else:
            self.bounds = (0, 0, width, height)
        self.ctx = cairo.Context(self.s)
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

    def write_to_png(self, filename):
        #self.ctx.rectangle(*self.bounds)
        #self.ctx.clip_extents(*self.bounds)
        self.s.write_to_png(filename)

    def line(self, coords=None, cstroke=BLACK, stroke=1, cap=cairo.LINE_CAP_ROUND):
        self.ctx.move_to(coords[0], coords[1])
        for i in range(2, len(coords), 2):
            self.ctx.line_to(coords[i], coords[i+1])
        self.ctx.set_source_rgba (*cstroke) # Solid color
        self.ctx.set_line_width(stroke)
        self.ctx.set_line_cap(cap)
        self.ctx.stroke()

    def circle(self, center=None, radius=None, cfill=WHITE, cstroke=BLACK, stroke=1):
        self.ctx.set_line_width(stroke)
        self.ctx.arc(center[0], center[1], radius, 0, 2 * math.pi)
        self.ctx.set_source_rgba(*cstroke)
        self.ctx.stroke()
        self.ctx.set_source_rgba(*cfill)
        self.ctx.fill()

    def background(self, cfill=WHITE):
        self.ctx.rectangle(self.bounds[0], self.bounds[1], self.dx, self.dy)
        #self.ctx.rectangle(*self.bounds)
        self.ctx.set_source_rgba(*cfill)
        self.ctx.fill()

    def rectangle(self, bounds=None, cfill=WHITE, cstroke=BLACK):
        self.ctx.rectangle(*bounds)
        #self.ctx.rectangle(*self.bounds)
        self.ctx.set_source_rgba(*cstroke)
        self.ctx.stroke()
        self.ctx.set_source_rgba(*cfill)
        self.ctx.fill()
        

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
    def __init__(self, width, height, bounds, extent=(-180,-90,180,90)):
        super(GeographicCanvas, self).__init__(width, height, bounds)
        #self.rectangle((0,0,width,height))
        # flip the axes from upper left, to lower left
        fx = 1.0 * self.scale_x
        fy = -1.0 * self.scale_y
        left = 0-extent[0]
        bottom = extent[1]
        mtrx = cairo.Matrix(fx,0,0,fy,left*self.scale_x,height + bottom*self.scale_y)
        #mtrx = cairo.Matrix(fx,0,0,fy,left*(fx),bottom*self.scale_y)
        print mtrx, fx, fy, self.dx, self.dy
        self.ctx.set_matrix(mtrx)
       
        self.ctx.rectangle(*self.bounds)
        self.ctx.clip()



if __name__ == '__main__':
    r = Canvas(256,256)
    r.background(cfill=WHITE)
    r.circle((0,0), 10)
    r.line(coords=(0,0,50,50,50,100))
    r.circle((100,100), 10)
    r.write_to_png("canvas0.png")

    r = GeographicCanvas(256,256, (0,0,256,256), (0,0,256,256))
    r.background(cfill=WHITE)
    r.circle((0,0), 10)
    r.line(coords=(0,0,50,50,50,100))
    r.circle((100,100), 10)
    r.write_to_png("gcanvas0.png")

    r = GeographicCanvas(256,256, (45,45,90,90), extent=(45,45,90,90))
    r.background(cfill=WHITE)
    r.rectangle((45,45,90,90))
    r.circle((0,0), 10)
    r.circle((45,45), 10)
    r.circle((90,90), 10)    
    r.line(coords=(45,45,90,90))
    r.write_to_png("gcanvas1.png")

    

