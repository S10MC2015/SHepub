#Credits:
#https://stackoverflow.com/a/12657803 for venv advice
#https://realpython.com/beautiful-soup-web-scraper-python/#what-is-web-scraping for teaching me how to web scrape
#That guy on the python discord who helped me
#Another guy on python discord who helped me
#Thanks to fanficfare for inadvertantly teaching me what decompose does and i really wish i knew you existed before i started this lol.
#Also thank you to fanficfare as i used your stylesheet without permission please forgive me.
#https://stackoverflow.com/a/35156699 for venv.sh thing
#Also Thanks to Ghost and Ultra for the help.

#Import all the things that will be needed
import requests
import os
import bs4
import ebooklib
from ebooklib import epub
import datetime
import logging

#logging things to both treminal and file for some of the testing
logging.basicConfig(format='%(asctime)s %(message)s \n \n', filemode="w", filename = "latest.log",level=logging.DEBUG, datefmt='%d-%m-%Y %H:%M:%S')
logging.getLogger().addHandler(logging.StreamHandler())

logging.debug("Logging is enabled! \n \n")

#create the book variable
book = epub.EpubBook()

#function for current time
def gettime():
  time = datetime.datetime.now()
  gettime.timestr = time.strftime("%d-%m-%Y  %H:%M:%S")


#Declares authornote normal and chapter text normal and passes variables just in case.
annorm = ""
chpnorm = ""
passes = 0
chpcontent = []

#URL of SH story.
#URL = input("Please put in the URL of the story. Eg. https://www.scribblehub.com/series/14190/the-novels-redemption/ \n \n")
logging.debug("Auto URL to https://www.scribblehub.com/series/14190/the-novels-redemption/ to save dev time. \n Remove in release. \n \n")
URL = "https://www.scribblehub.com/series/14190/the-novels-redemption/"

#Requests the story startpage and stores the html code into startpage variable. Then uses BeautifulSoup to get the actual contents.
startpage = requests.get(URL)
sphtml = bs4.BeautifulSoup(startpage.text, 'lxml')

#gets current time with function and then logs it
gettime()
starttime = "Start Time of Scraping: %s" %(gettime.timestr)
logging.debug(starttime)

#Finds the element for author name then takes the text out of it.
storytitle = sphtml.find(class_='fic_title')
storytitle = storytitle.get_text()
print("\nStory Title: " + storytitle + "\n \n")

#Finds the element for author name then takes the text out of it.
authorname = sphtml.find(class_='auth_name_fic')
authorname = authorname.get_text()
print("Author: " + authorname + "\n \n")

#Finds the element for coverimage then takes the image source url out of it.
coverimage = sphtml.find(class_='fic_image')
coverimage = coverimage.find('img')['src']
print("CoverImage URL: " + coverimage + "\n \n")

latestchpupload = sphtml.find(class_='fic_date_pub')
latestchpupload = latestchpupload['title']
print("Latest Chapter Upload Time: " + latestchpupload + "\n \n")

#Finds element for synopsis then finds all text in the <p> tags. Then it adds then to the variable with line breaks.
synopsisraw = sphtml.find(class_='wi_fic_desc')
if synopsisraw == "":
  pass
else:
  synopsisrawp = synopsisraw.find_all('p')
  synopsis = ""
  for i in synopsisrawp:
    synopsis += i.get_text() + "\n \n"
  print("Synopsis: " + synopsis + "\n \n")

#Finds element for genre then finds all elements with <a> tag then takes all text out and adds comma+space. Next it adds an extra space to last one and replaces comma+space+space with a full stop.
genreraw = sphtml.find(class_='wi_fic_genre')
if genreraw == None:
  pass
else:
  genrerawp = genreraw.find_all('a')
  genre = ""
  for i in genrerawp:
    genre += i.get_text() + ", "
  genre += " "
  genre = genre.replace(",  ",".")
  print("Genre: " + genre + "\n \n")


#Finds element for tags then finds all elements with <a> tag then takes all text out and adds comma+space. Next it adds an extra space to last one and replaces comma+space+space with a full stop.
tagsraw = sphtml.find(class_='wi_fic_showtags_inner')
if tagsraw == None:
  pass
else:
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

