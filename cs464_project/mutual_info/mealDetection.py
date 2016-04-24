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
labelled_data = "C:/Users/FKRT/Desktop/cs464_project/labelled data/"
cleaned_data = "C:/Users/FKRT/Desktop/cs464_project/cleaned data/"

# Menu sets
burgerking_menu = set()
cookshop_menu = set()
liva_menu = set()
mado_menu = set()
mcdonalds_menu = set()
ozsut_menu = set()
ilforno_menu = set()
quickchina_menu = set()
aspava_menu = set()
zigane_menu = set()

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
            menu.add(j)
        for k in data['tips'][i]['food-']:
            menu.add(k)
            negative_comments.add(data['tips'][i]['comment'])


# region ERRORZZZZ Buraya Bakarlar !!!
# Mado.json da \" kullanildigi icin hata veriyor, simdilik o dosyadan okuma !!!
# Biz burak la eger food+ veya food- yoksa jsonda onu hic yazmamisiz senin gibi, onu degistiricez ...
# O yuzden simdilik sadece files 0,3,4 ve 5 uzerinde calis ...
# endregion


# BurgerKing
# data = readfile(files[0], labelled_data)
# setmenu(data,burgerking_menu)

# Cookshop
data = readfile(files[1], cleaned_data)
setmenu(data,cookshop_menu)

# Liva
data = readfile(files[2], cleaned_data)
setmenu(data,liva_menu)

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
#    bag_of_positive_words[item] = bag_of_positive_words[item] / bag_of_words[item]
#    bag_of_negative_words[item] = bag_of_negative_words[item] / bag_of_words[item]

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

for i in range(0,20):
    print(words[i].value)
    print(words[i].mutual_info)
