目前，creamer已经初步具备提取功能，能正确分析大部分博客、资讯页面。

使用：

1,安装fann,http://leenissen.dk/fann/index.php?p=download.php, 及其python-bindings。

2,执行命令python creamer.py 。



---

设计思路：

1，分析网页的DOM，记录每一个标签名字、属性和文字。

2，计算每个标签的文字密度，据此判断该标签是否含有正文。

3，利用FANN(the Fast Artificial Neural Network Library)，对body中的标签进行初选。

4，用格拉布斯粗大誤差剔除法和其它过滤手段，对初选后的标签再过滤，最终确定网页正文。