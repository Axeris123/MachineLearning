import random

fileName = 'VowpalShuffled.jl'

num_lines = sum(1 for line in open(fileName))
tenPercent = round(num_lines * 0.1)

setToRewrite = random.sample(list(open(fileName)), tenPercent)

reviewSet = open(fileName, "r")
lines = reviewSet.readlines()
reviewSet.close()

endFile = open("VowpalTestSet.jl", 'w')

lines = set(lines) - set(setToRewrite)

for t in setToRewrite:
    endFile.write(t)
endFile.close()

rewriteFile = open('VowpalTrainSet.jl', "w")

for line in lines:
    rewriteFile.write(line)

rewriteFile.close()
