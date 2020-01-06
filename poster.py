import random

from base_poster import *
from config import *
from help import *

from proceedings import get_proceedings, get_citations, get_interactions
from NP import go_hard

citations = get_citations()
interactions = get_interactions()

swap = False

years = range(1980,2025,interval)
years.reverse()

for year in years:

    y0 = year-interval
    y1 = year-1
    papers = get_proceedings(y0, y1)

    if len(papers) == 0:
        continue

    out = []
    for paper in papers:
        paper.citations = citations[paper.DOI.lower()]
        out.append(
           paper
        )
    out.sort(key=lambda x: x.citations, reverse=True)
    out = out[0:2]

    authors = []
    for o in out:
        authors.extend([
            (a.name, a.affiliation, o.year) for a in o.authors
        ])
    
    # we use this to push authors back and forth, to avoid overlaps
    if swap:
        x = random.uniform(.5, .65)
    else:
        x = random.uniform(.39, .4)
    swap = not swap

    author_name = authors[0][0]
    y = scale(authors[0][2]) - 3*base_offset
    t = author_name + "\nd. " + str(authors[0][2]) # most cited author and year

    # print author info
    plt.text(x, y, t, fontsize=35, horizontalalignment='right', color="black", fontproperties=prop)
    
    # pick all papers from most cited author
    select_papers = []
    for p in papers:
        for a in p.authors:
            if a.name.lower() == author_name.lower():
                select_papers.append(p)

    # the top noun phrases in those selected papers
    top_np = top_np_from_papers(select_papers)
    if top_np:
        # we print the most ocurring 
        plt.text(x, y+.035, top_np, fontsize=50, horizontalalignment='right', color="black", fontproperties=thin)
        # add it to taken words, so it does not show up again
        taken_words.append(top_np.lower())
        
    # print some debug info    
    print authors[0][0], authors[0][2], ":", y0, "--", y1, "--->", y
    print "***", top_np


for year in years:
    y0 = year-interval
    y1 = year-1

    max_style = ('',0,0,'',0)
    max_quality = ('',0,0,'',0)
    max_social = ('',0,0,'',0)

    for key in interactions.keys():
        row = interactions[key]
        word, occ, numpaper, cat, first = row[0], int(row[1]), int(row[2]), row[3], int(row[4])

        if cat == 'style':
            if first >= y0 and first < y1:
                if numpaper > max_style[2] and word not in excludes:
                    max_style = (word.upper(), occ, numpaper, cat, first)

        elif cat == 'quality':
            if first >= y0 and first < y1:
                if numpaper > max_quality[2] and word not in excludes:
                    max_quality = (word.upper(), occ, numpaper, cat, first)

        elif cat == 'social':
            if first >= y0 and first < y1 and numpaper:
                if numpaper > max_social[2] and word not in excludes:
                    max_social = (word.upper(), occ, numpaper, cat, first)

    if max_style[0] == '':
        continue

    x = random.uniform(.65, .77)
    y = scale(max_style[-1])
    plt.text(x, y, max_style[0], fontsize=30, horizontalalignment='right', color=red, bbox=dict(edgecolor=red, fill=False, linewidth=3), fontproperties=thin)

    y = scale(max_quality[-1])
    fs = scale(max_quality[2], old_min = 0., old_max = 77., new_min = 35, new_max = 65)
    plt.text(x_quality, y, max_quality[0], fontsize=fs, horizontalalignment='left', color="black", fontproperties=fat)

    y = scale(max_social[-1])
    fs = scale(max_social[2], old_min = 0., old_max = 170., new_min = 35, new_max = 65)
    plt.text(x_social, y, max_social[0], fontsize=fs, horizontalalignment='right', color="black", fontproperties=fat, alpha=.35)    



fig.savefig("poster_out.pdf", bbox_inches='tight', pad_inches=0)    