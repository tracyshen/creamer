# -- coding: utf-8
from sgmllib import SGMLParser
import fann,grubbs

class ParseTag(object):
    """ Class representing a tag which is parsed by the HTML parser(s) """
    
    def __init__(self, tag, elmlist, enabled=True ,init=False):
        self.tag = tag
        self.elmlist = elmlist
        self.enabled = enabled
        self.init = init

    def disable(self):
        """ Disable parsing of this tag """
        self.enabled = False

    def enable(self):
        """ Enable parsing of this tag """
        self.enabled = True

    def isEnabled(self):
        """ Is this tag enabled ? """
        return self.enabled
	
    def __eq__(self,tag):
	return self.tag.lower()==tag.lower()


class RecordTag(object):
    
    def __init__(self,tag,attrs,inme=True):
	self.tag=tag
	self.attrs=attrs
	self.inMe=inme
	self.data=''
	self.parent=None
	self.preSibling=None
	self.nextSibling=None
	self.density=0
	self.children=[]
	
    def calculate_density(self):
	try:
	    total=0.0
	    for key,value in self.attrs:
		total+=len(key)+len(value)+1
	    total+=len(self.tag)*2+5 #5=len('<>')+len('</>')
	    dataLen=len(self.data)
	    self.density=dataLen/float(dataLen+total)
	except Exception,e:
	    print e

    def set_in_me(self,inme):
	self.inMe=inme
	
    def still_in_me(self):
	return self.inMe
	
    def add_data(self,data):
	self.data+=data
    	
    def __str__(self):
	return self.tag

class DOMTree(list):
    def __init__(self):
	"lastRecTag : the last closed tag"
	self.lastClosedRecTag=None  
	self.lastOpenRecTag=None
	self.curTag=None
	self.omitTags=['font','br','strong','b']
	
    def get_siblings(self,recTag):
	if recTag:
	    return [tag for tag in self.get_children(recTag.parent) if tag!=recTag]
	return []
	
    def get_children(self,recTag):
	if recTag:
	    return recTag.children
	return []

    def get_last_open_tag(self):
	try:   
	    idx=-1
	    while not self[idx].still_in_me():
		idx-=1		    
	    self.lastOpenRecTag=self[idx]
	except IndexError:
	    pass
	
    def start_tag(self,tag,attrs):
	if tag in self.omitTags:
	    return 
	self.get_last_open_tag()
	self.curTag=RecordTag(tag,attrs)
	try:
	    preTag=self[-1]
	    self.curTag.parent=self.lastOpenRecTag
	    self.lastOpenRecTag.children.append(self.curTag)
	    if not preTag.still_in_me():
		self.curTag.preSibling=self.lastClosedRecTag
		self.lastClosedRecTag.nextSibling=self.curTag	
	except (AttributeError,IndexError):
	    pass
	self.append(self.curTag)	    

    def get_last_closed_tag(self):
	try:
	    idx=-1
	    while not self[idx].still_in_me():
		idx-=1
	    self.lastClosedRecTag=self[idx]  
	except IndexError:
	    pass

    def end_tag(self,tag):
	if tag in self.omitTags:
	    return 
	self.get_last_closed_tag()
	self.lastClosedRecTag.set_in_me(False)
	self.lastClosedRecTag.calculate_density()	    
	
    def handle_data(self,data):
	self.get_last_open_tag()
	data=data.strip()
	try:
	    #~ print '  handle data: ',data.strip(),' curTag:',self.curTag,' lastOpenTag: ',self.lastOpenRecTag # self.lastOpenRecTag,' ', self.lastClosedRecTag
	    if self.curTag.still_in_me():
		self.curTag.add_data(data)
	    else:
		self.lastOpenRecTag.add_data(data)
	except AttributeError:
	    pass    
	    
class SimpleParser(SGMLParser):
    features = [ ParseTag('a', ['href']),
                 ParseTag('link', ['href']),
                 ParseTag('body', []),
		 ParseTag('title',[]),
		 ParseTag('script',[]),
		 ParseTag('style',[]),
                 ParseTag('meta', ['CONTENT', 'content',]),
	      ]
    def __init__(self):
	self.cream=''
	self.domTree=DOMTree()
	self.ann=fann.NeuNet()
	self.ann.create_from_file("cream.net")
  
    def unknown_starttag(self, tag, attrs):
        if tag in self.features:
	    parsetag = self.features[self.features.index(tag)]
	    parsetag.init=True
	self.domTree.start_tag(tag,attrs)
	    
    def unknown_endtag(self, tag): 
	if tag in self.features:
	    parsetag=self.features[self.features.index(tag)]
	    parsetag.init=False
	self.domTree.end_tag(tag)

    def handle_data(self, data):
	if not self.features[self.features.index('style')].init \
	    and not self.features[self.features.index('script')].init:
	    self.domTree.handle_data(data)

    def get_cream(self):
	idx=0
	bodyIdx=0
	for rtag in self.domTree:
	    if rtag.tag=='body':
		bodyIdx=idx
		break
	    idx+=1
	candidates={}
	pos=0
	for rtag in self.domTree[bodyIdx+1:]:
	    pos+=1
	    if rtag.tag in ['textarea']:
		continue
	    ownDensity=rtag.density
	    if rtag.preSibling:
		preDensity=rtag.preSibling.density
		if preDensity==0.0 and rtag.preSibling.preSibling:
		    preDensity=rtag.preSibling.preSibling.density
	    else:
		preDensity=0.0
	    if rtag.nextSibling:
		nextDensity=rtag.nextSibling.density
		if nextDensity==0.0 and rtag.nextSibling.nextSibling:
		    nextDensity=rtag.nextSibling.nextSibling.density
	    else:
		nextDensity=0.0
	    # Load the data we described above.
	    calc_out=self.ann.run([len(rtag.data),ownDensity,preDensity,nextDensity])
	    if calc_out[0]>0:
		candidates[pos]=rtag
		#~ print rtag.tag,' ',calc_out[0],' ',pos,' len:',len(rtag.data),' ',ownDensity,' ',preDensity,' ',nextDensity
	#~ print "==============================="
	#eleminate the tag that is far away from most of the tags
	validTagKeys=grubbs.grubb_eleminate_outliers(candidates.keys())
	validTagKeys.sort()
	for key in validTagKeys:
		print candidates[key].tag,' ',key,' ',candidates[key].data
	
    def reset(self):
        SGMLParser.reset(self)
	
class CreamParser(SimpleParser):
    """ A parser based on effbot's sgmlop """

    def __init__(self):
        # This module should be built already!
        import sgmlop
        self.parser = sgmlop.SGMLParser()
        self.parser.register(self)
        SimpleParser.__init__(self)
        
    def finish_starttag(self, tag, attrs):
        self.unknown_starttag(tag, attrs)

    def finish_endtag(self, tag):
        self.unknown_endtag(tag)        

    def feed(self, data):
        self.parser.feed(data)