#create book uid but i am an idiot.
bookid = URL
bookid = bookid.replace("https://","")
bookid = bookid.replace("http://","")
bookid = bookid.replace("www.scribblehub.com/read/","")
bookid = bookid.replace("www.scribblehub.com/series/","")
bookid = bookid.replace("/","")
bookid = bookid.replace("-","")
bookid = bookid.replace("_","")

#set some of the things for the book
book.set_identifier(bookid)
book.set_title(storytitle)
book.set_language('eng')
book.set_language('en')
book.add_author(authorname)
#book.set_cover(coverimage, open(coverimage, 'rb').read())
book.add_metadata('DC', 'description', synopsis)

#synopsisbook = bytes(synopsisraw.get_text(), 'utf-8')
#synopsisbook = synopsisraw.get_text()

#ch0fix = bs4.BeautifulSoup(b'<html><head><meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" /></head><body><h2>'+ storytitle +'</h2><h3> Details about the story.</h3><p>Created by: '+ authorname +'</p><p>Last Chapter Upload: '+ latestchpupload +'</p><p></p><p>Genre: '+ genre +'</p><p></p><p>Tags: '+ tags +'</p><p></p><p>Ebook made using SHepub.</p><p></p><p>Synopsis: '+ synopsisbook +'</p></body></html>')

#print(synopsisraw)
#exit()
synopsisbook = str(synopsisraw)

ch0fix = bs4.BeautifulSoup('<html><link href="stylesheet.css" type="text/css" rel="stylesheet"/><head><meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" /></head><body><h2>'+ storytitle +'</h2><h3> Details about the story.</h3><p>Created by: '+ authorname +'</p><p>Last Chapter Upload: '+ latestchpupload +'</p><p></p><p>Genre: '+ genre +'</p><p></p><p>Tags: '+ tags +'</p><p></p><p>Ebook made using SHepub.</p><p></p><p>Synopsis: '+ synopsisbook +'</p></body></html>', features="lxml")

#ch0fix = bs4.BeautifulSoup(b'<html><head><meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" /></head><body><h2>'+ bytes(storytitle, 'utf-8') +'</h2><h3> Details about the story.</h3><p>Created by: '+ bytes(authorname, 'utf-8') +'</p><p>Last Chapter Upload: '+ bytes(latestchpupload, 'utf-8') +'</p><p></p><p>Genre: '+ bytes(genre, 'utf-8') +'</p><p></p><p>Tags: '+ bytes(tags, 'utf-8') +'</p><p></p><p>Ebook made using SHepub.</p><p></p><p>Synopsis: '+ bytes(synopsisbook, 'utf-8') +'</p></body></html>')

ch0 = epub.EpubHtml(title='Details',
                   file_name='OEBPS/details.xhtml',
                   lang='en')

ch0fix = ch0fix.prettify()
ch0fix = ch0fix.replace("\n","")
ch0fix = ch0fix.replace("  ","")
ch0fix = ch0fix.replace("> <","><")
#print(ch0fix)
ch0.content = ch0fix
#logging.debug(ch0.content) # correct output
#ch0.set_content(ch0fix)
book.add_item(ch0)
#logging.debug(ch0.get_content()) # breaks
#print(ch0fix)
#print(ch0.get_content())
#exit()
style = 'body { font-family: Open Sans, Lato;}'#  background-color: #ffffff; text-align: justify; margin: 2%; adobe-hyphenate: none; } pre { font-size: x-small; } h1 { text-align: center; } h2 { text-align: center; } h3 { text-align: center; } h4 { text-align: center; } h5 { text-align: center; } h6 { text-align: center; } .CI { text-align:center; margin-top:0px; margin-bottom:0px; padding:0px; } .center {text-align: center;} .cover {text-align: center;} .full     {width: 100%; } .quarter  {width: 25%; } .smcap {font-variant: small-caps;} .u {text-decoration: underline;} .bold {font-weight: bold;} .big { font-size: larger; } .small { font-size: smaller; }'

default_css = epub.EpubItem(uid="style",
                        file_name="OEBPS/stylesheet.css",
                        media_type="text/css",
                        content=style)

book.add_item(default_css)

