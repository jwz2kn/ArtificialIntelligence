__author__ = 'John Zhang', 'Tyler Ealy'

"""
    CS 4710 Spring 2016 at UVA
    Homework 1, Expert Shell System, 02/22/2016
    This is a simple implementation of an expert shell system that allows users to enter in variables, facts, and rules.
    The system will remember this information and learn new variables.

    jwz2kn@virginia.edu, tre7ca@virginia.edu
"""

import numpy
import scipy
import string
import re
root = list()
facts = list()
rules = list()
learned = list()

def main():
    root.append("S = \"Sam likes Ice Cream\"")
    root.append("V = \"Today is Sunday\"")
    root.append("U = \"Ursula likes Chocolate\"")
    learned.append("T = \"Test learned variable\"")
    rules.append("S^V -> T")
    facts.append("S")
    facts.append("T")
    print listAll()
    print "Welcome to Expert System Shell! Please type 'q' to quit."
    while True:
        data = raw_input("> ")
        inputResult = parseInput(data)
        if inputResult == "q":
            break
        elif not inputResult:
            print "Wrong command!"
    return

# Return list of all strings variables
def listAll():
    rv = "Root Variables: \n"
    lv = "\nLearned Variables: \n"
    fts = "\nFacts: \n"
    rs = "\nRules: \n"

    # These are for-each loops
    for i in root:
        rv += "\t" + i + "\n"

    for j in learned:
        lv += "\t" + j + "\n"

    for k in facts:
        fts += "\t" + k + "\n"

    for l in rules:
        rs += "\t" + l +"\n"

    ans = rv + lv + fts + rs
    return ans

# Teach methods
def addRoot(strR):
    print "Called Teach"
    strRForm = strR.replace("Teach -R ", "")
    root.append(strRForm)
    return

def addBool(strB):
    print "Called Teach"
    indexOfEquals = strB.index("=")
    firstPart = strB[6:indexOfEquals-1]
    secondPart = strB[indexOfEquals+2:]
    varIsInRoot = False
    varIsInLearned = False
    for val in root:
        if firstPart in val:
            varIsInRoot = True
            break
    for val in learned:
        if firstPart in val:
            varIsInLearned = True
            break
    if varIsInRoot and not varIsInLearned:
        if (not (firstPart in facts)) and secondPart == "true":
            facts.append(firstPart)
        if (firstPart in facts) and secondPart == "false":
            facts.remove(firstPart)
    else:
        print "Variable must be a root variable to be given a truth value."
    return

def addRule(strRu):
    print "Called Teach"
    # Do logic checking for correct rule...?
    indexOfDash = strRu.index("-")
    # firstPart = strRu[6:indexOfDash-1]
    # secondPart = strRu[indexOfDash+3:]
    phrase = strRu[6:]
    allow = string.letters
    finalPhr = re.sub('[^%s]' % allow, '', phrase)
    print finalPhr
    rules.append(phrase)
    return

# Learn more variables
def learn():
    print "Called Learn"
    # Do a loop thru the rules (and vars and bools maybe), then add to learned list on each iteration
    return

# Ask about a rule or var
def query():
    print "Called Query"
    # Calculate and print truth value of their expression, using backwards chaining
    return

# Return logic for why a learn process worked
def why():
    boolAns = False
    strAns = str(boolAns)
    print "Called Why"
    # Calculate and print truth value of their expression along with the proof why.
    return str(boolAns)

# Parses the input and calls appropriate method
def parseInput(data):
    if data.startswith("q"):
        return "q"
    if data.startswith("Teach "):
        if data.startswith("Teach -R") & (" = \"" in data) & data.endswith("\""):
            addRoot(data)
        elif data.startswith("Teach -L"):
            print "A learned variable cannot be set true directly! It must be inferred via inference rules."
        elif data.startswith("Teach ") and " = " in data and (data.endswith("true") or data.endswith("false")):
            addBool(data)
        elif data.startswith("Teach ") and " -> " in data:
            addRule(data)
        print "Call Teach"
        return True
    elif data == "List":
        print listAll()
        return True
    elif data == "Learn":
        print "Call Learn"
        learn()
        return True
    elif data.startswith("Query (") & data.endswith(")"):
        print "Call Query"
        query()
        return True
    elif data.startswith("Why (") & data.endswith(")"):
        print "Call Why"
        why()
        return True
    else:
        return False

# Parses the logic
def parseLogic(logicStr):
    return

if __name__ == "__main__":
    main()


