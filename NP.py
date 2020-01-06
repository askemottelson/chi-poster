import nltk
from proceedings import get_proceedings

# Noun phrase patterns
jk_patterns = """
    CONJ: {<TO|CC>*}
    PRE: {<CONJ>?<JJ.*>+}
        {<CONJ>?<NN.*>+}
    NP: {<PRE>*<ZZ>+<VB.*>*<PRE>*}
    """

# List of keywords of interest
interactions = ["interaction", "interactions", "interactional"]

# Noun Phrase Chunker
NPChunker = nltk.RegexpParser(jk_patterns)


def assign_NP_sentence(tagged_sentence):
    nps = []
    tree = NPChunker.parse(tagged_sentence)

    for subtree in tree.subtrees():

        # If the subtree is our desired noun phrase
        if subtree.label() == 'NP':
            # Grab noun phrase from leaves, keeping correct instance of
            # 'interaction' highlighted
            nps.append(" ".join([word for word, tag in subtree.leaves()]))

    return nps


def parse_sentence(sentence):
    # Tag each word with grammar label
    sentence_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
    words = [w[0] for w in sentence_tagged]

    # Loop through the labelled words
    for idx, sent in enumerate(sentence_tagged):

        if sent[0] in interactions:

            # Replace interaction word with *interaction* and update grammar
            # tag to ZZ
            temp = list(sentence_tagged[idx])
            temp[1] = 'ZZ'
            temp[0] = "*interaction*"
            sentence_tagged[idx] = tuple(temp)

    # Check sentence grammar against noun phrase pattern
    return assign_NP_sentence(sentence_tagged)


def go_hard(papers=None):
    if papers == None:
        papers = get_proceedings()
    res = {}
    for paper in papers:
        res[paper] = []
        sentences = nltk.sent_tokenize(paper.clean_text)
        for i, sentence in enumerate(sentences):
            grammar_sentences = parse_sentence(sentence)
            res[paper] = res[paper] + grammar_sentences

    return res
