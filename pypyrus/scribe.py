import cairo
import math

WHITE = (1,1,1,1)
BLACK = (0,0,0,1)

class Renderer(object):
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

    def write_to_png(self, filename):
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

    def background(self, cfill=(1,1,1,1)):
        self.ctx.rectangle(*self.bounds)
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
    
class GeographicRenderer(Renderer):
    def __init__(self, width, height, bounds):
        super(GeographicRenderer, self).__init__(width, height, bounds)
        # flip the axes from upper left, to lower left
        mtrx = cairo.Matrix(1,0,0,-1,bounds[0],bounds[3])
        self.ctx.set_matrix(mtrx)

if __name__ == '__main__':
    r = GeographicRenderer(256,256, (0,0,256,256))
    r.background(cfill=WHITE)
    #r.text((200,200), "cow")
    r.line(coords=(0,0,50,50,50,100))
    r.circle((100,100), 10)
    
    r.write_to_png("moo.png")
            
    

    

