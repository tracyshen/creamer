#coding:utf-8
from urllib import urlopen
import pageparser,datamgr,sys


def get_cream(url):
	rawContent=datamgr.to_utf8(urlopen(url).read())
	pparser=pageparser.CreamParser()	
	pparser.feed(rawContent)
	#~ print 'url: ',url
	#~ print 'title: ',pageparser.spot.title
	#~ print 'keywords: ',pageparser.spot.keywords
	#~ print 'body data: ',pageparser.bdata
	pparser.get_cream()
	#~ print pageparser.cream
	

if __name__=='__main__':
	if len(sys.argv)>1:
		get_cream(sys.argv[1])
	else:
		url='http://house.focus.cn/showarticle/1911/572831.html'
		get_cream(url)
