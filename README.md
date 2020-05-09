# CF
Collaborative filtering recommendation algorithm
数据：mk-100k
u.data内容
user id  movie id  评分     其他
196	      242	    3	    881250949
186 	  302	    3	    891717742
22	      377	    1	    878887116
244	      51	    2	    880606923
166	      346	    1	    886397596
u.item内容
movie_id movie_name release
1|Toy Story (1995)|01-Jan-1995|
2|GoldenEye (1995)|01-Jan-1995|
3|Four Rooms (1995)|01-Jan-1995|
一.基于用户的协同过滤推荐
1.获取电影的列表
getMoviesList()将文件处理为字典，key为movie_id,value为movie_name,release等信息
2.推荐算法
         recommend_list,user_movie,items_movie,neighbors=recommendByUserFC(file_name,userid,k=5)
         # 推荐列表（排序后的电影id），用户看的所有电影，看每一部电影的所有用户，用户邻居（相似度，邻居id）
1）读取u.data文件readFile(file_name)，将文件处理为list
2）文件数据格式化成二维数组 List[[用户id,电影id,电影评分]
[196, 242, 3]
[186, 302, 3]
[22, 377, 1]
……
3）#格式化成字典数据 createUserRankDic(test_rates)
    #    1.用户字典：user_dic[用户id]=[(电影id,电影评分)...]
    #    2.电影字典：moive_to_user[电影id]=[用户id1,用户id2...]
4)寻找邻居calcNearestNeighbor（userid,user_dic,moive_to_user)[:k]
返回list，格式为[相似度，neighbor_id]
[0.2671999496051702, 360]
[0.2564759166321981, 344]
[0.2537784706377533, 669]
5）返回推荐列表
recommend_list=[50,181,100,1,……]
3.创建表格，显示推荐结果
from userid表示所有看过该电影的用户，只显示了五个
            movie name                   release            from userid
================================================================================
Star Wars (1977)                         01-Jan-1977   [234, 271, 299, 269, 94]
Return of the Jedi (1983)                14-Mar-1997   [184, 197, 344, 325, 18]
Fargo (1996)                             14-Feb-1997   [312, 184, 131, 237, 329]
……

二.基于物品的协同过滤推荐
1.获取电影的列表
getMoviesList()将文件处理为字典，key为movie_id,value为movie_name,release等信息
2.读取数据
item = ItemBasedCF("D:/PycharmProject/recomender system/data/ml-100k/u.data")
二维字典{user_id:{movie_id:rate}}
{'196':{'242':3,'393':4,'381':4,……}}
3.计算物品相似度
item.ItemSimilarity()
1）建立物品-物品的共现矩阵
{movie_id:{moive_id:number}}number表示既喜欢物品i有喜欢物品j的用户数量
{242:{393:19},{381：16}……}
2）计算相似度矩阵（余弦相似度）
相似度=表示既喜欢物品i有喜欢物品j的用户数量/根号（喜欢物品i的用户数量*喜欢物品j的用户数量）
{movie_id:{moive_id:similarity}}
{242:{393:0.126776812176236066},……}
……
4.给用户（id为166）做推荐：recommedDict = item.Recommend("166")
{movie_id,similarity}
{'272': 9.469108400924105,
'316': 4.613780614324314,
'271': 3.6687907559668975,
……}
5.创建表格，显示推荐结果
         movie name                  release
==================================================
Good Will Hunting (1997)               01-Jan-1997
As Good As It Gets (1997)              23-Dec-1997
Starship Troopers (1997)               01-Jan-1997
Volcano (1997)                         25-Apr-1997
Game, The (1997)                       01-Jan-1997
Scream 2 (1997)                        01-Jan-1997
……
