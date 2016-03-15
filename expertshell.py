__author__ = 'John Zhang', 'Tyler Ealy'

"""
    CS 4710 Spring 2016 at UVA
    Homework 1, Expert Shell System, 02/22/2016
    This is a simple implementation of an expert shell system that allows users to enter in variables, facts, and rules.
    The system will remember this information and learn new variables.

    jwz2kn@virginia.edu, tre7ca@virginia.edu
"""
# Global variables
root = list()
facts = list()
rules = list()
learned = list()
falsehoods = list()
whyStr = ""
masterPropsString = ""

def main():
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
    # Instructions did not specify, but printing stuff that was set to false helps clarity
    fal = "\nFalsehoods: \n"
    for f in falsehoods:
        fal += "\t" + f + "\n"
    ans = rv + lv + fts + fal +rs
    return ans

# Teach methods
def addRoot(strR):
    strRForm = strR.replace("Teach -R ", "")
    root.append(strRForm)
    indexOfEquals = strR.index("=")
    secondPart = strR[indexOfEquals-1:]
    strRForm = strRForm.replace(secondPart, "")
    falsehoods.append(strRForm)
    return

def addLearned(strR):
    strRForm = strR.replace("Teach -L ", "")
    learned.append(strRForm)
    indexOfEquals = strR.index("=")
    secondPart = strR[indexOfEquals-1:]
    strRForm = strRForm.replace(secondPart, "")
    falsehoods.append(strRForm)
    return

def addBool(strB):

    indexOfEquals = strB.index("=")
    firstPart = strB[6:indexOfEquals-1]
    secondPart = strB[indexOfEquals+2:]
    varIsInRoot = False
    varIsInLearned = False
    for val in root:
        if firstPart == val[:val.index("=")-1]:
            varIsInRoot = True
            break
    for val in learned:
        if firstPart == val[:val.index("=")-1]:
            varIsInLearned = True
            break
    # Put all learned variables back into falsehoods, remove from facts
    # for val in learned:
    #     temp = val[:val.index("=")-1]
    #     if temp in facts:
    #         facts.remove(temp)
    #         falsehoods.append(temp)
    if varIsInRoot and not varIsInLearned:
        # May need to move this part of if statement for edge cases
        if (not (firstPart in facts)) and secondPart == "true":
            facts.append(firstPart)
            if firstPart in falsehoods:
                falsehoods.remove(firstPart)
        if secondPart == "false":
            if firstPart in facts:
                facts.remove(firstPart)
            if firstPart not in falsehoods:
                falsehoods.append(firstPart)
    else:
        print "Variable must be a root variable to be given a truth value by user."
    return

def addRule(strRu):
    # Do logic checking for correct rule
    indexOfDash = strRu.index("-")
    firstPart = strRu[6:indexOfDash-1]
    secondPart = strRu[indexOfDash+3:]
    phrase = strRu[6:]
    varsAreValid = True
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
            if p != "":
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
    for element in propsLeft:
        if not(element in facts) and not(element in falsehoods):
            varsAreValid = False
            break
    varsRightAreValid = False
    for element in propsRight:
        for value in learned:
            varsRightAreValid = False
            if value.startswith(element):
                varsRightAreValid = True
                break
    # Dr. Diochnos informed us the testing team would not give logically invalid things
    if varsAreValid and varsRightAreValid:
        rules.append(phrase)
    return

# Learn more variables
def learn():
    # Do a loop thru the rules, then add to learned list on each iteration
    numIter = len(rules)
    count = 0
    while (count < numIter):
        for r in rules:
            # Parse the left side of rule, figure out truth value of the stuff on right side of rule
            # if right side == true, add to learned variables
            indexOfDash = r.index("-")
            logicStr = r[:indexOfDash-1]
            varStr = r[indexOfDash+3:]
            truthValue = parseLogic(logicStr)
            varsAreValid = False
            for value in learned:
                varsAreValid = False
                if value.startswith(varStr):
                    varsAreValid = True
                    break
            if truthValue == True and varsAreValid:
                if varStr not in facts:
                    facts.append(varStr)
                if varStr in falsehoods:
                    falsehoods.remove(varStr)
            elif truthValue == False and varsAreValid:
                if varStr not in falsehoods:
                    falsehoods.append(varStr)
                if varStr in facts:
                    facts.remove(varStr)
        count += 1
    return

