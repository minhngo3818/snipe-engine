from snipe.utils.decorators import exetime
from num2words import num2words
from spacy.language import Language
from spacy.tokens import Doc
import spacy
import wordsegment as ws
import re

ws.load()  # load wordsegment
nlp = spacy.load("en_core_web_md", disable=["ner"])


@Language.component("punct")
def punct_comp(doc):
    words = [
        token.text for token in doc if re.match(r"\b(?:\d+|[a-zA-Z']+)\b", token.text)
    ]
    return Doc(doc.vocab, words=words)


@Language.component("splitter")
def splitter_comp(doc):
    # Split compound word that sticks like this "SystemsAMBALinksHome"
    words = [
        seg_word
        for token in doc
        if len(token.text) > 0
        for seg_word in ws.segment(token.text)
    ]
    return Doc(doc.vocab, words=words)


@Language.component("num2word")
def num2word_comp(doc):
    # Convert number to words
    result = [
        num_word
        for token in doc
        for num_word in (
            num2words(token.text).split() if token.text.isdigit() else [token.text]
        )
    ]
    return Doc(doc.vocab, words=result)


@Language.component("sepnumword")
def sepnumword_comp(doc):
    # Separate digit and word from a token
    result = []
    for token in doc:
        matches = re.findall(r"\d+|[a-zA-Z]+", token.text)
        if matches:
            result.extend(matches)
        else:
            result.append(token.text)
    return Doc(doc.vocab, words=result)


@Language.component("rm_stopwords")
def rm_stopwords(doc):
    return Doc(doc.vocab, words=[token.text for token in doc if not token.is_stop])


nlp.add_pipe("punct", first=True)
nlp.add_pipe("sepnumword", after="punct")
nlp.add_pipe("num2word", after="sepnumword")
nlp.add_pipe("splitter", after="num2word")
nlp.add_pipe("rm_stopwords", after="splitter")


@exetime
def tokenize_context(text, doc_id, token_map):
    # Split text into chunks to reduce load on spaCy
    chunks = text.split("\n")

    # Track last token index of previous chunk
    prev_end_pos = 0

    for i in range(len(chunks)):
        doc = nlp(chunks[i])
        end_pos = 0

        for token in doc:
            if token.text not in token_map:
                token_map[token.text] = {
                    "id": doc_id,
                    "term_freq": 0,
                    "pos_idx": [],
                }

            if token.i > end_pos:
                end_pos = token.i

            token_map[token.text]["pos_idx"].append(token.i + prev_end_pos)
            token_map[token.text]["term_freq"] += 1

        prev_end_pos = end_pos
