import pickle
import sys
import re
import unicodedata

# never mind sentences with these keywords
bad_words = [
    "license", "copyright",
    "acm", "chi", "publish",
    "proceedings", "redistribute",
    "permission", "redistribute",
    "acknowledgement", "acknowledgements",
    "funded", "eu", "sd", "significant", "pemession",
    "fund", "funds", "nokia", "table", "figure", "p",
    "acknowledgments", "grant", "erc", "strategic",
    "nsf", "foundation", "innovation", "acknowledgment",
    "council", "councils", "grants", "foundations", "finance",
    "financed"
]


def cache_save(key, data):
    with open("pkls/"+key+".pkl", "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


def cache_load(key): 
    with open("pkls/"+key+".pkl", "rb") as f:
        return pickle.load(f)


def log(msg):
    print(msg)
    sys.stdout.flush()


def norm(s):
    s = s.replace("\"","").encode("latin", errors="ignore")
    
    d = {
        'xe2':'',
        'x80':'',
        'x94':''
    }

    pattern = re.compile('|'.join(d.keys()))
    result = pattern.sub(lambda x: d[x.group()], s)

    return result.replace("\\\\\\","").replace("  ", " ")

