#!/usr/bin/python3

# http://www.tug.org/TUGboat/Articles/tb27-1/tb86kroonenberg-fonts.pdf

import copy, math
from pyx import *

# Configure the size of the Glow Forge's bed
bedWidth = 11
bedHeight = 19.5
#bedWidth = 7.5
#bedHeight = 10.5

# Configure bottle cap dimensions
# 67mm (2.64in) width, 8.5:19 ratio 0.45
# 60mm (2.37in) width, 8.5:19 ratio 0.45
# 52mm (2.06in) width, 8.5:19 ratio 0.45
# 41mm (1.61in) width, 8.5:19 ratio 0.45
width = 2.64 # inch
ratio = 0.45 # ratio of long to short outer edges
inner = 0.8 # percentage of overall width
edges = 16 # total number of edges; this is a clipped octagon
gap = 0.15 # inch
col = color.cmyk(0, 0, 0, 1)

# Spice labels
labels = [
    2.64,
    "Ground\nCinnamon", "Whole\nCoriander", "Cocoa\nPowder", "Whole\nCumin",
    "Granulated\nOnions", "Oregano", "Smoked\nPaprika", "Cracked\nBlack Pepper",
    "Whole Black\nPeppercorns", "Crushed Chili\nPeppers",
    "Szechuan\nPeppercorns", "Sesame\nSeeds", "", "",
    2.37,
    "Whole\nAllspice", "Ancho Chile\nPowder", "Whole Star\nAnise",
    "Baking\nPowder", "Baking\nSoda", "Whole\nCaraway", "Cayenne\nPepper",
    "Chamomile", "Chipotle", "Cinnamon\nSticks", "Sodium\nCitrate",
    "Pink Curing\nSalt \#1\n{\Large(Prague Powder)}", "Curry\nPowder",
    "Espresso\nPowder", "Fennel\nSeeds", "Garlic\nPowder", "Marjoram",
    "Yellow Mustard\nSeeds", "Sweet\nPaprika", "Whole Green\nPeppercorns",
    "Whole Pink\nPeppercorns", "Ground White\nPepper", "Porcini\nPowder",
    "Golden\nRaisins", "Fried\nShallots", "Sugar \&\nCinnamon",
    "Nutritional\nYeast", "Za\'atar", "", "",
    2.06,
    "Whole Anise\nSeeds", "Ascorbic\nAcid", "Basil", "Basil\nSeeds",
    "Bay\nLeaves", "Decorticated\nCardamon", "Iota\nCarrageenan",
    "Kappa\nCarrageenan", "Lambda\nCarrageenan", "Celery\nSeeds",
    "Citric\nAcid", "Whole\nCloves", "Dill\nSeeds", "Fenugreek",
    "Dried\nGinger", "Herbes\nde Provence", "Irish Moss", "Jalape\\~no\nPowder",
    "Juniper\nBerries", "Lavender", "Lactic\nAcid", "Lemon\nPeel",
    "Locust Bean\nFlour", "Mace", "Nutmeg", "Orange\nPeel", "Parseley",
    "Saffron", "Sage", "Savory", "Seto Fumi\nFurikake", "Spearmint", "Sumak",
    "Cream Of\nTartar", "Tarragon", "Thyme", "Tumeric", "Urfa Biber\nPowder",
    "Vanilla\nBeans", "Xanthan\nGum", "", "", "", "", "", "", "", "", "",
    "", "", "", "",
    1.61,
    "Sodium\nCarbonate", "Potassium\nSorbate",
    "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "",
    "", "", "", "", "", "", "", "",
]

# Set up TeX runtime environment
unit.set(defaultunit="inch")
text.set(text.LatexRunner)
text.preamble(r"""\usepackage{color}
                  \definecolor{COL}{cmyk}{%g,%g,%g,%g}
                  \newcommand{\kalam}{\fontfamily{kalam}\selectfont}""" % (
                  col.c, col.m, col.y, col.k))

# Set up page dimensions
glowforge = document.paperformat(bedWidth*unit.t_inch, bedHeight*unit.t_inch)
clip = canvas.clip(path.rect(0, 0, bedWidth, bedHeight))
c = canvas.canvas(attrs = [clip], ipython_bboxenlarge = gap/2 * unit.t_inch)
pageno = 0

# Print the current page and get ready for the next one
def flushPage():
    global c, pageno
    page = document.page(c, paperformat = glowforge, margin = 0.4 * unit.t_inch,
                         bboxenlarge = 1 * unit.t_pt)
    document.document([page]).writeSVGfile(r"spicerack%d.svg" % pageno)
    pageno += 1
    c = canvas.canvas(attrs = [clip], ipython_bboxenlarge = gap/2 * unit.t_inch)

# Draw the shape of the bottle cap
nx = math.ceil(math.sqrt(len([i for i in labels if type(i) is str])))
ex, ey = 0, 0
sx, sy = gap/2, gap/2
for label in labels:
    if type(label) is not str:
        # Compute the scale factor needed to bring the drawing to the
        # desired "width"
        sy += width - label
        width = label
        scale = 0
        i = 0
        while i < edges / 2:
            m = ratio if i & 1 else 1
            scale += m * math.sin(math.radians(360*i/edges))
            i = i + 1
        scale = width / scale
        continue
    # Advance to the next line, if the current one is full
    if sx + width + gap/2 >= clip.path.bbox().width():
        ex, ey = 0, ey + 1
        sx, sy = gap/2, sy + width + gap
    # Advance to the next page, if the current one is full
    if sy + width + gap/2 >= clip.path.bbox().height():
        flushPage()
        ex, ey = 0, 0
        sx, sy = gap/2, gap/2
    # Center the label both horizontally and vertically; honor new lines
    c.text(width/2 + sx, width/2 + sy,
           r"\textcolor{COL}{"
           r"\kalam\huge\vbox{\hbox to 0pt{\hss " +
           r"\hss}\hbox to 0pt{\hss ".join(label.split('\n')) +
           r"\hss}}}",
           [text.halign.boxcenter, text.halign.flushcenter,
            text.valign.middle])
    # Compute the outline of the bottle cap
    x, y = (width - scale) / 2 + sx, sy
    i = 0
    p = path.path(path.moveto(x, y))
    while i < edges:
        m = ratio if i & 1 else 1
        ox, oy = x, y
        x += m * scale * math.cos(math.radians(360*i/edges))
        y += m * scale * math.sin(math.radians(360*i/edges))
        p.append(path.lineto(x, y))
        i += 1
    # Draw the cuts in red
    c.stroke(p, [color.rgb.red])
    # Draw the decorative frame in a different color
    p = copy.deepcopy(p)
    p.append(path.arc(width/2 + sx, width/2 + sy, width*inner/2, -90, 270))
    c.fill(p, [style.fillrule.even_odd, col])
    # Advance to the next position in the SVG file
    ex = (ex + 1) % nx
    sx += gap + width
    if ex == 0:
        ey += 1
        sx, sy = gap/2, sy + gap + width

flushPage()
