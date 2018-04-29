import re
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score

getData = re.compile(r'^(\d)')


predictionsFile = open('reviews.predict',"r")
predictions = predictionsFile.readlines()
predictionsFile.close()
predictions = [int(num) for num in predictions]
print(predictions)

tests = []


with open('VowpalTestSet.jl', 'r') as f:
    for line in f:
        m = getData.search(line)
        if m:
           tests.append(m.group(1))

tests = [int(num) for num in tests]


##      MEASURES

accuracy = accuracy_score(tests, predictions)
recall = recall_score(tests, predictions, average='macro')
precision = precision_score(tests, predictions, average='macro')
fmeasure = f1_score(tests, predictions, average='macro')

print("Accuracy: ", accuracy)
print("Recall: ", recall)
print("Precision: ", precision)
print("F-measure: ", fmeasure)


