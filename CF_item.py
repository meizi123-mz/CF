import math
import pdb
from texttable import Texttable
def getMoviesList(file_name):
    #print sys.getdefaultencoding()
    movies_contents=readFile(file_name)
    movies_info={}
    for movie in movies_contents:
        movie_info=movie.split("|")
        movies_info[int(movie_info[0])]=movie_info[1:]
    return movies_info
def readFile(file_name):
    contents_lines=[]
    f=open(file_name,"r",encoding='ISO-8859-1')#The encoding was "ISO-8859-1"
    contents_lines=f.readlines()
    f.close()
    return contents_lines
class ItemBasedCF:
    def __init__(self, train_file):
        self.train_file = train_file
        self.readData()

    def readData(self):
        # 读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()
        # 用户-物品的评分表
        for line in open(self.train_file):
            user, item, score,other = line.strip().split("\t")
            self.train.setdefault(user, {})
            self.train[user][item] = int(float(score))

    def ItemSimilarity(self):
        # 建立物品-物品的共现矩阵
        cooccur = dict()  # 物品-物品的共现矩阵
        buy = dict()  # 物品被多少个不同用户购买N
        for user, items in self.train.items():
            for i in items.keys():
                buy.setdefault(i, 0)
                buy[i] += 1
                cooccur.setdefault(i, {})
                for j in items.keys():
                    if i == j: continue
                    cooccur[i].setdefault(j, 0)
                    cooccur[i][j] += 1
        # 计算相似度矩阵
        self.similar = dict()
        for i, related_items in cooccur.items():
            self.similar.setdefault(i, {})
            for j, cij in related_items.items():
                self.similar[i][j] = cij / (math.sqrt(buy[i] * buy[j]))
        return self.similar

    # 给用户user推荐，前K个相关用户，前N个物品
    def Recommend(self, user, K=3, N=10):
        rank = dict()
        action_item = self.train[user]
        # 用户user产生过行为的item和评分
        for item, score in action_item.items():
            sortedItems = sorted(self.similar[item].items(), key=lambda x: x[1], reverse=True)[0:K]
            for j, wj in sortedItems:
                if j in action_item.keys():
                    continue
                rank.setdefault(j, 0)
                rank[j] += score * wj
        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N])


# 声明一个ItemBasedCF的对象
movies=getMoviesList("D:/PycharmProject/recomender system/data/ml-100k/u.item")#得到电影Item的信息
item = ItemBasedCF("D:/PycharmProject/recomender system/data/ml-100k/u.data")
item.ItemSimilarity()
recommedDict = item.Recommend("166")
table = Texttable()
table.set_deco(Texttable.HEADER)
table.set_cols_dtype(['t',  # text
                      't']) # automatic
table.set_cols_align(["l", "l"])
rows=[]
rows.append([u"movie name",u"release"])
for movieid in recommedDict:
    movieid=int(movieid)
    rows.append([movies[movieid][0], movies[movieid][1]])
table.add_rows(rows)
print(table.draw())