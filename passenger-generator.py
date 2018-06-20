from bs4 import BeautifulSoup  as bs
from textgenrnn import textgenrnn as tg # takes quite a while to process due to (I believe) setting up tensorflow
import requests
import pandas as pd
import re

# response = requests.get('https://www.azlyrics.com/p/passenger.html')
# page = response.text
# page = bs(page, "lxml")
# page.prettify()
# print(page)
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
def process_page(url, index): # Needs to be modified to return song title as well for insertion in dataframe
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

# album_list = create_album_list(page)

# It was at this point that I was banned from retrieving lyrics from azlyrics.com
df = pd.DataFrame(columns=['track','album','song','lyrics'])

lyrics_temp = ["Here's a simple song|-|Won't stop the rain from coming down|-|Or your heart from breaking|-|Here's a simple song|-|It's never gonna turn this day around|-|Stop the earth from shaking|-|It's just a simple song|-|Nothing right or wrong|-|You can sing along if you want to|-|Well, I know it's not bein' easy|-|But easy ain't worth singin' about|-|Yeah, I know, I know|-|The time goes slow|-|But it always running out|-|Here's a simple song|-|Won't stop the rain from coming down|-|Or your heart from breaking|-|Here's a simple song|-|It's never gonna turn this day around|-|Stop the earth from shaking|-|It is just a simple song|-|Nothing right or wrong|-|You can sing along if you want to|-|Well, I know it's far from simple|-|But simple ain't worth worryin' about|-|Yeah, I know, I know|-|It's time to go|-|I think I keep on finding|-|Everything seems to be about timing|-|Here's a simple song|-|Won't stop the rain from coming down|-|Or your heart from breaking|-|Just a simple song|-|Never gonna turn this day around|-|Stop the earth from shaking|-|It's just a simple song|-|Nothing right or wrong|-|You can sing along if you want to|-|Whoa-oh-oh, it's just a simple song|-|Nothing right or wrong|-|You can sing along if you want to",
"I've only known her for a while|-|And she came as some surprise|-|I see the sunshine when she smiles|-|I feel the rain fall when she cries|-|She hits me in the heart|-|She drops me to my knees|-|And I don't know where I'd be without you|-|Sweet Louise|-|Oh, well she flies just like a bird|-|And she floats just like a dream|-|And she's the sweetest song I've heard|-|And the sweetest face I've seen|-|And she hits me in the heart|-|And she drops me to my knees|-|I don't know where I'd be without you|-|My sweet Louise|-|They say patience is a virtue|-|Yeah she wait, she won't desert you|-|She's got hands that couldn't hurt you if they tried|-|With all that happiness she has|-|Well she loves and understands me|-|But oh Lord I know she's always by my side|-|So if you please put me at ease|-|My sweet Louise|-|And she hits me in the heart|-|Oh and she drops me to my knees|-|I don't know know everything about you|-|Yeah but you give me no reason to doubt you|-|And I don't wanna be without you|-|Sweet Louise",
"Well, I am the boy who cried wolf|-|And I know I've lied in the past|-|But last night I saw his yellow eyes shining in the dark|-|Yeah, I know I spun tales with his voice|-|And I open my mouth too fast|-|But last night I saw his footprints in the path|-|Well, I could swim every sea from south pole to north|-|But I know I'll only ever be the boy who cried wolf|-|Well, I am the shepherd's only son|-|And I know what a joke I've become|-|I have an honest heart but I have lies on my tongue|-|I don't know how it started or where it came from|-|And you have no reason and I have no proof|-|But this time I swear, I'm telling the truth|-|I saw that old wolf, from tail to tooth|-|And I know that he's hungry and he's coming down too|-|Well, I could swim every sea from south pole to north|-|And I could climb every tree and scale every course|-|And I could share only the truth from this day forth|-|But I know I'll only ever be the boy who cried wolf|-|Oh, oh, I am the boy who cried wolf|-|Oh, oh, I am the boy who cried",
"When I built these walls with bricks and stones|-|I built them all around|-|I built these walls a long time ago|-|She ain't gonna take 'em down|-|No, she ain't gonna break 'em down|-|I built these walls with my two hands|-|I laid every single part|-|And behind these walls a coward stands|-|An eagle and a broken heart|-|An eagle and a broken heart|-|Oh-oh-oh-oh-oh, she comes around|-|See if I don't get lost|-|I won't get found|-|Oh-oh-oh.oh, and turn it 'round|-|See if I don't go up|-|I won't come down|-|I won't come down|-|When I built these walls around my chest|-|I built them thick and strong|-|Oh, and she can try her very best|-|But they've been here for too long|-|For long ago there was a girl|-|That stood there where she stands|-|But she reached right in into my heart|-|And broke it in her hands|-|Oh, she broke it in her hands|-|Oh-oh-oh-oh, and I suppose|-|If there's no rain of clouds|-|Nothing grows|-|Oh-oh-oh, but this I know|-|If I don't get high|-|I won't get low|-|Oh-oh-oh, and I find her strange|-|She wants to climb up|-|But she could fall|-|Oh-oh-oh, she said: I won't change|-|And I live and die|-|Behind these walls|-|Behind these walls|-|Behind these walls",
"Well, I walked out this evening|-|Stood out in front of my house|-|To see the daylight leaving|-|My eyes pointed south|-|I felt like I was dreaming|-|I'd never seen the sky so red|-|Gave me the strangest feeling|-|And a voice inside me said|-|All my life I've been chasing setting suns|-|See me running up the hill when the evening comes|-|They get further away the faster that I run|-|I'm getting old and tired of chasing setting suns|-|Walked down to the ocean|-|And sat on the cold hard stones|-|Saw the seabirds fishing and the sunlight glistening|-|Down on my English home|-|Thought back to all the things I've seen|-|The people I know and the places I've been|-|The city skylines and the fields of green|-|It's a wonder I made it home|-|All my life I've been chasing setting suns|-|See me running up the hill when the evening comes|-|They get further away the faster that I run|-|I'm getting old and tired of chasing setting suns|-|Well, all my life I've been chasing setting suns|-|See me running up the hill when the evening comes|-|They get further away the faster that I run|-|I'm getting old and tired of chasing setting suns|-|I'm getting old and tired of chasing setting suns|-|Oh, and I'm getting old and tired of chasing setting suns",
"She's a whistle on the wind|-|A feather on the breeze|-|A ripple on the stream|-|She is sunlight on the sea|-|She's a soft summer rain|-|Falling gently through the trees|-|And I love her|-|She's cunning as a fox|-|Clever as a crow|-|Solid as a rock|-|She is stubborn as a stone|-|She's a hardheaded woman|-|And the best one that I know|-|And I love her|-|Yeah, well I love her|-|She's as new as the springtime|-|Strong as autumn blows|-|Warm as the summer|-|And soft as the snow|-|She's a thousand miles from here|-|But she's everywhere I go|-|'Cause I love her|-|She loves me like a woman|-|She looks like a lady|-|She laughs like a child|-|And cries like a baby|-|I think that maybe she's the one that's gonna save me",
"There's somewhere I'd cross the sea|-|In a land that's lost and free|-|With my darling close to me|-|At least where I'm supposed to be|-|We're somewhere on the ocean breeze|-|And around the swinging trees|-|You're the only one for me|-|That is where I long to be|-|Someday|-|Someday yeah, yeah, yeah, yeah|-|You're somewhere out upon the beach|-|Out of range and out of reach|-|With the truest love of mine|-|Underneath the bluest sky|-|Yeah, far away from any time|-|We'll watch the lazy sun go down|-|With my sweetheart I lay down|-|That is where I will be found|-|Someday|-|Someday yeah, yeah, yeah, yeah",
"Well, the past is the past, the future is not yet|-|The dye has been cast though the paint’s no longer wet|-|If you’re willing to forgive then maybe one day you’ll forget|-|Darling, ain’t that worth a try?|-|Ain’t it worth a try when|-|Yesterday’s gone and tomorrow is not here|-|The days they are longer, how they quickly disappear|-|If you learn to move on that’s when the pathway becomes clear|-|Darling, ain’t that worth a try?|-|Ain’t it worth a try to see black from blue|-|Perhaps it’s just a point of view|-|And maybe this one’s down to you, my friend|-|In the end|-|For these moments that have gone, the summer’s still to be|-|And every day that’s past, it’s just a raindrop on the sea|-|If you learn to let go maybe one day you’ll be free|-|Baby, ain’t that worth a try?|-|Ain’t it worth a try to see black from blue|-|Perhaps it’s just a point of view|-|Or maybe this one’s down to you, my friend|-|Do you see grey from green?|-|Or all the colors in between?|-|But maybe this is just a dream, my friend|-|In the end",
"Claps of thunder and bolts of lightning|-|Wind comes howling through|-|Sometimes love is just a kite string|-|And a heart shaped at two|-|And holding on can be so frightening|-|I know she’s frightened too|-|But I’ll go dancing out in the thunder and lightning|-|If she will too|-|If she tells me she will too",
"Be a lantern burning|-|Never gonna go out|-|The winds are turning|-|Never gonna blow out|-|I've had a life of learning|-|I know people come and go|-|Be a lantern burning|-|Your fire is burning|-|Be my lighthouse shining|-|Went out on the sea|-|Be my silver lining|-|Be my golden key|-|I've had a life of climbing|-|Don't let me fall from the trees|-|Be my lighthouse shining|-|When I'm out on the sea|-|Oh-oh-oh-oh, oh-oh-oh, oh-oh-oh|-|Oh-oh-oh, oh-oh|-|Oh-oh-oh-oh, oh-oh-oh, oh-oh-oh|-|Oh-oh-oh, oh-oh|-|Oh-oh-oh-oh, oh-oh-oh, oh-oh-oh|-|Oh-oh-oh, oh-oh|-|Oh-oh-oh-oh, oh-oh-oh, oh-oh-oh|-|Oh-oh-oh, oh-oh|-|Oh-oh-oh-oh, oh-oh-oh, oh-oh-oh|-|Oh-oh-oh, oh-oh|-|Oh-oh-oh-oh, oh-oh-oh, oh-oh-oh"]

album_temp ='The Boy Who Cried Wolf'
song_temp = ["Simple Song","Sweet Louise","The Boy Who Cried Wolf","Walls","Setting Suns","And I Love Her","Someday","In The End","Thunder and Lightning","Lanterns"]

# # Save test album
# i = 1 # song in album counter
# j = 0 # absolute song counter
# for song in song_temp:
#     df.loc[j] = [i,album_temp,song_temp[j], lyrics_temp[j]]
#     i = i + 1
#     j = j + 1
# print(df)
# df.to_csv("passenger-df.csv",sep=",", encoding='utf-8')

# For each URL, process the page
# for album, song_urls in album_list.items():
#     for song_url in song_urls:
#         page = process_page(song_url,i) # process current song
#         print(page)
        # lyrics = collect_lyrics(page) # collect lyrics on current page
        # df.loc[j] = [j,i,]
        # i = i + 1 # increment counter to go to next song
        
# songs = pd.read_csv('passenger-df.csv')
# print(songs)

# # Generate examples: saved in passenger-generated-examples
textgen = tg()
textgen.train_from_file('passenger-tgr.txt',num_epochs=10)
examples = textgen.generate(5)

