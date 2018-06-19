from bs4 import BeautifulSoup  as bs
#from textgenrnn import textgenrnn as tg # takes quite a while to process due to (I believe) setting up tensorflow
import requests
import pandas as pd
import re

response = requests.get('https://www.azlyrics.com/p/passenger.html')
page = response.text
page = bs(page, "lxml")
page.prettify()
print(page)
# By inspection the page actually just maintains lists of values as a variable and subs them in when rendering

# print (albums) 

# Create dictionary with key as album name, value as list of song URLs
def create_album_list(album_page):
    page = album_page.find('div', id="listAlbum")
    album_list = {}
    a = ''
    for s in page.find_all():
        if s.name == 'div':
            if s.find_next('b') != None:
                a = s.find_next('b').contents[0].replace('"','') # Extract first element of returned list object
            else:
                a = s.contents[0].replace('"','').replace(':','')
            
            album_list[a] = []
        # print(a)

        elif s.name == 'a' and 'href' in s.attrs:
            n = s['href'].replace('..','')
            album_list[a].append('https://www.azlyrics.com'+ n)
    return album_list

# Helper function for finding relevant lyrics; used in page.find() call
def nothing_special(tag):
    return not (tag.has_attr('class') or tag.has_attr('id')) and tag.name=='div'

# Takes string of requested song, GET requests webpage, and does basic processing
def process_page(url, index):
    page = requests.get(url).text
    page = bs(page,'lxml')
    for e in page.find_all('br'):
        e.extract()
    print(page)
    page = page.find(nothing_special).contents[2:] 
    # Remove newline entries in list
    page = [i for i in page if i not in ('\n')] 
    return page

# Takes processed list of elements in page and processes/concatenates lyric lines together
def collect_title_lyrics(page):
    lyrics = ''
    # Enumerate list, remove carriage returns and newlines in remaining entries
    for index, verse in enumerate(page):
        page[index] = verse.replace('\r','').replace('\n','')
        if index == len(page) - 1:
            lyrics = lyrics + page[index]
        else:
            lyrics = lyrics + page[index] + '|-|'
    return lyrics

album_list = create_album_list(page)
# print(album_list)
df = pd.DataFrame(columns=['index','track','song','album','lyrics'])
# print(df)
# For each URL, process the page

i = 0 # song in album counter
j = 0 # absolute song counter
# for album, song_urls in album_list.items():
#     for song_url in song_urls:
#         page = process_page(song_url,i) # process current song
#         print(page)
        # lyrics = collect_lyrics(page) # collect lyrics on current page
        # df.loc[j] = [j,i,]
        # i = i + 1 # increment counter to go to next song
        
    # print(song_page)


a = process_page('The Boy Who Cried Wolf',1)

# print(a)
# print(collect_lyrics(a))

