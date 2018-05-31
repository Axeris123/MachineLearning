import re
import itertools
import progressbar
import random
import os
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from subprocess import run
from nltk import sent_tokenize
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import ToktokTokenizer

REVIEWS_FILE = 'reviews/ReviewsFile.jl'
REVIEWS_VOWPAL = 'reviews/VowpalReviews.jl'
REVIEWS_SHUFFLED = 'reviews/VowpalShuffled.jl'
TRAIN_SET = 'reviews/VowpalTrainSet.jl'
TEST_SET = 'reviews/VowpalTestSet.jl'
MODEL = 'reviews/reviews.model'
PREDICTIONS = 'reviews/reviews.predict'


def generate_vowpal():
    get_data = re.compile(r'("stars": (\d)).*("title": "(.*?)"),.*("review_date": "(.*?)"),.*("review_text": "(.*?)"),')

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
    # tagger = PerceptronTagger()

    vowpal_file = open(REVIEWS_VOWPAL, 'a')
    widgets = [
        ' [', progressbar.Timer(), '] ',
        progressbar.Bar(),
        ' (', progressbar.Percentage(), ') ',
    ]
    lines_number = count_lines(REVIEWS_FILE)
    with open(REVIEWS_FILE, 'r') as f:
        for line in progressbar.progressbar(f, max_value=lines_number, widgets=widgets):
            m = get_data.search(line)
            if m:
                stars = m.group(2)
                #   date = m.group(6).replace("on ", "").replace(" ", "-").replace(",", "")
                text = m.group(4) + " " + m.group(8)
                text = text.replace(":", "")
                sentences = sent_tokenize(text)
                tokens = [toktok.tokenize(sent) for sent in sentences]
                tokens = list(itertools.chain.from_iterable(tokens))
                # tags = tagger.tag(tokens)

                good_words_count = 0
                bad_words_count = 0
                # adj_count = 0
                # noun_count = 0
                # verb_count = 0

                # #  text_with_tags = ''
                # for string, tag in tags:
                #     #    text_with_tags += string + ' ' + tag + ' '
                #     if tag == 'ADJ':
                #         adj_count += 1
                #     elif tag == 'VERB':
                #         verb_count += 1
                #     elif tag == 'NOUN':
                #         noun_count += 1
                #     else:
                #         continue

                for tok in tokens:
                    if str(tok).lower() in good:
                        good_words_count += 1
                    if str(tok).lower() in bad:
                        bad_words_count += 1

                tokens_count = len(tokens) / 100
                text_len = len(text) / 100
                sents_count = len(sentences) / 100
                good_words_count = good_words_count / 100
                bad_words_count = bad_words_count / 100
                vowpal_file.write(
                    stars + " | " + "length:" + str(text_len) + " goodWords:" + str(good_words_count) + " badWords:" +
                    str(bad_words_count) + " sentencescount:" + str(sents_count) + " wordscount:" + str(
                        tokens_count) + " "
                    + " " + text + "\n")
    vowpal_file.close()
    return True


def shuffle_lines():
    with open(REVIEWS_VOWPAL, 'r') as source:
        data = [(random.random(), line) for line in source]
    data.sort()
    with open(REVIEWS_SHUFFLED, 'w') as target:
        for _, line in data:
            target.write(line)
    return True


def get_test_set():
    file_name = REVIEWS_SHUFFLED

    num_lines = count_lines(file_name)
    ten_percent = round(num_lines * 0.1)

    set_to_rewrite = random.sample(list(open(file_name)), ten_percent)

    review_set = open(file_name, "r")
    lines = review_set.readlines()
    review_set.close()

    end_file = open(TEST_SET, 'w')

    lines = set(lines) - set(set_to_rewrite)

    for t in set_to_rewrite:
        end_file.write(t)
    end_file.close()

    rewrite_file = open(TRAIN_SET, "w")

    for line in lines:
        rewrite_file.write(line)

    rewrite_file.close()
    return True


def give_results():
    get_data = re.compile(r'^(\d)')

    predictions_file = open(PREDICTIONS, "r")
    predictions = predictions_file.readlines()
    predictions_file.close()
    predictions = [int(num) for num in predictions]
    tests = []

    with open(TEST_SET, 'r') as f:
        for line in f:
            m = get_data.search(line)
            if m:
                tests.append(m.group(1))

    tests = [int(num) for num in tests]

    # MEASURES

    accuracy = accuracy_score(tests, predictions)
    recall = recall_score(tests, predictions, average='macro')
    precision = precision_score(tests, predictions, average='macro')
    fmeasure = f1_score(tests, predictions, average='macro')

    print("Accuracy: ", accuracy)
    print("Recall: ", recall)
    print("Precision: ", precision)
    print("F-measure: ", fmeasure)
    return True


def count_lines(filename):
    f = open(filename)
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)
    return lines


def main():
    if not os.path.exists(REVIEWS_VOWPAL):
        generate_vowpal()
    if not os.path.exists(REVIEWS_SHUFFLED):
        shuffle_lines()
    if not os.path.exists(TRAIN_SET) and not os.path.exists(TEST_SET):
        get_test_set()
    if os.path.exists(TRAIN_SET) and os.path.exists(TEST_SET):
        run(["vw", "--oaa", "5", "--loss_function=logistic", TRAIN_SET, "-f", MODEL])
        run(["vw", "-t", "-i", MODEL, TEST_SET, "-p", PREDICTIONS])
        if os.path.exists(MODEL) and os.path.exists(PREDICTIONS):
            give_results()
        else:
            print('Nie udało się poprawnie wygenerować modelu statystycznego!')
    else:
        print('Nie udało się wygenerować zbioru testowego i uczącego!')


if __name__ == "__main__":
    main()
