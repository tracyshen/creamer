import math
GrubbsRatio={3:[1.15,1.16],
			4:[1.46,1.49],
			5:[1.67,1.75],
			6:[1.82,1.94],
			7:[1.94,2.10],
			8:[2.03,2.22],
			9:[2.11,2.32],
			10:[2.18,2.41],
			11:[2.23,2.48],
			12:[2.28,2.55],
			13:[2.33,2.61],
			14:[2.37,2.66],
			15:[2.41,2.70],
			16:[2.44,2.75],
			17:[2.48,2.78],
			18:[2.50,2.82],
			19:[2.53,2.85],
			20:[2.56,2.88],
			21:[2.58,2.91],
			22:[2.60,2.94],
			23:[2.62,2.96],
			24:[2.64,2.99],
			25:[2.66,3.01],
			#the following data were not ganranteed to be true:
			26:[2.68,3.03],
			27:[2.70,3.05],
			28:[2.72,3.07],
			29:[2.73,3.09],
			30:[2.74,3.10],
			}

def grubb_eleminate_outliers(rawList,a=0.05):
	if a==0.05:
		idx=0
	else:
		idx=1
	count=len(rawList)
	if count<=2 or count>30:
		return rawList
	ave=average(rawList)
	variance=get_variance(rawList,ave)
	newList=[]
	for i in rawList:
		if math.fabs((ave-i)/float(variance))<GrubbsRatio[count][idx]:
			newList.append(i)
	return newList
	
def get_variance(inList,ave):
	sum=0
	for i in inList:
		var=i-ave
		sum+=var*var
	num=len(inList)
	if num>1:
		return math.sqrt(sum/float(num-1))
	return None
	
def average(inList):
	sum=0
	for i in inList:
		sum+=i
	num=len(inList)
	if num>0:
		return sum/float(num)
	return None















