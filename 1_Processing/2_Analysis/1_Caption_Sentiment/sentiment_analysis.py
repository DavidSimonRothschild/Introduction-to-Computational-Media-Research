import string
from nltk.tokenize.treebank import TreebankWordTokenizer
from pathlib import Path

# Sentiment analysis script for German, rule-based.
# adapted to run in restricted env (no pickle download)

datafolder = Path("data/")


# ------------- helpers ------------- #

# very simple sentence splitter (no pickle, no download)
def simple_sentence_tokenize(text: str):
    parts = []
    current = []
    for ch in text:
        current.append(ch)
        if ch in ".!?":
            parts.append("".join(current).strip())
            current = []
    if current:
        parts.append("".join(current).strip())
    return [p for p in parts if p]


word_tokenizer = TreebankWordTokenizer()


def treebank_tokenizer(sentence: str):
    tokens = []
    for s in simple_sentence_tokenize(sentence):
        tokens.extend(word_tokenizer.tokenize(s))
    # strip punctuation + lowercase
    tokens = [
        "".join(ch for ch in tok if ch not in string.punctuation).lower()
        for tok in tokens
    ]
    return [t for t in tokens if t]


def stopword_filter(tokens):
    file_to_open = datafolder / "stopWords.txt"
    with open(file_to_open, "r", encoding="utf-8") as f:
        stopwords = [line.strip().lower() for line in f if line.strip()]
    # keep only tokens that are NOT stopwords
    return [t for t in tokens if t not in stopwords]


def negation_words():
    negdict = datafolder / "negationswoerter.txt"
    with open(negdict, "r", encoding="utf-8") as negwords:
        return [line.strip().lower() for line in negwords if line.strip()]


# ------------- core logic ------------- #

def analyze(query: str, dict_filename: str) -> float:
    tokens = treebank_tokenizer(query)
    tokens = stopword_filter(tokens)
    negs = set(negation_words())
    dict_path = datafolder / dict_filename

    sentiment_value = 0.0

    with open(dict_path, "r", encoding="utf-8") as sentis:
        for s in sentis:
            # SentiWS format: lemma|lemma2<TAB>score<TAB>inflections
            cells = s.split("\t")
            lemma_parts = cells[0].lower().split("|")
            value = float(cells[1].strip())
            if len(cells) > 2:
                infl = [w.strip().lower() for w in cells[2].split(",") if w.strip()]
            else:
                infl = []

            # set for faster lookup
            all_forms = set(lemma_parts) | set(infl)

            # go through tokens in the sentence
            for idx, tok in enumerate(tokens):
                if tok in all_forms:
                    # check prev/next for negation but carefully
                    neg_factor = 1.0
                    if idx > 0 and tokens[idx - 1] in negs:
                        neg_factor = -0.5
                    elif idx < len(tokens) - 1 and tokens[idx + 1] in negs:
                        neg_factor = -0.5
                    sentiment_value += value * neg_factor

    return sentiment_value


def positive_sentiment(query: str) -> float:
    return analyze(query, "SentiWS_v2.0_Positive.txt")


def negative_sentiment(query: str) -> float:
    return analyze(query, "SentiWS_v2.0_Negative.txt")


def main(query: str):
    # SentiWS positive are >0, negative are <0, so we can just sum
    value = round(positive_sentiment(query) + negative_sentiment(query), 2)
    # clamp to [-1, 1]
    value = max(min(value, 1.0), -1.0)
    return {"sentiment": value}


if __name__ == "__main__":
    print("Use test or call main(<query>)")
    testQuery = "Die E-ID ist der untergang der schweizer selbstbestimmung und schliesst alte menschen aus."
    print(main(testQuery))
