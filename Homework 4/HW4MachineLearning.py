__author__ = 'John Zhang, jwz2kn@virginia.edu', 'Tyler Ealy, tre7ca@virginia.edu'

import json
import numpy as np
import math

data = list()
ingredients = list()
dummyVarNumerator = 1.0
dummyVarDenominator = 1
probOfEachLabelDict = {}
nLogProbOfEachLabel = {}
probOfEachIngredGivenLabel = {}
NumOfRecipesGivenCuisine = {}
NumOfTimesIngredientOccursGivenC = {}


# JSON path

def main():
    global dummyVarDenominator
    with open('/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/training_data.json', 'r') as json_data:
        for line in json_data:
            data.append(json.loads(line))
    with open('/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/ingredients.txt', 'r') as ingredients_text:
        for line in ingredients_text:
            ingredients.append(json.loads(line))
    dummyVarDenominator = len(ingredients)
    fillProbOfEachLabelDict()
    nLogProbOfEachLabel = nLogOfDict(probOfEachLabelDict)
    fillNumRecipeGivenC()
    initializeIngredProbList()
    makeIngredientsOccurencesDict()
    #print(NumOfTimesIngredientOccursGivenC['Turkish bay leaves'])
    fillIngredProbList()
    # print(NumOfRecipesGivenCuisine)
    # print(probOfEachIngredGivenLabel['chinese']['Turkish bay leaves'])
    # print(probOfEachIngredGivenLabel['greek']['Turkish bay leaves'])
    # print(sum(probOfEachLabelDict.values()))
    # print(len(probOfEachLabelDict))
    # print(probOfEachLabelDict)
    # print(nLogProbOfEachLabel)

    #print(NumOfRecipesGivenCuisine)
    #print_training_data(data)
    #print(len(data))
    #print(len(ingredients))


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
    # This is WITHOUT natural log transform
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
    #print probOfEachIngredGivenLabel


def fillIngredProbList():
    global probOfEachIngredGivenLabel, NumOfTimesIngredientOccursGivenC, NumOfRecipesGivenCuisine
    cuisines = probOfEachLabelDict.keys()
    for c in cuisines:
        probOfEachIngredGivenLabel[c] = {}
        for i in ingredients:
            # This is WITH smoothing and natural log transform
            probOfEachIngredGivenLabel[c][i] = math.log((NumOfTimesIngredientOccursGivenC[i][c] + dummyVarNumerator) \
                                               / (NumOfRecipesGivenCuisine[c] + dummyVarDenominator))

def fillNumRecipeGivenC():
    l = len(data)
    numer = 0
    currentLabel = ""
    for i in range(l):
        if i == 0:
            currentLabel = data[i]['cuisine']
            numer += 1
            continue
        if data[i]['cuisine'] == currentLabel:
            numer += 1
        elif data[i]['cuisine'] != currentLabel:
            NumOfRecipesGivenCuisine[currentLabel] = numer
            numer = 1
            currentLabel = data[i]['cuisine']
        if i == l - 1:
            NumOfRecipesGivenCuisine[currentLabel] = numer


def makeIngredientsOccurencesDict():
    global NumOfTimesIngredientOccursGivenC
    l = len(ingredients)
    cuisines = probOfEachLabelDict.keys()
    currentNumberOfIngredGivenC = 0
    m = len(data)
    for i in ingredients:
        NumOfTimesIngredientOccursGivenC[i] = {}
        for c in cuisines:
            for j in range(m):
                if data[j]['cuisine'] == c and i in data[j]['ingredients']:
                    currentNumberOfIngredGivenC += 1
            NumOfTimesIngredientOccursGivenC[i][c] = currentNumberOfIngredGivenC
            currentNumberOfIngredGivenC = 0


def naïve_bayes_classifer():
    print 1


def classify_new_instance():
    print 1

    

if __name__ == "__main__":
    main()
