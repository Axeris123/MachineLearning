import re

import spacy

getData = re.compile(r'("stars": (\d)).*("title": "(.*?)"),.*("review_date": "(.*?)"),.*("review_text": "(.*?)"),')

vowpalFile = open("VowpalReviews.jl", 'a')
nlp = spacy.load('en')

good = ["good", "amazing", "awesome", "wonderful", "beautiful", "excellent", "favorable", "great", "marvelous",
        "positive", "super", "worthy", "admirable", "breathtaking", "impressive", "absorbing", "brilliant",
        "charismatic", "charming", "clever", "dazzling", "enjoyable", "entertaining", "exciting", "splendid", "legendary",
        "funny", "imaginative", "unpredictable", "surprising", "best"]
bad = ["bad", "awful", "unacceptable", "garbage", "weak", "senseless", "dull", "bland", "boring", "disappointing", "disappoint",
       "disgusting","disappointed", "distasteful", "flawed", "tiresome", "silly", "stupid", "unoriginal", "predictable",
       "uninteresting", "uninspired", "third-rate", "horrible", "wacky", "despicable", "petty", "pathetic", "junk", "worst",
       "incompetent", "not"]


with open('ReviewsFile.jl', 'r') as f:
    licznik = 0
    for line in f:
        m = getData.search(line)
        if m:
            stars = m.group(2)
            date = m.group(6).replace("on ", "").replace(" ", "-").replace(",", "")
            text = m.group(4) + " " + m.group(8)
            text = text.replace(":", "")
            doc = nlp(text)

            sentsCount = 0
            goodWordsCount = 0
            badWordsCount = 0
            for sent in doc.sents:
                sentsCount += 1
            for tok in doc:
                if str(tok).lower() in good:
                    goodWordsCount += 1
                if str(tok).lower() in bad:
                    badWordsCount += 1
            tokensCount = len(doc) / 100
            textLen = len(text) / 100
            sentsCount = sentsCount / 100
            goodWordsCount = goodWordsCount / 100
            badWordsCount = badWordsCount / 100
            vowpalFile.write(stars + " | " + "length:" + str(textLen) + " goodWords:" + str(goodWordsCount) + " badWords:" +
                             str(badWordsCount) + " sentencescount:"+str(sentsCount) + " wordscount:" + str(tokensCount) + " "
                             + date + " " + text + "\n")
            licznik+=1
            print(licznik)
         #   print(sentsCount)
            # for token in doc:
            #     print(token.text)
           # print(m.group(2), m.group(4), date, m.group(8))

vowpalFile.close()


