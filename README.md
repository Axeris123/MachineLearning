# Uczenie Maszynowe - Recenzje

Jest to projekt z uczenia maszynowego na przedmiot Przetwarzanie Języka Naturalnego

### Wymagania

* [Vowpal Wabbit] Do uruchomienia projektu potrzebny nam jest Vowpal Wabbit. Dokładne instrukcje dotyczące instalacji znajdują się na stronie: https://github.com/JohnLangford/vowpal_wabbit/wiki/

* [Plik z recenzjami] Recenzje zescrape'owane z Amazona znajdują się w pliku ReviewsFile.jl. Możliwe jest scrape'owanie recenzji z innych portali, jednak wtedy trzeba byłoby odpowiednio zmodyfikować skrypt generateVowpal.py

* Pakiety scikit-learn wraz z zależnościami(scipy, numpy), progressbar, nltk

# Nowa instrukcja
W celu zanstalowania wszystkich potrzebnych pakietów należy wywołać polecenie:

```
pip install -r requirements.txt
```

Następnie, w celu uruchomienia programu i wykonania wszystkich rzeczy, które były robione po kolei przez poniższe skrypty, wywołujemy:

```
python reviewsProject.py
```

I to tyle :)

### Generowanie pliku w formacie akceptowanym przez Vowpala

W celu przekonwertowania pliku z recenzjami na plik akceptowany przez Vowpala służy skrypt generateVowpal.py. Uruchamiamy go poleceniem:

```
python3 generateVowpal.py
```
Trzeba wziąć pod uwagę, że plik z recenzjami zawiera około 180 tysięcy linii. Przekonwertowanie go przy użyciu tego skryptu trwa ~20-30min.

### Sortowanie pliku

Gdy już mamy nasz wygenerowany plik VowpalReviews.jl należy go przesortować, żeby podczas uczenia Vowpal poprawnie zanalizował nasze recenzje.

```
python3 shuffleLines.py
```

### Dzielenie zbioru na zbiór uczący i zbiór testowy

Po przesortowaniu naszego zbioru następnie należy podzielić go na 2 zbiory: uczący i testowy. Zwykle przyjmuje się, że zbiór uczący to ~90% całego zbioru, a zbiór testowy to pozostałe 10%. Skrypt getTestSet.py znajduje się w katalogu vowpalfinal, ponieważ chciałem w miarę uporządkować pliki.

```
python3 getTestSet.py
```

### Uczenie

Po tym jak już podzeliliśmy nasz zbiór na zbiór uczący i testowy w końcu możemy przejść do meritum sprawy: żeby wygenerować model należy wywołać polecenie:

```
vw --oaa 5 --loss_function=logistic VowpalTrainSet.jl  -f reviews.model
```

* [-oaa 5] oznacza, że stosujemy metodę One Against All, oraz nasza klasyfikacja jest 5-klasowa (od 1 do 5 gwiazdek). Więcej o metodzie OAA na stronie: https://github.com/JohnLangford/vowpal_wabbit/wiki/One-Against-All-(oaa)-multi-class-example

* [-loss_function=logistic] Jako funkcji kosztu używamy regresję logistyczną (ponieważ daje ona najlepsze wyniki przy klasyfikacji multiklasowej). https://en.wikipedia.org/wiki/Multinomial_logistic_regression


### Przewidywanie

Jak już mamy nasz model vowpala zapisany do pliku reviews.model, możemy na jego podstawie przewidywać oceny innych recenzji wywołując polecenie:

```
vw -t -i reviews.model VowpalTestSet.jl -p reviews.predict
```
* [-t] oznacza, że testujemy - przy przewidywaniu nie będzie brana ocena widniejąca jako etykieta linii
* [-i] ozacza, że jako model regresji przyjmujemy model z pliku reviews.model
* [-p] wskasuje miejsce, do którego mają trafić wyniki przewidywania

### Statystyki

Wygenerowany plik reviews.predict zawiera wyniki przewyidywań. W każdej linii znajduje się ocena 1-5. Oceny te odpowiadają kolejnym liniom ze zbioru testowego VowpalTestSet.jl. W celu przeliczenia statystyk i skuteczności naszych przewidywań należy uruchomić skrypt:

```
python3 giveResults.py
```

Pokażą się 4 statystki: Accuracy, Recall, Precision, F-Measure (Celność, Pokrycie, Precyzja, F-Wynik). Wszystkie te statystyki są dokładnie wytłumaczone na Wikipedii: https://en.wikipedia.org/wiki/Precision_and_recall.
