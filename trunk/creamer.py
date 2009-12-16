#coding:utf-8
from urllib import urlopen
import pageparser,datamgr

url='http://house.focus.cn/showarticle/1911/572831.html'
rawContent=datamgr.to_utf8(urlopen(url).read())
pageparser=pageparser.CreamParser()	
pageparser.feed(rawContent)
#~ print 'url: ',url
#~ print 'title: ',pageparser.spot.title
#~ print 'keywords: ',pageparser.spot.keywords
#~ print 'body data: ',pageparser.bdata
pageparser.get_cream()
#~ print pageparser.cream
