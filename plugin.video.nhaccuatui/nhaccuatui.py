__author__ = 'traitravinh'
import urllib, urllib2, re, os, sys
import xbmc
import xbmcaddon,xbmcplugin,xbmcgui
from bs4 import BeautifulSoup

mysettings = xbmcaddon.Addon(id='plugin.video.nhaccuatui')
home = mysettings.getAddonInfo('path')
searchHistory = xbmc.translatePath(os.path.join(home,'history.txt'))
searchlink ='http://www.nhaccuatui.com/tim-kiem?q='
home_link = 'http://www.nhaccuatui.com/'
logo='http://stc.nct.nixcdn.com/static_v8/images/share/logo-nct.jpg'
pl=xbmc.PlayList(xbmc.PLAYLIST_MUSIC)

def Home():
    addDir('Search',searchlink,1,logo,'')

def SearchFirst(url):
    try:
        hist = open(searchHistory)
        addDir('Search',searchlink,2,logo,'')
        for text in hist:
            addDir(text,searchlink+text.replace(' ','+'),2,logo,'')
    except:pass

def Search(url):
    try:
        if url.find('+')!=-1:
            url = url.rstrip()
        else:
            keyb = xbmc.Keyboard('', 'Enter search text')
            keyb.doModal()
            if (keyb.isConfirmed()):
                    searchText = urllib.quote_plus(keyb.getText())
            url = "http://www.nhaccuatui.com/tim-kiem?q="+ searchText.replace(' ','+').rstrip()
            if searchText!='':
                with open(searchHistory,'a') as file:
                    file.write('\n'+searchText.replace('+',' '))

        index_search(url)
    except: pass


def index_search(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        search_control_select = soup('ul',{'class':'search_control_select'})
        li_soup = BeautifulSoup(str(search_control_select[0]))('a')
        for i in range(1,4):
            a_soup = BeautifulSoup(str(li_soup[i]))
            alink = a_soup('a')[0]['href']
            atitle = a_soup('a')[0]['title'].encode('utf-8')
            acount=a_soup('span')[0].contents[0]
            title = atitle + str(acount)
            addDir(title,alink,4,logo,atitle)
    except:pass

def search_return(url,cname):
    try:
        image = logo
        key = ''
        subkey =''
        if cname.find('B')!=-1:
            key='list_song'
            subkey = 'name_song'
        elif cname.find('P')!=-1:
            key = 'list_album'
            subkey = 'box_absolute'
        elif cname.find('V')!=-1:
            key = 'list_video'
            subkey = 'img'

        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        lists = soup('li',{'class':key})
        for l in lists:
            asoup = BeautifulSoup(str(l))
            alink = asoup('a',{'class':subkey})[0]['href']
            try:
                aimage = asoup('img')[0]['src']
                image = aimage
            except:pass
            atitle = asoup('a',{'class':subkey})[0]['title'].encode('utf-8')

            addDir(atitle,alink,5,image,cname)

        box_pageview = soup('div',{'class':'box_pageview'})
        pages = BeautifulSoup(str(box_pageview[0])).findAll('a')
        for p in pages:
            psoup = BeautifulSoup(str(p))
            plink = psoup('a')[0]['href']
            ptitle = psoup('a')[0].contents[0]

            addDir(ptitle.encode('utf-8'),plink,4,logo,cname)
    except:pass

def explore(url):
    try:
        xml_link = getXML(url)
        filelinks =[]
        filetitles =[]
        filelinks= getMediaLink(xml_link)
        filetitles = getMediaTitle(xml_link)
        filelinkslenght = len(filelinks)

        for i in range(0,filelinkslenght):
            addLink(filetitles[i],filelinks[i],6,iconimage,cname)
            i+=1
    except:pass

def getXML(url):
    try:
        link = urllib2.urlopen(url).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        flash_playing = soup('div',{'class':'box_playing'})
        file = re.compile('file=(.+?)" /').findall(str(flash_playing[0]))[0]
        return file
    except:pass

def getMediaLink(url):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','').replace('\n','')
        match = re.compile('<location>(.+?)</location>').findall(newlink)
        finallink=[]
        for content in match:
            finallink.append(content.replace('<![CDATA[','').replace(']]>','').replace(' ',''))
        return finallink
    except:pass

def getMediaTitle(url):
    try:
        link = urllib2.urlopen(url).read()
        newlink = ''.join(link.splitlines()).replace('\t','').replace('\n','')
        match = re.compile('<title>(.+?)</title>').findall(newlink)
        finaltitle=[]
        for content in match:
            finaltitle.append(content.replace('<![CDATA[','').replace(']]>',''))

        return finaltitle
    except:pass

def home():
    try:
        link = urllib2.urlopen(home_link).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        title_box_key = soup('div',{'class':'tile_box_key'})
        for t in title_box_key:
            tsoup = BeautifulSoup(str(t))
            title = BeautifulSoup(str(tsoup('h2')[0]))('a')[0].contents[0]
            link = BeautifulSoup(str(tsoup('h2')[0]))('a')[0]['href']

            print title
            print link

    except:pass

def index(url):
    try:
        link = urllib2.urlopen(home_link).read()
        soup = BeautifulSoup(link.decode('utf-8'))
        fram_select = soup('div',{'class':'fram_select'})
        info_album = BeautifulSoup(str(fram_select[3]))('div',{'class':'info_song'})
        for i in info_album:
            isoup = BeautifulSoup(str(i))
            ilink = isoup('a')[0]['href']
            ititle = isoup('a')[0]['title']

            print ilink
            print ititle.encode('utf-8')

        # box_pageview = soup('div',{'class':'box_pageview'})
        # pages = BeautifulSoup(str(box_pageview[0])).findAll('a')
        # for p in pages:
        #     psoup = BeautifulSoup(str(p))
        #     plink = psoup('a')[0]['href']
        #     ptitle = psoup('a')[0].contents[0]
        #
        #     print plink
        #     print ptitle


    except:pass

def Play(url):
    try:
        print 'CAME HERE====================>'
        print url
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_DVDPLAYER)
        xbmcPlayer.play(url)
    except:pass

def addDir(name,url,mode,iconimage,cname):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&cname="+urllib.quote_plus(cname)
    ok=True
    liz=xbmcgui.ListItem(name, iconImage=logo, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage,cname):
        # u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&cname="+urllib.quote_plus(cname)
        u = urllib.unquote_plus(url)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name})
        liz.setProperty('mimetype', 'video/x-msvideo')
        pl.add(url, liz)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder=False)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param

params=get_params()
url=None
name=None
mode=None
iconimage=None
cname=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        cname=urllib.unquote_plus(params["cname"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

sysarg=str(sys.argv[1])
if mode==None or url==None or len(url)<1:
    Home()
elif mode==1:
    SearchFirst(url)
elif mode==2:
    Search(url)
elif mode==3:
    index_search(url)
elif mode==4:
    search_return(url,cname)
elif mode==5:
    explore(url)
elif mode==6:
    Play(url)

xbmcplugin.endOfDirectory(int(sysarg))
