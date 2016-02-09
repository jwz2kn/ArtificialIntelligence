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

def list():
    rv = "Root Variables: \n"
    lv = "\nLearned Variables: \n"
    fts = "\nFacts: \n"
    rs = "\nRules: \n"

    for i in root:
        rv += "\t" + root[i, 1] + " = " + "\"" + root[i, 2] + "\"" + "\n"

    for j in learned:
        lv += "\t" + learned[j, 1] + " = " + "\"" + learned[j, 2] + "\"" + "\n"

    for k in facts:
        fts += "\t" + facts[k, 1] + "\n"

    for l in rules:
        rs += "\t" + rules[l, 1] + " -> " + rules[l, 2] + "\n"

    ans = rv + lv + fts + rs
    return
def parser():
    return

def main():
    root.append(["S", "Sam likes Ice Cream"])
    root.append(["V", "Today is Sunday"])
    root.append(["U", "Ursula likes Chocolate"])
    learned.append(["T", "Test learned variable"])
    rules.append(["S&V", "T"])
    facts.append(["S", True])
    facts.append(["T", True])
    print list()
    return
if __name__ == "__main__":
    main()


