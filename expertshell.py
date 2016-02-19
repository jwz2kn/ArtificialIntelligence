__author__ = 'John Zhang', 'Tyler Ealy'

"""
    CS 4710 Spring 2016 at UVA
    Homework 1, Expert Shell System, 02/22/2016
    This is a simple implementation of an expert shell system that allows users to enter in variables, facts, and rules.
    The system will remember this information and learn new variables.

    jwz2kn@virginia.edu, tre7ca@virginia.edu
"""

# import numpy
# import scipy
import string
import re
root = list()
facts = list()
rules = list()
learned = list()
falsehoods = list()

def main():
    root.append("S = \"Sam likes Ice Cream\"")
    root.append("V = \"Today is Sunday\"")
    root.append("U = \"Ursula likes Chocolate\"")
    learned.append("T = \"Test learned variable\"")
    rules.append("S&V -> T")
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
def addLearned(strR):
    print "Called Teach"
    strRForm = strR.replace("Teach -L ", "")
    learned.append(strRForm)
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
            if firstPart in falsehoods:
                falsehoods.remove(firstPart)
        if (firstPart in facts) and secondPart == "false":
            facts.remove(firstPart)
            if firstPart not in falsehoods:
                falsehoods.append(firstPart)
    else:
        print "Variable must be a root variable to be given a truth value by user."
    return

def addRule(strRu):
    print "Called Teach"
    # Do logic checking for correct rule...?
    indexOfDash = strRu.index("-")
    firstPart = strRu[6:indexOfDash-1]
    secondPart = strRu[indexOfDash+3:]
    print firstPart
    print secondPart
    phrase = strRu[6:]
    # allow = string.letters
    # parsedPhr = re.sub('[^%s]' % allow, '', phrase)
    # print parsedPhr
    # print phrase
    #
    varsAreValid = True
    # for letter in parsedPhr:
    #     if not (letter in facts or letter in falsehoods):
    #         varsAreValid = False
    #         break
    propsLeft = list()
    propsRight = list()
    p = ""
    for l in firstPart:
        # Continue to parse for string until you hit &, |, !, (, )
        if (l != "&") & (l != "|") & (l != "!") & (l != "(") & (l != ")"):
            if l != firstPart[-1]:
                p = p + l
            else:
                p = p + l
                propsLeft.append(p)
                p = ""
        elif (l == "&") | (l == "|") | (l == "!") | (l == "(") | (l == ")"):
            propsLeft.append(p)
            p = ""

    p = ""
    for l in secondPart:
        # Continue to parse for string until you hit &, |, !, (, )
        if (l != "&") & (l != "|") & (l != "!") & (l != "(") & (l != ")"):
            if l != secondPart[-1]:
                p = p + l
            else:
                p = p + l
                propsRight.append(p)
                p = ""
        elif (l == "&") | (l == "|") | (l == "!") | (l == "(") | (l == ")"):
            propsRight.append(p)
            p = ""
    print propsLeft
    for element in propsLeft:
        print element
        if not(element in facts) and not(element in falsehoods):
            varsAreValid = False
            break
    print varsAreValid
    for element in propsRight:
        print element
        if not(element in learned):
            varsAreValid = False
            break
    # Dr. Diochnos informed us the testing team would not give logically invalid things
    if varsAreValid:
        rules.append(phrase)
    return

# Learn more variables
def learn():
    print "Called Learn"
    # Do a loop thru the rules (and vars and bools maybe), then add to learned list on each iteration
    for r in rules:
        # Parse the left side of rule, figure out truth value of the stuff on right side of rule
        # if right side == true, add to learned variables
        indexOfDash = r.index("-")
        logicStr = r[:indexOfDash-1]
        varStr = r[indexOfDash+3:]
        truthValue = parseLogic(logicStr)
        if truthValue == True and varStr not in learned:
            learned.append(varStr)
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
            addLearned(data)

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
    props = list()
    p = ""
    for l in logicStr:

        # Continue to parse for string until you hit &, |, !, (, )
        if (l != "&") & (l != "|") & (l != "!") & (l != "(") & (l != ")"):
            if l != logicStr[-1]:
                p = p + l
            else:
                p = p + l
                props.append(p)
                p = ""
        elif (l == "&") | (l == "|") | (l == "!") | (l == "(") | (l == ")"):
            props.append(p)
            p = ""

    print props
    # What rule looks like coming in: S&T|U.
    # What we want: True&False|True
    # ['S', 'T', 'U']
    # Loop thru props
    # If current prop in facts or falsehoods, add corresponding truth value to boolean list


    return

if __name__ == "__main__":
    main()


