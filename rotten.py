import itertools
import pickle
import urllib3
import certifi
import requests
import re
import subprocess
import progressbar

from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import sent_tokenize
from nltk.tag.perceptron import PerceptronTagger
from nltk.tokenize import ToktokTokenizer

MODEL = 'reviews/reviews.model'
PREDICTIONS = 'reviews/reviews.predict'
TEMP_FILE = 'reviews/temp.jl'

widgets = [
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.Percentage(), ') ',
]


def count_average_score():
    lines = 0
    sum = 0
    with open(PREDICTIONS, 'r') as file:
        for line in file:
            sum += int(line)
            lines += 1
    average = sum / lines
    return round(average, 2)


def get_program():
    tv_schedule = 'http://www.ontvtonight.com/guide/genres/movies.html'
    page = urlopen(tv_schedule)
    soup3 = BeautifulSoup(page, 'html.parser')

    lista = soup3.find_all('tr')

    program = {}

    for film in lista[2:len(lista) - 1]:
        time = film.td.h5.text.replace(u'\xa0', u' ')
        title = film.find_next('h5').find_next('h5').a.text.strip()
        channel = film.find_next('h5').find_next('h5').find_next('h5').a.text.strip()
        channel = channel.replace('\t', '').replace('\n', ' ')
        program[title] = [time, channel]

    return program


def get_google_result(title):
    research = "rotten tomatoes " + title
    goog_search = "https://www.google.com/search?q=" + research

    r = requests.get(goog_search)

    bs = BeautifulSoup(r.text, "html.parser")
    link = bs.find('h3').find('a').get('href')
    link = re.findall(r'https://www.rottentomatoes.com/m/.*/', link)

    if not link or not re.search(r'rottentomatoes.com/m', link[0]):
        return False

    r = requests.get(link[0])
    bs = BeautifulSoup(r.text, "html.parser")
    link_object = bs.find('a', href=True, text=re.compile('\.*?View All Audience Reviews\.*?'))

    if not link_object:
        return False

    href = link_object.get('href')

    review_link = "https://rottentomatoes.com" + href

    return review_link


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

program = get_program()
program_with_scores = {}

for key, value in progressbar.progressbar(program.items(), max_value=len(program.items()), widgets=widgets):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    url = get_google_result(key)
    if not url:
        continue
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, 'html.parser')
    pageInfo = soup.find('span', attrs={'class': 'pageInfo'}).text
    count = int(re.search(r'of ([0-9]+)', pageInfo).group(1)) + 1

    if count > 25:
        count = 25

    reviews = []
    toktok = ToktokTokenizer()
    tagger = PerceptronTagger()

    temp_file = open(TEMP_FILE, 'w', encoding='utf-8')

    href = re.findall(r'/m/.*/reviews/', url)
    for i in range(1, count):
        url = 'https://www.rottentomatoes.com' + href[0] + '?page=' + str(i) + '&type=user'
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data, 'html.parser')
        for j in soup.select('div.user_review'):
            text = j.text.replace(':', '')
            sentences = sent_tokenize(text)
            tokens = [toktok.tokenize(sent) for sent in sentences]
            tokens = list(itertools.chain.from_iterable(tokens))

            good_words_count = 0
            bad_words_count = 0

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

            temp_file.write(
                "| " + "length:" + str(text_len) + " goodWords:" + str(good_words_count) + " badWords:" +
                str(bad_words_count) + " sentencescount:" + str(
                    sents_count) + " wordscount:" + str(
                    tokens_count) + " "
                + text + "\n")
    temp_file.close()
    subprocess.run(["vw", "-t", "-i", MODEL, TEMP_FILE, "-p", PREDICTIONS, "--quiet"])
    average = count_average_score()
    value.append(average)
    program_with_scores[key] = value

program_file = open('program_obj.bin', mode='wb')
pickle.dump(program_with_scores, program_file)
program_file.close()
