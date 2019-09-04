import itertools
import random
import collections
import glob
import os
import json
import time

'''
This program combines all the text files 
'''

#opens the all txt files and adds the contents to the dictionary and
#file names to a list
def Open():
    openedFiles = []
    dictionaries = []
    files = glob.glob('./*.txt')
    if len(files) >= 2:
        for i in range(2):
            with open(files[i], "r") as f:
                dictionary = json.load(f)
                dictionaries.append(dictionary)
                openedFiles.append(files[i])
    return dictionaries, openedFiles

#returns how many files in dir
def NumberOfFiles():
    files = glob.glob('./*.txt')
    return len(files)

#combines 2 dictionaries
def Combine(dictionaries):
    mainDictionary = {}
    d1 = dictionaries[0]
    d2 = dictionaries[1]

    for (k, v) in list(d1.items())+list(d2.items()):
        addedUrls = []
        for url in v:
            if url not in addedUrls:
                mainDictionary.setdefault(k, [])
                mainDictionary[k].append(url)
                addedUrls.append(url)
    print("Files combined")
    return mainDictionary

#deletes opened files
def Delete(openedFiles):
    for i in range(2):
        os.remove(openedFiles[i])

#saves new file
def Save(mainDictionary):
    name = "dictionary" + str(random.randint(100, 999)) + ".txt"
    with open(name, "w+") as file:
        file.write(json.dumps(mainDictionary))

#main function
def Main():
    number = NumberOfFiles()
    if number > 1:
        dictionaries, openedFiles = Open()
        
        mainDictionary = Combine(dictionaries)
            
        Save(mainDictionary)
        Delete(openedFiles)
