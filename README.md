# Homemade-Python-Search-Engine
### A python program that creates a dictionary of websites and their contents and using that can be used as a search engine.
# How To Use
#### First open up your seeds.rtf file and add your own seed websites. For best results use large websites with lots of hyper links but keep the website confined to a specfic niche. Then run the Main program file with all the liberies installed and let it run. For decent results you will want to let it run for a few hours. Then once you are done, close out of that and open your Search program, then enter the dictionaries ID and search away. The main problem though with this search engine is that it doesnt have spell checking, so unless a website out there has made the same mistake as you, you wont get any results. If you want you can unzip the dictionary i've provided and use that. That dictionary is based around the defult seeds. If the main program is too slow for you, there are a few changes you can do to make it much faster. Comment out the last line in the main program, then you can open it up multiple times and let them run all at once (recommended max is 6). While that is going you are going to want to edit combine.py and put the contents of the main() in a loop and uncomment the last 2 lines. Then run this program. This means you can make the dictionary much larger, much faster.
# What I learnt
#### This program taught me many things. For example how to manage, clean and analyse large amounts of data. I had to learn how to make my data as accurate and as usefull as i could by removing unwated inputs. This included things like punctuation and unreasonably long strings. I had to remove things like this to keep my file sizes down. After my first test for 1 hour the saved dictionary was 4Gb, by the end the same style dictionary was 30Mb. This was mainly due to revisisting the same website over and over again causing it to black list my ip, causing it to scrape un-needed data. I also developed my knowledge of webscraping and other liberies.
