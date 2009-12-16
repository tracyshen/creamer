#coding:utf-8
from os import path
from types import *
import chardet
class Spot(object):
	def __init__(self,url,title='',keywords='',timestamp='',literal=''):
		self.url=url
		self.title=title
		self.keywords=keywords
		self.literal=literal
		self.timestamp=timestamp
		self.scream=None
		
	def set_scream(self,scream):
		self.scream=scream
	#~ def __str__(self):
		#~ return self.url
	#~ def __eq__(self,item):
		#~ return self.url==str(item).lower()
		
class CaselessDict(dict):

    def __init__(self, mapping=None):
        if mapping:
            if type(mapping) is dict:
                for k,v in d.items():
                    self.__setitem__(k, v)
            elif type(mapping) in (list, tuple):
                d = dict(mapping)
                for k,v in d.items():
                    self.__setitem__(k, v)
                    
        # super(CaselessDict, self).__init__(d)
        
    def __setitem__(self, name, value):

        if type(name) in StringTypes:
            super(CaselessDict, self).__setitem__(name.lower(), value)
        else:
            super(CaselessDict, self).__setitem__(name, value)

    def __getitem__(self, name):
        if type(name) in StringTypes:
            return super(CaselessDict, self).__getitem__(name.lower())
        else:
            return super(CaselessDict, self).__getitem__(name)

    def __copy__(self):
        pass
	
def to_utf8(data,sencoding=None):
    if sencoding:
	try:
	    return data.decode(sencoding).encode('utf-8')
	except Exception,e:
	    pass
	    
    try:
	return data.decode('GBK18030').encode('utf-8')
    except Exception,e:
	try:
	    return data.decode('GBK').encode('utf-8')
	except Exception,e:		
	    try:
		sencoding=chardet.detect(data)['encoding']
		return data.decode(sencoding).encode('utf-8')
	    except Exception,e:
		return data
	
