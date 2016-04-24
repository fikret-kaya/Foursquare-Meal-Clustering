import json

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

# File list
files = ['BurgerKing.json','Cookshop.json','LivaBistro.json','Mado.json','McDonalds.json','Ozsut.json',
         'PizzaIllForno.json','QuickChina.json','YıldızAspavaLabeled.json','ZiganePideLabeled.json']

# Reads file and return the data of the file
def readfile(filename):
    with open(filename, encoding="utf8", errors="ignore") as jsonfile:
        data = json.load(jsonfile)
        return data

# Gets file's data and add them to general menu
def setmenu(data, menu):
    for i in range(len(data['tips'])):
        for j in data['tips'][i]['food+']:
            menu.add(j)
        for k in data['tips'][i]['food-']:
            menu.add(k)


# region ERRORZZZZ Buraya Bakarlar !!!
# Mado.json da \" kullanildigi icin hata veriyor, simdilik o dosyadan okuma !!!
# Biz burak la eger food+ veya food- yoksa jsonda onu hic yazmamisiz senin gibi, onu degistiricez ...
# O yuzden simdilik sadece files 0,3,4 ve 5 uzerinde calis ...
# endregion


# BurgerKing
data = readfile(files[0])
setmenu(data,burgerking_menu)
# Cookshop
data = readfile(files[1])
setmenu(data,cookshop_menu)
# Liva
data = readfile(files[2])
setmenu(data,liva_menu)
# Mado

# McDonalds

# Ozsut
data = readfile(files[5])
setmenu(data,ozsut_menu)
# IlForno
data = readfile(files[6])
setmenu(data,ilforno_menu)
# QuickChina
data = readfile(files[7])
setmenu(data,quickchina_menu)
# Aspava

# Zigane

print(len(burgerking_menu))
