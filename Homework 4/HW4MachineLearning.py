__author__ = 'John Zhang, jwz2kn@virginia.edu', 'Tyler Ealy, tre7ca@virginia.edu'

import json
import math
import csv
import time
import resource
import platform

print "Machine Learning with Cuisine Training Set Data"
print "Please make sure to open .py file and use correct data paths"

training_data_path = '/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/training_data.json'
ingredients_path = '/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/ingredients.txt'
test_data_path = '/Users/John/Desktop/CS 4710/ArtificialIntelligence/Homework 4/test_data_sample.json'

print "Current data paths: "
print "Training Data Path:", training_data_path
print "Ingredients Path:", ingredients_path
print "Testing Data Path:", test_data_path

start_time = time.time()

data = list()
ingredients = list()
testing_data = list()

dummyVarNumerator = 1.0
dummyVarDenominator = 1

recipesGivenCuisine = {}
probOfEachLabelDict = {}
nLogProbOfEachLabel = {}

probOfEachIngredGivenLabel = {}
NumOfRecipesGivenCuisine = {}
NumOfTimesIngredientOccursGivenC = {}


def main():
    global dummyVarDenominator, nLogProbOfEachLabel
    with open(training_data_path, 'r') as json_data:
        for line in json_data:
            data.append(json.loads(line))
    with open(ingredients_path, 'r') as ingredients_text:
        for line in ingredients_text:
            ingredients.append(json.loads(line))
    with open(test_data_path, 'r') as json_test_sample:
        for line in json_test_sample:
            testing_data.append(json.loads(line))
    dummyVarDenominator = len(ingredients)
    fillProbOfEachLabelDict()
    nLogProbOfEachLabel = nLogOfDict(probOfEachLabelDict)
    fillNumRecipeGivenC()
    initializeIngredProbList()
    makeIngredientsOccurencesDict()
    # print(NumOfTimesIngredientOccursGivenC['Turkish bay leaves'])
    fillIngredProbList()
    naive_bayes_learn(testing_data)
    # print(recipesGivenCuisine['greek'])
    # print(NumOfRecipesGivenCuisine)
    # print(probOfEachIngredGivenLabel['chinese']['Turkish bay leaves'])
    # print(probOfEachIngredGivenLabel['greek']['Turkish bay leaves'])
    # print(sum(probOfEachLabelDict.values()))
    # print(len(probOfEachLabelDict))
    # print(probOfEachLabelDict)
    # print(nLogProbOfEachLabel)

    # print(NumOfRecipesGivenCuisine)
    # print_training_data(data)
    # print(len(data))
    # print(len(ingredients))


def print_training_data(d):
    for i in range(len(d)):
        print(json.dumps(d[i]))


def nLogOfDict(d):
    keys = d.keys()
    endDict = {}
    for k in keys:
        endDict[k] = math.log(d[k])
    return endDict


def fillProbOfEachLabelDict():
    # This is WITHOUT natural log transform
    denom = len(data)
    numer = 0.0
    currentLabel = ""
    currentCuisineRecipes = list()
    for i in range(denom):
        if i == 0:
            currentLabel = data[i]['cuisine']
            currentCuisineRecipes.append(data[i])
            numer += 1
            continue
        if data[i]['cuisine'] == currentLabel:
            currentCuisineRecipes.append(data[i])
            numer += 1
        elif data[i]['cuisine'] != currentLabel:
            currentProb = numer/denom
            probOfEachLabelDict[currentLabel] = currentProb
            recipesGivenCuisine[currentLabel] = currentCuisineRecipes
            numer = 1.0
            currentLabel = data[i]['cuisine']
            currentCuisineRecipes = list()
            currentCuisineRecipes.append(data[i])
        if i == denom - 1:
            currentProb = numer/denom
            probOfEachLabelDict[currentLabel] = currentProb
            currentCuisineRecipes.append(data[i])
            recipesGivenCuisine[currentLabel] = currentCuisineRecipes


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
    m = len(data)
    for i in ingredients:
        NumOfTimesIngredientOccursGivenC[i] = {}
        for c in cuisines:
            currentNumberOfIngredGivenC = 0
            currentCuisineRecipes = recipesGivenCuisine[c]
            for item in currentCuisineRecipes:
                if i in item['ingredients']: # data[j]['cuisine'] == c and
                    currentNumberOfIngredGivenC += 1
            NumOfTimesIngredientOccursGivenC[i][c] = currentNumberOfIngredGivenC


def naive_bayes_learn(examples):
    l = len(examples)
    cuisines = probOfEachLabelDict.keys()
    with open('recipes.csv', 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['id', 'cuisine'])
        for i in range(l):
            chosenLabel = ""
            currentMaxScore = float("-inf")
            for c in cuisines:
                if search_match_current_data(testing_data[i]['ingredients']) != "":
                    chosenLabel = search_match_current_data(testing_data[i]['ingredients'])
                    break
                if classify_new_instance(testing_data[i]['ingredients'], c) > currentMaxScore:
                    currentMaxScore = classify_new_instance(testing_data[i]['ingredients'], c)
                    chosenLabel = c
            csvwriter.writerow([testing_data[i]['id'], chosenLabel])
            print testing_data[i]['id'], chosenLabel


def classify_new_instance(ingreds, c):
    vnb = nLogProbOfEachLabel[c]
    for i in ingreds:
        vnb += probOfEachIngredGivenLabel[c][i]
    return vnb


def search_match_current_data(ingreds):
    l = len(data)
    label = ""
    for i in range(l):
        if data[i]['ingredients'] == ingreds:
            label = data[i]['cuisine']
            break
    return label


if __name__ == "__main__":
    main()

plat = platform.platform()
multiplier = 1e-6
lb = "MB"
if "Linux" in plat:
    # Linux gets memory in KB, not B, still need to convert to MB for display
    multiplier = 0.001

print "PLATFORM:", plat
print("EXECUTION TIME: %.6f s" % (time.time() - start_time))
if "Windows" not in plat:
    print "MEMORY USAGE:", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * multiplier, lb
else:
    print "Windows memory measurement not available. Usage similar to Mac and Linux, about 14 MB"
