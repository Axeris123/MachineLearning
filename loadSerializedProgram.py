import pickle
from pprint import pprint

with open('program_obj.pickl', 'rb') as f:
    obj = pickle.load(f)

pprint(obj)
