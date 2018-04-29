import random

fileName = 'VowpalShuffled.jl'

num_lines = sum(1 for line in open(fileName))
tenPercent = round(num_lines * 0.1)

setToRewrite = random.sample(list(open(fileName)), tenPercent)


reviewSet = open(fileName,"r")
lines = reviewSet.readlines()
reviewSet.close()

rewriteFile = open('VowpalTrainSet.jl',"w")

licznik = 0
for line in lines:
    if line not in setToRewrite:
        rewriteFile.write(line)
    licznik += 1
    print(licznik)

rewriteFile.close()


endFile = open("VowpalTestSet.jl", 'w')
licznik = 0
for t in setToRewrite:
    endFile.write(t)
    licznik +=1
    print(licznik)
endFile.close()
