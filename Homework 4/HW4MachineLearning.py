__author__ = 'John Zhang, jwz2kn@virginia.edu', 'Tyler Ealy, tre7ca@virginia.edu'

import json
import numpy as np

data = list()
dummyVarNumerator = 1
dummyVarDenominator = 1
probOfEachLabelDict = {}
# JSON path

def main():
    global dummyVarDenominator
    with open('/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/training_data.json', 'r') as json_data:
        for line in json_data:
            data.append(json.loads(line))
    dummyVarDenominator = len(data)
    fillProbOfEachLabelDict()
    #print(sum(probOfEachLabelDict.values()))
    #print(len(probOfEachLabelDict))
    #print_training_data(data)
    #print(len(data))


def print_training_data(d):
    for i in range(len(d)):
        print(json.dumps(d[i]))

def fillProbOfEachLabelDict():
    denom = len(data)
    numer = 0.0
    currentLabel = ""
    for i in range(denom):
        if i == 0:
            currentLabel = data[i]['cuisine']
            numer += 1
            continue
        if data[i]['cuisine'] == currentLabel:
            numer += 1
        elif data[i]['cuisine'] != currentLabel:
            currentProb = numer/denom
            probOfEachLabelDict[currentLabel] = currentProb
            numer = 1.0
            currentLabel = data[i]['cuisine']
        if i == denom - 1:
            currentProb = numer/denom
            probOfEachLabelDict[currentLabel] = currentProb


if __name__ == "__main__":
    main()
