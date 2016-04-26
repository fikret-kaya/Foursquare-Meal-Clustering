import json
import collections, re
import math

class Word:

	mutual_info = 0

	def __init__(self, value, count, pos_count, neg_count):
		self.value = value
		self.count = count
		self.pos_count = pos_count
		self.neg_count = neg_count

	def set_mutual_info(self, mutual_info):
		self.mutual_info = mutual_info


# Data folders
labelled_data = "labelled data/"
cleaned_data = "cleaned data/"

# Constants
separation_words = 20

# Menu sets
burgerking_menu = []
cookshop_menu = []
liva_menu = []
mado_menu = []
mcdonalds_menu = []
ozsut_menu = []
ilforno_menu = []
quickchina_menu = []
aspava_menu = []
zigane_menu = []

comments = set()
positive_comments = set()
negative_comments = set()

# File list
files = ['BurgerKing.json','Cookshop.json','LivaBistro.json','Mado.json','McDonalds.json','Ozsut.json',
		 'PizzaIllForno.json','QuickChina.json','YıldızAspavaLabeled.json','ZiganePideLabeled.json']

# Reads file and return the data of the file
def readfile(filename, dir):
	with open(dir + filename, encoding="utf8", errors="ignore") as jsonfile:
		data = json.load(jsonfile)
		return data

# Gets file's data and add them to general menu
def setmenu(data, menu):
	for i in range(len(data['tips'])):
		comments.add(data['tips'][i]['comment'])
		for j in data['tips'][i]['food+']:
			positive_comments.add(data['tips'][i]['comment'])
			if j not in menu:
				menu.append(j)
		for k in data['tips'][i]['food-']:
			if k not in menu:
				menu.append(k)
			negative_comments.add(data['tips'][i]['comment'])

def group_menu(menu):
	loop_range = range(len(menu))
	for i in loop_range:
		menu.append([])

