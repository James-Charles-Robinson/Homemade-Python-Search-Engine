import requests
from bs4 import BeautifulSoup
import random
import json
import string
import combine

#gets the html from the url
def GetHTML(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")
    return soup

#gets all the valid href's
def GetHref(soup):
    links = []
    hrefs = soup.find_all("a")
    for href in hrefs:
        href = href.get("href")
        if href != None and href != "/" and ("http:" in href or "https:" in href) and len(href) < 110 and "\n" not in href and "/n" not in href and "wiktionary" not in href:
            if ("wikipedia" in href and "en" in href) or "wikipedia" not in href:
                links.append(href)
    return links

#gets all the text from the page
def GetText(soup):
    translator = str.maketrans('', '', string.punctuation)
    allWords = []
    sentences = soup.find_all("p")
    for sentence in sentences:
        words = sentence.getText().split(" ")
        for word in words:
            word = (word.translate(translator)).lower().rstrip()
            if word not in stopWords and word not in allWords and "\\" not in word and word != "" and word != " " and len(word) < 20:
                allWords.append(word)
    return allWords

#usines combine.py to combine the txt files in the dir, this is done so lists and dicts in the program dont get
#too long and therefore the program runs out of memory
def TryCombine():
    length = combine.NumberOfFiles()
    if length >= 2:
        combine.Main()

#as said before, this removes urls from the website list to save memory
#to get to 50000 it takes about 1 hour, and the duplicates are removed, and 25% of urls are deleted, this keeps the website list
#fresh if running for many hours
def WebsitePurge(websites):
    if len(websites) > 50000:
        count = 0
        newWebsites = []
        for i in range(int(len(websites)*0.75)):
            randomNum = random.randint(0, len(websites)-1)
            website = websites[randomNum]
            if website not in newWebsites:
                newWebsites.append(website)
            else:
                cout += 1
        websites = newWebsites
        print("new len", len(websites), "there was", count, "duplicates")
    return websites
    
#this function determines if we have been sent to a "too many requests" page instead of an actual one, this keeps
#the dictionary short and free of false positives for words such as ip and request
#it also stops the program from requesting from this website for a long period of time, about 30 (however this is random)
def IpBan(soup, website, bannedWebsites):
    randomNumber = random.randint(0, 3000)
    if randomNumber == 8 and len(bannedWebsites) > 0:
        print("banned websites cleared, there used to be", len(bannedWebsites), "websites in that list")
        bannedWebsites = []
    if website.split("/")[2] not in bannedWebsites:
        sentences = soup.find_all("p")
        for sentence in sentences:
            try:
                if "too many requests" in sentence or "rate limit" in sentence or "404" in sentence or "User-Agent" in sentence:
                    print(website, "ip banned you by sentence")
                    bannedWebsites.append(website.split("/")[2])
                    if "stack" in website:
                        bannedWebsites.append("stack")
            except:
                pass
            words = sentence.getText().split(" ")
            for word in words:
                if word == "Reason:" or word == "XID:":
                    print(website, "ip banned you by word")
                    bannedWebsites.append(website.split("/")[2])
                    if "stack" in website:
                        bannedWebsites.append("stack")
    return bannedWebsites


#adds the website url to all of the words contained in the website to a dictionary
def AddToDictionary(website, dictionary, soup, seedWebsites):
    if website not in seedWebsites: 
        words = GetText(soup)
        for word in words:
            word.replace("\t", "")
            if word != "" and word != " ":
                dictionary.setdefault(word, [])
                dictionary[word].append(website)
    return dictionary

#prints out the progress
def Progress(frequency, i, donePercentage):
    percentage = round((i / frequency)*100)
    if percentage % 5 == 0 and percentage not in donePercentage:
        print("\n " + str(percentage) + "%\n")
        donePercentage.append(percentage)
    return donePercentage

#removes duplicate urls from each word in the dictionary, this can be quite a significant amount (about 50%)
def RemoveDupes(dictionary):
    print("starting to remove dupes")
    newDict = {}
    counta = 0
    countb = 0
    for key, value in dictionary.items():
        urls = value
        ur = []
        for i in range(3):
            for url in urls:
                if url not in ur:
                    counta += 1
                    ur.append(url)
                else:
                    countb += 1
            urls = ur
        for url in urls:
            newDict.setdefault(key, [])
            newDict[key].append(url)
    return newDict

#gets the seed websites from seeds.rtf, rtf file is used so its not combined by TryCombine()
def Seeds():
    with open("seeds.rtf", "r") as f:
        urls = f.readlines()

    websites = []
    for i in range(len(urls)):
        website = urls[i]
        websites.append(website.rstrip())

    seedWebsites = websites[:]
        
    return websites, seedWebsites

#removes the processed urls from the list and write then to a file
def Write(dictionary):
    name = "dictionary" + str(random.randint(100, 999)) + ".txt"
    dictionary = RemoveDupes(dictionary)
    with open(name, "w+") as file:
        file.write(json.dumps(dictionary))


#the whole process for each website
def Main(websites, dictionary, i, lastWebsites, bannedWebsites, seedWebsites):
    try:
        website = websites[i]
        if (website.split("/")[2]) not in lastWebsites and website.split("/")[2] not in bannedWebsites and ("stack" not in website or ("stack" in website and "stack" not in bannedWebsites)):
            if len(lastWebsites) >= 15: #15 websites are in this list at a time, this avoids spam as much as possible,
                lastWebsites.pop(0)     #doesnt work well for websites that use different portals for different languages or subjects, such as wikipedia and stackoverflow/exchange
            lastWebsites.append(website.split("/")[2])
            soup = GetHTML(website)
            bannedWebsites = IpBan(soup, website, bannedWebsites)
            newLinks = GetHref(soup)
            for newLink in newLinks:
                if newLink not in websites:
                    websites.append(newLink)
            dictionary = AddToDictionary(website, dictionary, soup, seedWebsites)
    except:
        print(website, "failed to respond")
    return websites, dictionary, lastWebsites, bannedWebsites


###MAIN PROGRAM###

#seeds
websites, seedWebsites = Seeds()
seedLength = len(seedWebsites)
print(seedLength)

#these words arent added to the dictionary, same ones used as google
stopWords = ["I", "a", "about", "an", "are", "as", "at", "be", "by", "com", "for", "from", "how", "in",
             "is", "it", "of", "on", "or", "that", "the", "this", "to", "was", "what", "when", "where", "who", "will", "with", "the", "www"]

  
frequency = 200 #how many websites it should scrape per run, takes about 1 second per url, depending on many factors
dictionary = {}
bannedWebsites = []
lastWebsites = ["https://random.com"]

#gets the data from the seeds
#takes about 1 second per seed depending on how large and response the urls are
print("\nGetting urls from seeds")
for i in range(seedLength):
    websites, dictionary, lastWebsites, bannedWebsites = Main(websites, dictionary, i, lastWebsites, bannedWebsites, seedWebsites)
print("Finished scraping seeds")

#then proceeds to randomly try out collected urls
while True:
    donePercentage = [0]
    for g in range(frequency):
        i = random.randint(0, len(websites)-1)
        websites, dictionary, lastWebsites, bannedWebsites = Main(websites, dictionary, i, lastWebsites, bannedWebsites, seedWebsites)
        donePercentage = Progress(frequency, g, donePercentage)

    #writes to the txt file
    Write(dictionary)
    print("Dictionary saved\n")
    print("The website list is", len(websites), "urls long")
    dictionary = {}
    websites = WebsitePurge(websites)
    #TryCombine()
