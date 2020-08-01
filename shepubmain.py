#Import all the things that will be needed
import requests
import os
import bs4
import ebooklib

#URL of SH story.
URL = 'https://www.scribblehub.com/read/14190-the-novels-redemption/'

#Requests the story startpage and stores the html code into startpage variable. Then uses BeautifulSoup to get the actual contents.
startpage = requests.get(URL)
sphtml = bs4.BeautifulSoup(startpage.content, 'html.parser')

#Finds the element for author name then takes the text out of it.
authorname = sphtml.find(class_='auth_name_fic')
authorname = authorname.get_text()
print("Author: " + authorname + "\n \n")

#Finds the element for coverimage then takes the image source url out of it.
coverimage = sphtml.find(class_='fic_image')
coverimage = coverimage.find('img')['src']
print("CoverImage URL: " + coverimage + "\n \n")

#Finds element for synopsis then finds all text in the <p> tags. Then it adds then to the variable with line breaks.
synopsisraw = sphtml.find(class_='wi_fic_desc')
synopsisrawp = synopsisraw.find_all('p')
synopsis = ""
for i in synopsisrawp:
  synopsis += i.get_text() + "\n \n"
print("Synopsis: " + synopsis + "\n \n")

#Finds element for genre then finds all elements with <a> tag then takes all text out and adds comma+space. Next it adds an extra space to last one and replaces comma+space+space with a full stop.
genreraw = sphtml.find(class_='wi_fic_genre')
genrerawp = genreraw.find_all('a')
genre = ""
for i in genrerawp:
  genre += i.get_text() + ", "
genre += " "
genre = genre.replace(",  ",".")
print("Genre: " + genre + "\n \n")

#Finds element for tags then finds all elements with <a> tag then takes all text out and adds comma+space. Next it adds an extra space to last one and replaces comma+space+space with a full stop.
tagsraw = sphtml.find(class_='wi_fic_showtags_inner')
tagsrawp = tagsraw.find_all('a')
tags = ""
for i in tagsrawp:
  tags += i.get_text() + ", "
tags += " "
tags = tags.replace(",  ",".")
print("Tags: " + tags + "\n \n")

#Finds element for the read button then finds the hyperlink url.
firstchpurl = sphtml.find(class_='read_buttons')
firstchpurl = firstchpurl.find('a')['href']
print("First Chapter URL: " + firstchpurl + "\n \n")

#exit()


#URL of chapter.
URL = 'https://www.scribblehub.com/read/14190-the-novels-redemption/chapter/149818/'

#Requests the chapter page and stores the html code into chapter variable. Then uses BeautifulSoup to get the actual contents.
chapter = requests.get(URL)
chphtml = bs4.BeautifulSoup(chapter.content, 'html.parser')

#Finds the element for chapter title then takes the text out of it.
chptitle = chphtml.find(class_='chapter-title')
chptitle = chptitle.get_text()
print("Chapter Title: " + chptitle + "\n \n")

#exit()

#Finds element for chaptertext then finds all elements with <a> tag then takes all text with element tags out.
chpraw = chphtml.find(id='chp_raw')
chprawp = chpraw.find_all('p')

#Finds element for authornote then finds all elements with <a> tag then takes all text with element tags out.
anraw = chphtml.find(class_='wi_authornotes_body')
anrawp = anraw.find_all('p')

#Declares authornote normal and chapter text normal variables
annorm = ""
chpnorm = ""

#Goes through the text with element tags and replaces tags with double new line and adds it to chapter text normal variable
for i in chprawp:
  chpnorm += i.get_text() + "\n \n"

#Goes through the text with element tags and replaces tags with double new line and adds it to authornote normal variable
for i in anrawp:
  annorm += i.get_text() + "\n \n"

#The chapter contains the authornote normally so this uses the authornote we extracted and replaces it with nothingness in the chapter text
chpnorm = chpnorm.replace(annorm,"")


print("Chapter Text: " + chpnorm + "\n \n \n")
print("AuthorNote: " + annorm + "\n \n \n")