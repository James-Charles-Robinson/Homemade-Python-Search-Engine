import json
import nltk
from nltk.corpus import wordnet

#Loads dictionary of choice
def LoadDict():
    name = input("What is your dictionary ID, eg 389: ")
    name = "dictionary" + name + ".txt"
    print("Loading please wait")
    with open(name, "r") as f:
        dictionary = json.load(f)
    print("This dictionary has " + str(len(dictionary)) + " words in it")
    return dictionary

#for each word in the search, we check to see if its in dict, if so return the urls associated
def DictSearch(search, urls, dictionary):
    for word in search:
        try:
            url = dictionary[word]
            for ur in url:
                urls.append(ur)
        except:
            pass
    return urls

#gets the synonyms for each word, if less then 10 websites is found for the search, we look for synonyms aswell
def Synonyms(search):
    synonyms = []
    newSynonyms = []
    for word in search:
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas(): 
                synonyms.append(l.name())
    for synonym in synonyms:
        if synonym not in newSynonyms:
            newSynonyms.append(synonym)
    synonyms = newSynonyms
    return synonyms

#remove duplicates from a list
def RemoveDupes(lst):
    lst = list(set(lst))
    return lst
'''
first finds the word with the least results, after some testing this is usually the more important result,
for example in the search best footballer. Footballer is what we want but "best" has way more results,
so we prefer to show the word with the least results
It also finds if we can find any websites that have 2 or more words in the search, for example,
we would prefer to print out the website with "best footballer" instead of "footballer"
'''
def ReoccuringUrls(search, dictionary):
    allUrls = []
    leastOccurances = 10000
    leastOccurancesUrls = []
    for word in search:
        urls = DictSearch([word], [], dictionary)
        if len(urls) < leastOccurances:
            leastOccurances = len(urls)
            leastOccurancesUrls = urls
        if len(urls) > 0:
            urls = RemoveDupes(urls)
            for url in urls:
                allUrls.append(url)
    urls = allUrls
    multipleUrls = []
    for url in urls:
        count = urls.count(url)
        if count >= 2 and url not in multipleUrls:
            multipleUrls.append(url)
            urls.remove(url)
        elif url in multipleUrls:
            urls.remove(url)
    urls = RemoveDupes(urls)
    multipleUrls = RemoveDupes(multipleUrls)
    leastOccurancesUrls = RemoveDupes(leastOccurancesUrls)
    return multipleUrls, urls, leastOccurancesUrls

#prints the urls in order from best to worst, the order is
#search terms in url, multiple words from search in website, websites with least occuring word, all the other websites that contain one of the words
def Printing(urls, hyphenSearch, multipleUrls, leastOccurancesUrls, length):
        inLink = []
        for url in urls:
            if hyphenSearch in url:
                if length > 0:
                    print(url)
                    inLink.append(url)
                    length -= 1

        if len(multipleUrls) > 0:
            for i in range(len(multipleUrls)):
                if i <= 9 and multipleUrls[i] not in inLink and length > 0:
                    print(multipleUrls[i])
                    length -= 1
        
        for i in range(len(leastOccurancesUrls)):
            if length > 0 and leastOccurancesUrls[i] not in multipleUrls and leastOccurancesUrls[i] not in inLink:
                print(leastOccurancesUrls[i])
                length -= 1
        try:
            count = 0
            while length > 0:
                url = urls[count]
                if url not in leastOccurancesUrls and url not in multipleUrls and url not in inLink:
                    print(url)
                    length -= 1
                count += 1
        except:
            pass
        
dictionary = LoadDict()

###MAIN LOOP###

while True:
    search = (str(input("What would you like to search, no punctuation: "))).lower().split(" ")
    print("")
    urls = []
    
    multipleUrls, urls, leastOccurancesUrls = ReoccuringUrls(search, dictionary)

    numOfPrints = 10 #we only print max 10 urls
    
    if len(urls) < numOfPrints:
        synonyms = Synonyms(search)
        urls = DictSearch(synonyms, urls, dictionary)

    if len(urls) >= 1:
        print("websites found\n")
        length = len(urls)
        if length > numOfPrints:
            length = numOfPrints

        seperator = "-"
        hyphenSearch = seperator.join(search)
        Printing(urls, hyphenSearch, multipleUrls, leastOccurancesUrls, length)
            
    else:
        print("No websites found")


    print("Search done\n")
