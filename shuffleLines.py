import random
with open('VowpalReviews.jl','r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()
with open('vowpalfinal/VowpalShuffled.jl','w') as target:
    for _, line in data:
        target.write( line )