def add_alternative_names(allData, allMenus, words, comments):
	separatedComments = []
	mi_pre = []
	for i in range(0,len(allMenus)):
		mi_pre.append([])
		separatedComments.append([])
		for j in range(0,len(allMenus[i])//2):
			mi_pre[i].append([])
			separatedComments[i].append([])
			for k in range(len(words)):
				w = Word(words[k],1,1,1)
				mi_pre[i][j].append(w)
		for j in range(0,len(allMenus[i])//2):
			for k in range(len(allData[i]['tips'])):
				for l in allData[i]['tips'][k]['food+']:
					if (l == allMenus[i][j]):
						separatedComments[i][j].append(allData[i]['tips'][k]['comment'].split())
						for m in allData[i]['tips'][k]['comment'].split():
							if ( m in words):
								mi_pre[i][j][words.index(m)].pos_count += 1
								mi_pre[i][j][words.index(m)].count += 1
								for n in range(0,len(allMenus[i])//2):
									if (n != j):
										mi_pre[i][n][words.index(m)].neg_count += 1
										mi_pre[i][n][words.index(m)].count += 1
				for l in allData[i]['tips'][k]['food-']:
					if ( l == allMenus[i][j]):
						separatedComments[i][j].append(allData[i]['tips'][k]['comment'].split())
						for m in allData[i]['tips'][k]['comment'].split():
							if ( m in words):
								mi_pre[i][j][words.index(m)].pos_count += 1
								mi_pre[i][j][words.index(m)].count += 1
								for n in range(0,len(allMenus[i])//2):
									if (n != j):
										mi_pre[i][n][words.index(m)].neg_count += 1
										mi_pre[i][n][words.index(m)].count += 1
		for j in range(0,len(allMenus[i])//2):
			total_count = 0
			total_pos_count = 0
			total_neg_count = 0
			for k in range(len(words)):
				total_count += mi_pre[i][j][k].count
				total_pos_count += mi_pre[i][j][k].pos_count
				total_neg_count += mi_pre[i][j][k].neg_count
			temp_info = 0
			for k in range(len(words)):
				temp_info = (mi_pre[i][j][k].pos_count/total_count)*math.log((total_count*mi_pre[i][j][k].pos_count)/(mi_pre[i][j][k].count*total_pos_count),2)
				temp_info = ((total_neg_count-mi_pre[i][j][k].neg_count)/total_count)*math.log((total_count*(total_neg_count-mi_pre[i][j][k].neg_count))/((total_count-mi_pre[i][j][k].count)*total_neg_count),2)
				mi_pre[i][j][k].mutual_info = temp_info
			mi_pre[i][j].sort(key=lambda a: a.mutual_info, reverse=True)
			index_var = 0
			while( len(separatedComments[i][j])>0 and index_var < 20):
				allMenus[i][len(allMenus[i])//2+j].append(mi_pre[i][j][0].value);
				separatedComments[i][j][:] = [a for a in separatedComments[i][j] if mi_pre[i][j][0].value not in a]
				mi_pre[i][j][:] = mi_pre[i][j][1:]
				index_var +=1
			print(i,j,allMenus[i][j],allMenus[i][len(allMenus[i])//2+j])

# region ERRORZZZZ Buraya Bakarlar !!!
# Mado.json da \" kullanildigi icin hata veriyor, simdilik o dosyadan okuma !!!
# Biz burak la eger food+ veya food- yoksa jsonda onu hic yazmamisiz senin gibi, onu degistiricez ...
# O yuzden simdilik sadece files 0,3,4 ve 5 uzerinde calis ...
# endregion

allData = []
# BurgerKing
# data = readfile(files[0], labelled_data)
# setmenu(data,burgerking_menu)
# Cookshop
data = readfile(files[1], cleaned_data)
setmenu(data,cookshop_menu)
group_menu(cookshop_menu)
allData.append(data)
# Liva
data = readfile(files[2], cleaned_data)
setmenu(data,liva_menu)
group_menu(liva_menu)
allData.append(data)

# Mado
# data = readfile(files[3], labelled_data)
# setmenu(data,mado_menu)

# McDonalds
# data = readfile(files[4], labelled_data)
# setmenu(data,mcdonalds_menu)

# Ozsut
# data = readfile(files[5], labelled_data)
# setmenu(data,ozsut_menu)

# IlForno
# data = readfile(files[6], labelled_data)
# setmenu(data,ilforno_menu)

# QuickChina
# data = readfile(files[7], labelled_data)
# setmenu(data,quickchina_menu)

# Aspava
# data = readfile(files[8], labelled_data)
# setmenu(data,aspava_menu)

# Zigane
# data = readfile(files[9], labelled_data)
# setmenu(data,zigane_menu)


# all words in comments
bag_of_comments = [collections.Counter(re.findall(r'\w+', txt)) for txt in comments]
bag_of_words = sum(bag_of_comments, collections.Counter())

all_words = []
for item in bag_of_words:
	all_words.append(item)


# words that have positive comments
bag_of_positive_comments = [collections.Counter(re.findall(r'\w+', txt)) for txt in positive_comments]
bag_of_positive_words = sum(bag_of_positive_comments, collections.Counter())

positive_words = []
for item in bag_of_positive_words:
	positive_words.append(item)


# words that have negative comments
bag_of_negative_comments = [collections.Counter(re.findall(r'\w+', txt)) for txt in negative_comments]
bag_of_negative_words = sum(bag_of_negative_comments, collections.Counter())

negative_words = []
for item in bag_of_negative_words:
	negative_words.append(item)

#for item in bag_of_words:
#	bag_of_positive_words[item] = bag_of_positive_words[item] / bag_of_words[item]
#	bag_of_negative_words[item] = bag_of_negative_words[item] / bag_of_words[item]

words = []
for item in bag_of_words:
	w = Word(item, bag_of_words[item]+1, bag_of_positive_words[item]+1, bag_of_negative_words[item]+1)
	words.append(w)

total_count = 0
total_pos_count = 0
total_neg_count = 0
for word in words:
	total_count = total_count + word.count
	total_pos_count = total_pos_count + word.pos_count
	total_neg_count = total_neg_count + word.neg_count

temp_info = 0
for i in range(0,len(words)):
	temp_info = (words[i].pos_count/total_count)*math.log((total_count*words[i].pos_count)/(words[i].count*total_pos_count),2)
	temp_info = ((total_pos_count-words[i].pos_count)/total_count)*math.log((total_count*(total_pos_count-words[i].pos_count))/((total_count-words[i].count)*total_pos_count),2) + temp_info
	temp_info = (words[i].neg_count/total_count)*math.log((total_count*words[i].neg_count)/(words[i].count*total_neg_count),2) + temp_info
	temp_info = ((total_neg_count-words[i].neg_count)/total_count)*math.log((total_count*(total_neg_count-words[i].neg_count))/((total_count-words[i].count)*total_neg_count),2) + temp_info
	words[i].mutual_info = temp_info

words.sort(key=lambda a: a.mutual_info, reverse=True)

for i in range(0,separation_words):
	print(words[i].value)
	print(words[i].mutual_info)

temp_words = []
for i in range(separation_words,len(words)):
	temp_words.append(words[i].value)
add_alternative_names(allData,[cookshop_menu,liva_menu],temp_words,comments)