# Ask about a rule or var
def query(rawData):
    props = list()
    p = ""
    evalStr = ""
    for l in rawData:
        # Continue to parse for string until you hit &, |, !, (, )
        if (l != "&") & (l != "|") & (l != "!") & (l != "(") & (l != ")"):
            if l != rawData[-1]:
                p = p + l
            else: # Takes care of last proposition
                p = p + l
                props.append(p)
                if p in facts:
                    evalStr += "True"
                elif p in falsehoods:
                    evalStr += "False"
                else:
                    propIsPresent = False
                    for r in rules:
                        ruleRight = r[r.index(">")+2:]
                        ruleLeft = r[:r.index("-")-1]
                        # if right side of the rule == current proposition
                        if ruleRight == p:
                            propIsPresent = True
                            boolVal = parseLogic(ruleLeft)
                            if boolVal == True:
                                evalStr += "True"
                            elif boolVal == False:
                                evalStr += "False"
                            break
                    if not propIsPresent:
                        varPrinted = "This statement is not provable because there is no rule that can determine " + \
                            "the truth value of the proposition " + p + "."
                        print varPrinted
                        return
                p = ""
        elif (l == "&") | (l == "|") | (l == "!") | (l == "(") | (l == ")"): # Takes care of middle propositions
            if p != "":
                props.append(p)
                if p in facts:
                    evalStr += "True "
                elif p in falsehoods:
                    evalStr += "False "
                else:
                    propIsPresent = False
                    for r in rules:
                        ruleRight = r[r.index(">")+2:]
                        ruleLeft = r[:r.index("-")-1]
                        # if right side of the rule == current proposition
                        if ruleRight == p:
                            propIsPresent = True
                            boolVal = parseLogic(ruleLeft)
                            if boolVal == True:
                                evalStr += "True "
                            elif boolVal == False:
                                evalStr += "False "
                            break
                    if not propIsPresent:
                        varPrinted = "This statement is not provable because there is no rule that can determine " + \
                            "the truth value of the proposition " + p + "."
                        print varPrinted
                        return

            if l == "&":
                evalStr += "and "
            elif l == "|":
                evalStr += "or "
            elif l == "!":
                evalStr += "not "
            elif l == "(" or l == ")":
                evalStr += l
            p = ""

    result = eval(evalStr)
    print result
    return

# Return logic for why a learn process worked
def why(rawData):
    props = list()
    p = ""
    evalStr = ""
    whyStr = ""
    whyStrProps = ""
    for l in rawData:
        # Continue to parse for string until you hit &, |, !, (, )
        if (l != "&") & (l != "|") & (l != "!") & (l != "(") & (l != ")"):
            if l != rawData[-1]:
                p = p + l
            else: # Takes care of last proposition
                p = p + l
                props.append(p)
                if p in facts:
                    evalStr += "True"
                    rootRight = ""
                    for r in root:
                        if p == r[:r.index("=")-1]:
                            rootRight = r[r.index("=")+3: len(r) - 1]
                            break
                    for r in learned:
                        if p == r[:r.index("=")-1]:
                            rootRight = r[r.index("=")+3: len(r) - 1]
                            break
                    whyStr += "I KNOW THAT IT IS TRUE THAT " + rootRight + "\n"
                    whyStrProps += rootRight
                # elif p in falsehoods:
                #     evalStr += "False"
                #     rootRight = ""
                #     for r in root:
                #         if p == r[:r.index("=")-1]:
                #             rootRight = r[r.index("=")+3: len(r) - 1]
                #             break
                #     for r in learned:
                #         if p == r[:r.index("=")-1]:
                #             rootRight = r[r.index("=")+3: len(r) - 1]
                #             break
                #     whyStr += "I KNOW THAT IT IS NOT TRUE THAT " + rootRight + "\n"
                #     whyStrProps += rootRight
                else:
                    propIsPresent = False
                    for r in rules:
                        ruleRight = r[r.index(">")+2:]
                        ruleLeft = r[:r.index("-")-1]
                        # if right side of the rule == current proposition
                        if ruleRight == p:
                            propIsPresent = True
                            boolVal = parseLogic(ruleLeft)
                            rootRight = ""
                            for r in root:
                                if p == r[:r.index("=")-1]:
                                    rootRight = r[r.index("=")+3: len(r) - 1]
                                    break
                            for r in learned:
                                if p == r[:r.index("=")-1]:
                                    rootRight = r[r.index("=")+3: len(r) - 1]
                                    break
                            if boolVal == True:
                                evalStr += "True"
                                whyStr += "BECAUSE " + masterPropsString + " I KNOW THAT "+ rootRight + "\n"
                                whyStrProps += rootRight
                            elif boolVal == False:
                                evalStr += "False"
                                whyStr += "BECAUSE IT IS NOT TRUE THAT " + masterPropsString + " I CANNOT PROVE "+ \
                                          rootRight + "\n"
                                whyStrProps += rootRight
                            break
                    if not propIsPresent:
                        varPrinted = "This statement is not provable because there is no rule that can determine " + \
                            "the truth value of the proposition " + p + "."
                        print varPrinted
                        return
                p = ""
        elif (l == "&") | (l == "|") | (l == "!") | (l == "(") | (l == ")"): # Takes care of middle propositions
            if p != "":
                props.append(p)
                if p in facts:
                    evalStr += "True "
                    rootRight = ""
                    for r in root:
                        if p == r[:r.index("=")-1]:
                            rootRight = r[r.index("=")+3: len(r) - 1]
                            break
                    for r in learned:
                        if p == r[:r.index("=")-1]:
                            rootRight = r[r.index("=")+3: len(r) - 1]
                            break
                    whyStr += "I KNOW THAT IT IS TRUE THAT " + rootRight + "\n"
                    whyStrProps += rootRight
                # elif p in falsehoods:
                #     evalStr += "False "
                #     rootRight = ""
                #     for r in root:
                #         if p == r[:r.index("=")-1]:
                #             rootRight = r[r.index("=")+3: len(r) - 1]
                #             break
                #     for r in learned:
                #         if p == r[:r.index("=")-1]:
                #             rootRight = r[r.index("=")+3: len(r) - 1]
                #             break
                #     whyStr += "I KNOW THAT IT IS NOT TRUE THAT " + rootRight + "\n"
                #     whyStrProps += rootRight
                else:
                    propIsPresent = False
                    for r in rules:
                        ruleRight = r[r.index(">")+2:]
                        ruleLeft = r[:r.index("-")-1]
                        # if right side of the rule == current proposition
                        if ruleRight == p:
                            propIsPresent = True
                            boolVal = parseLogic(ruleLeft)
                            print ruleLeft
                            rootRight = ""
                            for r in root:
                                if p == r[:r.index("=")-1]:
                                    rootRight = r[r.index("=")+3: len(r) - 1]
                                    break
                            for r in learned:
                                if p == r[:r.index("=")-1]:
                                    rootRight = r[r.index("=")+3: len(r) - 1]
                                    break
                            if boolVal == True:
                                evalStr += "True "
                                whyStr += "BECAUSE " + masterPropsString + " I KNOW THAT "+ rootRight + "\n"
                                whyStrProps += rootRight
                            elif boolVal == False:
                                evalStr += "False "
                                whyStr += "BECAUSE IT IS NOT TRUE THAT " + masterPropsString + " I CANNOT PROVE "+ \
                                          rootRight + "\n"
                                whyStrProps += rootRight
                            break
                    if not propIsPresent:
                        varPrinted = "This statement is not provable because there is no rule that can determine " + \
                            "the truth value of the proposition " + p + "."
                        print varPrinted
                        return

            if l == "&":
                evalStr += "and "
                whyStrProps += " AND "
            elif l == "|":
                evalStr += "or "
                whyStrProps += " OR "
            elif l == "!":
                evalStr += "not "
                whyStrProps += " NOT "
            elif l == "(" or l == ")":
                evalStr += l
                whyStrProps += l
            p = ""

    result = eval(evalStr)
    print result
    if result == True:
        whyStr += "I THUS KNOW THAT " + whyStrProps
    else:
        whyStr += "THUS I CANNOT PROVE " + whyStrProps
    print whyStr
    return


