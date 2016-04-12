__author__ = 'John Zhang, jwz2kn@virginia.edu', 'Tyler Ealy, tre2ca@virginia.edu'

import json
import numpy as np

data = list()
# JSON path
def main():
    with open('/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/training_data.json', 'r') as json_data:
        for line in json_data:
            data.append(json.loads(line))
    #print_training_data(data)

def print_training_data(d):
    for i in range(len(d)):
        print(json.dumps(d[i]))


if __name__ == "__main__":
    main()