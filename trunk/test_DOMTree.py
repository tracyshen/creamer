#coding:utf-8
import pageparser,datamgr
from pytidy import pytidy

url='http://blog.qq.com/qzone/41533848/1260352786.htm'
spotObj=datamgr.Spot(url)

rawContent="""<body>
<p>
<p>　　<B>保障性住房缘何多是非</B>
<p>
<p>　　保障性住房是指政府为中低收入住房困难家庭所提供的限定标准、限定价格或租金的住房，由廉租住房、经济适用住房和政策性租赁住房构成。自从保障性住房推出之后，一直是非不断，以丑闻居多。
<p>
<p>　　最近，武汉经适房“六连号”、郑州“经适房建别墅事件”等案例暴露出了保障性住房制度上的漏洞，更重要的是将政府执行部门的公信度降低到了极点。许多经济适用房被不符合条件的人占有，成为一些人合法吞噬低收入者福利的一种途径。经济适用房作为一种公共福利，是政府兴建、政府分配，政府成为直接主体，经济适用房的分配不公，使许多真正的中低收入者对于购置保障性住房失去了希望，社会影响极坏。
<p>

<p>　　造成这样丑闻的原因主要是由于保障性住房的资源过于紧张，中低收入者庞大的需求量与紧张的房源之间不成比例，加之保障性住房的价格与市场上普通的商品房之间价格也有着较大的差异，这就使一些有着“投机思想”和“特权主义”的人费尽心思去徇私舞弊。
<p>
<p>　　<B>保障性住房成“鸡肋”房</B>
</body>
"""
pageparser=pageparser.HMSGMLOpParser(spotObj)	
pageparser.feed(rawContent)
pageparser.get_cream()

#~ print pytidy.fix("<br/>")
for rectag in pageparser.domTree:
	print rectag.tag,': '
	print '   parent: ',rectag.parent
	print '  preSibling: ',rectag.preSibling
	print '   nextSibling: ',rectag.nextSibling
	print '   children: ',[child.tag for child in pageparser.domTree.get_children(rectag)]
	print '   siblings: ',[sibling.tag for sibling in pageparser.domTree.get_siblings(rectag)]
	print '   data: ',rectag.data,len(rectag.data)
	print '  density: ',rectag.density

