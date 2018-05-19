import re
import itertools
import progressbar
from nltk import sent_tokenize
from nltk.tokenize import ToktokTokenizer

getData = re.compile(r'("stars": (\d)).*("title": "(.*?)"),.*("review_date": "(.*?)"),.*("review_text": "(.*?)"),')

good = ["good", "amazing", "awesome", "wonderful", "beautiful", "excellent", "favorable", "great", "marvelous",
        "positive", "super", "worthy", "admirable", "breathtaking", "impressive", "absorbing", "brilliant",
        "charismatic", "charming", "clever", "dazzling", "enjoyable", "entertaining", "exciting", "splendid",
        "legendary",
        "funny", "imaginative", "unpredictable", "surprising", "best"]
bad = ["bad", "awful", "unacceptable", "garbage", "weak", "senseless", "dull", "bland", "boring", "disappointing",
       "disappoint",
       "disgusting", "disappointed", "distasteful", "flawed", "tiresome", "silly", "stupid", "unoriginal",
       "predictable",
       "uninteresting", "uninspired", "third-rate", "horrible", "wacky", "despicable", "petty", "pathetic", "junk",
       "worst",
       "incompetent", "not"]

toktok = ToktokTokenizer()

vowpalFile = open("VowpalReviews.jl", 'a')
widgets = [
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.Percentage(), ') ',
]
linesNumber = sum(1 for line in open('ReviewsFile.jl'))
with open('ReviewsFile.jl', 'r') as f:
    for line in progressbar.progressbar(f, max_value=linesNumber, widgets=widgets):
        m = getData.search(line)
        if m:
            stars = m.group(2)
            date = m.group(6).replace("on ", "").replace(" ", "-").replace(",", "")
            text = m.group(4) + " " + m.group(8)
            text = text.replace(":", "")
            sentences = sent_tokenize(text)
            tokens = [toktok.tokenize(sent) for sent in sentences]
            tokens = list(itertools.chain.from_iterable(tokens))

            sentsCount = 0
            goodWordsCount = 0
            badWordsCount = 0
            for tok in tokens:
                if str(tok).lower() in good:
                    goodWordsCount += 1
                if str(tok).lower() in bad:
                    badWordsCount += 1
            tokensCount = len(tokens) / 100
            textLen = len(text) / 100
            sentsCount = len(sentences) / 100
            goodWordsCount = goodWordsCount / 100
            badWordsCount = badWordsCount / 100
            vowpalFile.write(
                stars + " | " + "length:" + str(textLen) + " goodWords:" + str(goodWordsCount) + " badWords:" +
                str(badWordsCount) + " sentencescount:" + str(sentsCount) + " wordscount:" + str(tokensCount) + " "
                + date + " " + text + "\n")
vowpalFile.close()
