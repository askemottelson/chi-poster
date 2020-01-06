import random

from base_poster import *
from config import *
from help import *

from proceedings import get_proceedings, get_citations, get_interactions

citations = get_citations()
interactions = get_interactions()

swap = False

years = range(1980,2025,interval)
years.reverse()

plotted_authors = []

all_papers = get_proceedings(1980,2020)

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
        x = random.uniform(.5, .6)
    else:
        x = random.uniform(.35, .45)
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

    all_author_papers = []
    for p in all_papers:
        for a in p.authors:
            if a.name.lower() == author_name.lower():
                all_author_papers.append(p)

    # the top noun phrases in those selected papers
    all_nps = nps_from_papers(all_author_papers)
    top_np = top_np_from_papers(select_papers)
    if top_np:
        # we print the most ocurring 
        plt.text(x, y+.035, top_np, fontsize=50, horizontalalignment='right', color="black", fontproperties=thin)
        # add it to taken words, so it does not show up again
        taken_words.append(top_np.lower())
        
    # print some debug info    
    print authors[0][0], authors[0][2], ":", y0, "--", y1
    print "***", top_np

    plotted_authors.append((x, y, author_name, [l.lower() for l in all_nps], y1))



years = range(1980,2025,2)
years.reverse()

for year in years:
    y0 = year-interval
    y1 = year-1

    max_style = ('',0,0,'',0)
    max_quality = ('',0,0,'',0)
    max_social = ('',0,0,'',0)

    all_styles = []

    for key in interactions.keys():
        row = interactions[key]
        word, occ, numpaper, cat, first = row[0], int(row[1]), int(row[2]), row[3], int(row[4])

        if cat == 'style':
            if first >= y0 and first < y1:
                if numpaper > max_style[2] and word not in excludes:
                    max_style = (word.upper(), occ, numpaper, cat, first)

                if word not in excludes:
                    all_styles.append(
                        (word.upper(), occ, numpaper, cat, first)
                    )

        elif cat == 'quality':
            if first >= y0 and first < y1:
                if numpaper > max_quality[2] and word not in excludes:
                    max_quality = (word.upper(), occ, numpaper, cat, first)

        elif cat == 'social':
            if first >= y0 and first < y1 and numpaper:
                if numpaper > max_social[2] and word not in excludes:
                    max_social = (word.upper(), occ, numpaper, cat, first)

    x = random.uniform(.68, .75)
    y = scale(max_style[-1])

    if max_style[0] != '':    
        plt.text(x, y, max_style[0], fontsize=30, horizontalalignment='right', color=red, bbox=dict(edgecolor=red, fill=False, linewidth=3), fontproperties=thin)

    # let's references
    #for style in all_styles:
    for pa in plotted_authors:
        year = pa[-1]

        #if year <= y1:

        #print max_style[0].lower(), "?in?", pa[3]
        # overlap
        if max_style[0].lower() in pa[3] and max_style[0] != '':
            print "1draw reference from", max_style[0], "to", pa[2].upper()

            # p1 = (x, y)
            # p2 = (pa[0], pa[1])

            xs = [x+.001, pa[0]]
            ys = [y+.011, pa[1]]
            
            plt.plot(xs, ys, color=red, linewidth=3, alpha=.5)#, zorder=0)


        if max_quality[0].lower() in pa[3] and max_quality[0] != '':
            print "2draw reference from", max_quality[0], "to", pa[2].upper()

            xs = [x_quality+.05, pa[0]-.06]
            ys = [y, pa[1]]
            
            plt.plot(xs, ys, color="black", linewidth=15, alpha=.5)#, zorder=0)

        if max_social[0].lower() in pa[3] and max_social[0] != '':
            print "3draw reference from", max_social[0], "to", pa[2].upper()

            xs = [x_social-.03, pa[0]-.03]
            ys = [y, pa[1]+.02]
            
            plt.plot(xs, ys, color="black", linewidth=30, alpha=.1)#, zorder=0)


    y = scale(max_quality[-1])
    fs = scale(max_quality[2], old_min = 0., old_max = 77., new_min = 35, new_max = 65)
    if max_quality[0] != '':
        plt.text(x_quality, y, max_quality[0], fontsize=fs, horizontalalignment='left', color="black", fontproperties=fat)

    y = scale(max_social[-1])
    fs = scale(max_social[2], old_min = 0., old_max = 170., new_min = 35, new_max = 65)
    if max_social[0] != '':
        plt.text(x_social, y, max_social[0], fontsize=fs, horizontalalignment='right', color="black", fontproperties=fat, alpha=.35)



fig.savefig("poster_out.pdf", bbox_inches='tight', pad_inches=0)    