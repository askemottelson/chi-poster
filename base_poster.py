import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.font_manager as fm

from config import *

futura = "etc/futura medium condensed bt.ttf"
prop = fm.FontProperties(fname=futura)

futura_thin = "etc/futura light bt.ttf"
thin = fm.FontProperties(fname=futura_thin)

futura_bold = "etc/Futura Bold font.ttf"
fat = fm.FontProperties(fname=futura_bold)

bg_color = (222/255., 214/255., 206/255.)
base_font_color = (223/255., 195/255., 177/255.)
red = (210/255., 61/255., 39/255.)

width = 29.7
height = 42.0

# make base figure in A3
fig = plt.figure(figsize=(width, height))
ax = plt.Axes(fig, [0., 0., width, height])
ax = plt.gca()
ax.set_facecolor(bg_color)
plt.tick_params(axis='both', which='both', bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)

# draw years
years = range(1980,2025,5)
years.reverse()

rect = patches.Rectangle((0,0),1,base_height,linewidth=0,edgecolor=red,facecolor=red)
ax.add_patch(rect)

plt.text(0.01, base_height/3.5, "HUMAN-COMPUTER INTERACTION", fontsize=150, horizontalalignment='left', color=base_font_color, fontproperties=prop)#, bbox=dict(facecolor=red, alpha=1.0, edgecolor=red))

for i, year in enumerate(years):
    y = base_offset + base_height + (i * ((1-base_height/2.)/float(len(years))))
    plt.text(0.01, y, str(year), fontsize=45, horizontalalignment='left', color=red, fontproperties=prop)
    plt.text(0.99, y, str(year), fontsize=45, horizontalalignment='right', color=red, fontproperties=prop)

ax.spines['bottom'].set_color(bg_color)
ax.spines['top'].set_color(bg_color)
ax.spines['right'].set_color(bg_color)
ax.spines['left'].set_color(bg_color)

plt.xlim(0.,1.)
plt.ylim(0.,1.)