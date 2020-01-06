taken_words = []

def top_np_from_papers(papers):
    res = go_hard(papers)

    highest_grammar_count = (0, None)

    for paper in res.keys():
        grammar = clean_grammar(res[paper])

        for gr in grammar:
            try:
                inter = interactions[gr.lower()]
            except KeyError:
                # -interact,3,3,other,1990
                inter = [gr.lower(), 0, 0, 'select', paper.year]

            if inter[3] not in ['quality', 'style', 'social', 'select'] or gr in excludes or gr.lower() in taken_words:
                continue
            
            c = int(inter[2])
            #print "c?", c, highest_grammar_count
            if c > highest_grammar_count[0]:
                #print "SET HIGHEST", inter
                highest_grammar_count = (c, gr)

    if highest_grammar_count[1]:
        return highest_grammar_count[1].upper()
    else:
        return None


def clean_grammar(grammar):
    wrongs = ["*","[","]","(",")",";",":",",","."]

    clean = []
    for g in grammar:
        if g in excluded_grammar:
            continue

        g = g.replace(" *interaction* ",'')
        g = g.split()

        for cand in g:

            had_wrong = False
            for wrong in wrongs:
                if wrong in cand:
                    had_wrong = True

            if not had_wrong:
                clean.append(cand)

    return list(set(clean))


def scale(val, old_min = 1980., old_max = 2020., new_min = 1.-.03, new_max = base_height + base_offset):
    return ( (val - old_min) / (old_max - old_min) ) * (new_max - new_min) + new_min