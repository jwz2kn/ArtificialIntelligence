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
    print "Welcome to Expert System Shell! Please enter Help for help, or other commands to teach something!"
    print "Type Quit to quit."
    while True:
        data = str(input("> "))
        if parseInput(data) == "Quit":
            break
        elif not parseInput(data):
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
def addRoot():
    return

def addBool():
    return

def addRule():
    return

# Learn more variables
def learn():
    return

# Ask about a rule or var
def query():
    return

# Return logic for why a learn process worked
def why():
    return

# Parses the input and calls appropriate method
def parseInput(data):
    if data.startswith('Quit'):
        return "Quit"
    if data.startswith('Teach '):
        
    elif data == 'List':
        print listAll()
    elif data.startswith('Learn '):

    elif data.startswith('Query '):

    elif data.startswith('Why (') & data.endswith(')'):
        why()
    else:
        return False

# Parses the logic
def parseLogic(logicStr):
    return

if __name__ == "__main__":
    main()


