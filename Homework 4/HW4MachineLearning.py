__author__ = 'John Zhang, jwz2kn@virginia.edu', 'Tyler Ealy, tre7ca@virginia.edu'

import json
import numpy as np
import math

data = list()
dummyVarNumerator = 1.0
dummyVarDenominator = 1
probOfEachLabelDict = {}
nLogProbOfEachLabel = {}
probOfEachIngredGivenLabel = {}
NumOfIngredientsGivenCuisine = {}

# JSON path

def main():
    global dummyVarDenominator
    with open('/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/training_data.json', 'r') as json_data:
        for line in json_data:
            data.append(json.loads(line))
    dummyVarDenominator = len(data)
    fillProbOfEachLabelDict()
    nLogProbOfEachLabel = nLogOfDict(probOfEachLabelDict)
    fillNumIngredGivenC()
    # print(sum(probOfEachLabelDict.values()))
    # print(len(probOfEachLabelDict))
    # print(probOfEachLabelDict)
    # print(nLogProbOfEachLabel)
    # initializeIngredProbList()
    print(NumOfIngredientsGivenCuisine)
    #print_training_data(data)
    #print(len(data))


def print_training_data(d):
    for i in range(len(d)):
        print(json.dumps(d[i]))


def nLogOfDict(dict):
    keys = dict.keys()
    endDict = {}
    for k in keys:
        endDict[k] = math.log(dict[k])
    return endDict


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


def initializeIngredProbList():
    global probOfEachIngredGivenLabel
    keys = probOfEachLabelDict.keys()
    for k in keys:
        probOfEachIngredGivenLabel[k] = {}
    print probOfEachIngredGivenLabel


def fillIngredProbList():
    global probOfEachIngredGivenLabel
    keys = probOfEachLabelDict.keys()


def fillNumIngredGivenC():
    l = len(data)
    currentIngredientsSum = 0
    currentLabel = ""
    for i in range(l):
        if i == 0:
            currentLabel = data[i]['cuisine']
            currentIngredientsSum += len(data[i]['ingredients'])
            continue
        if data[i]['cuisine'] == currentLabel:
            currentIngredientsSum += len(data[i]['ingredients'])
        elif data[i]['cuisine'] != currentLabel:
            NumOfIngredientsGivenCuisine[currentLabel] = currentIngredientsSum
            # reset + count the current thing
            currentLabel = data[i]['cuisine']
            currentIngredientsSum = 0
            currentIngredientsSum += len(data[i]['ingredients'])
        if i == l - 1:
            currentIngredientsSum += len(data[i]['ingredients'])
            NumOfIngredientsGivenCuisine[currentLabel] = currentIngredientsSum

if __name__ == "__main__":
    main()
