from bs4 import BeautifulSoup  as bs
#from textgenrnn import textgenrnn as tg # takes quite a while to process due to (I believe) setting up tensorflow
import requests

response = requests.get('https://www.azlyrics.com/p/passenger.html')
page = response.text
page = bs(page, "lxml")
page.prettify()
page.find_
# print (song_list)

# song_list_txt = open("page","w")
# song_list_txt.write(response.text)

# By inspection the page actually just maintains lists of values as a variable and subs them in when rendering

# print (page.find('div', {"id": "listAlbum"}))
albums = page.find('div', id="listAlbum")
# albums = albums.findAll('a', href=True)
# print (albums) 


album_list = {}
a = ''
for s in albums.find_all():
    if s.name == 'div':
        if s.find_next('b') != None:
            a = s.find_next('b').contents[0].replace('"','') # Extract first element of returned list object
        else:
            a = s.contents[0].replace('"','').replace(':','')
        
        album_list[a] = []
        print(a)

    elif s.name == 'a' and 'href' in s.attrs:
        n = s['href'].replace('..','')
        album_list[a].append(n)
        print(n)

print(album_list)