book.spine = [ch0]
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())
epub.write_epub('shepubtest.epub', book)
#exit() #for testing
URL = firstchpurl

def chpdata(URL,passes):

  passes += 1

  #Requests the chapter page and stores the html code into chapter variable. Then uses BeautifulSoup to get the actual contents.
  chapter = requests.get(URL)
  chphtml = bs4.BeautifulSoup(chapter.text, 'lxml')

  #make it faster by straining
  chphtml = chphtml.find(id="primary")

  #Finds the element for chapter title then takes the text out of it.
  chptitle = chphtml.find(class_='chapter-title')
  chptitle = chptitle.get_text()
  print("Chapter Title: " + chptitle + "\n \n")

  #exit()

  #Declares authornote normal and chapter text normal variables
  annorm = ""
  chpnorm = ""

  #Finds element for authornote then finds all elements with <a> tag then takes all text with element tags out.
  anraw = chphtml.find(class_='wi_authornotes_body')
  #if anraw == None:
  #  pass
  #else:
  #  anrawp = anraw.find_all('p')
  #  #Goes through the text with element tags and replaces tags with double new line and adds it to authornote normal variable
  #  for i in anrawp:
  #    annorm += i.get_text() + "\n \n"



  #Finds element for chaptertext then finds all elements with <p> tag then takes all text with element tags out. If it finds the authornotes elements inside, it will decompose them.
  chpraw = chphtml.find(id='chp_raw')
  if chpraw.find(class_='sp-wrap sp-wrap-default'):
    chpraw.find(class_='sp-wrap sp-wrap-default').decompose

  #chpraw = chpraw.prettify()

  if anraw == None:
    chpcontentsingle = ("%s" % (chpraw))
  else:
    #anraw = anraw.prettify
    chpcontentsingle = ("%s Author Notes: %s" % (chpraw, anraw))

  chpcontentsingle = chpcontentsingle.replace("\n","")
  chpcontentsingle = chpcontentsingle.replace("\'","")

  chpcontent.append(chpcontentsingle)
  #logging.debug(chpcontentsingle)
  print("logging.debug(chpcontentsingle) hs been disabled due to lag.")

  #logging.debug(chpcontent)
  #exit()
  #chprawp = chpraw.find_all('p')


  #Goes through the text with element tags and replaces tags with double new line and adds it to chapter text normal variable
  #for i in chprawp:
 #   chpnorm += i.get_text() + "\n \n"

  #The chapter contains the authornote normally so this uses the authornote we extracted and replaces it with nothingness in the chapter text
  #chpnorm = chpnorm.replace(annorm,"")


  #logging.debug("Chapter Text: " + chpnorm + "\n \n \n")
  #logging.debug("AuthorNote: " + annorm + "\n \n \n")

  #Finds element for the read button then finds the hyperlink url.
  nextchpurl = chphtml.find(class_='btn-wi btn-next')
  if nextchpurl == None:
    #ebookmake

    for i in range(len(chpcontent)):
      chpcontent[i].replace("\n", "")

    [i.strip() for i in chpcontent]
    list(map(str.strip,chpcontent))


    logging.debug(chpcontent)
    print("Passes: ", passes)
    chpcontentlen = len(chpcontent)
    print("This should be the same number as passes. \n chpcontent.len() = ", chpcontentlen)
    gettime()
    endtime = "End Time of Scraping: %s" %(gettime.timestr)
    logging.debug(endtime)
    exit()
  else:
    nextchpurl = nextchpurl['href']
    logging.debug("Next Chapter URL: " + nextchpurl + "\n \n \n \n")
#    if 'chapter' in globals():
#      del chapter
#    if 'chphtml' in globals():
#      del chphtml
#    if 'chptitle' in globals():
#      del chptitle
#    if 'chpraw' in globals():
#      del chpraw
#    if 'chprawp' in globals():
#      del chprawp
#    if 'chpnorm' in globals():
#      del chpnorm
#    if 'annorm' in globals():
#      del annorm
#    if 'anraw' in globals():
#      del anraw
#    if 'anrawp' in globals():
#      del anrawp
#    if 'l' in globals():
#      del l
    print("Passes: ", passes)
    chpdata(nextchpurl,passes)


chpdata(firstchpurl,passes)