# Parses the input and calls appropriate method
def parseInput(data):
    if data.startswith("q"):
        return "q"
    if data.startswith("Teach "):
        if data.startswith("Teach -R") & (" = \"" in data) & data.endswith("\""):
            addRoot(data)
        elif data.startswith("Teach -L") & (" = \"" in data) & data.endswith("\""):
            addLearned(data)

        elif data.startswith("Teach ") and " = " in data and (data.endswith("true") or data.endswith("false")):
            addBool(data)
        elif data.startswith("Teach ") and " -> " in data:
            addRule(data)
        return True
    elif data == "List":
        print listAll()
        return True
    elif data == "Learn":
        learn()
        return True
    elif data.startswith("Query "):
        rawData = data[6:]
        query(rawData)
        return True
    elif data.startswith("Why "):
        rawData = data[4:]
        why(rawData)
        return True
    else:
        return False

# Parses the logic
def parseLogic(logicStr):
    props = list()
    global masterPropsString
    masterPropsString = ""
    p = ""
    evalStr = ""
    for l in logicStr:
        # Continue to parse for string until you hit &, |, !, (, )
        if (l != "&") & (l != "|") & (l != "!") & (l != "(") & (l != ")"):
            if l != logicStr[-1]:
                p = p + l
            else: # Takes care of last proposition
                p = p + l
                props.append(p)
                if p in facts:
                    evalStr += "True "

                    for r in root:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break
                    for r in learned:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break
                elif p in falsehoods:
                    evalStr += "False "

                    for r in root:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break
                    for r in learned:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break

                p = ""
        elif (l == "&") | (l == "|") | (l == "!") | (l == "(") | (l == ")"): # Takes care of middle propositions
            if p != "":
                props.append(p)
                if p in facts:
                    evalStr += "True "

                    for r in root:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break
                    for r in learned:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break
                elif p in falsehoods:
                    evalStr += "False "

                    for r in root:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break
                    for r in learned:
                        if p == r[:r.index("=")-1]:
                            masterPropsString += r[r.index("=")+3: len(r) - 1]
                            break
            if l == "&":
                evalStr += "and "
                masterPropsString += " AND "
            elif l == "|":
                evalStr += "or "
                masterPropsString += " OR "
            elif l == "!":
                evalStr += "not "
                masterPropsString += " NOT "
            elif l == "(" or l == ")":
                evalStr += l
                masterPropsString += l
            p = ""

    result = eval(evalStr)
    return result

if __name__ == "__main__":
    main()


