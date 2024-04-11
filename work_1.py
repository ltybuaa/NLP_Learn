import os
import jieba
from matplotlib import pyplot as plt

data_dir=os.listdir("Chinese_data")
txt=""
for name in data_dir:
    with open('Chinese_data/'+name,'r',encoding="gb18030") as file:
        txt=txt+file.read()

#加入要去除的标点符号
excludes = {"，", "。", "\n", "-", "“", "”", "：", "；", "？", "（", "）", "！", "…"}

#利用jieba分词
words = jieba.lcut(txt)

#设置初始计数数组
counts = {}

#开始遍历计数
for word in words:
    counts[word] = counts.get(word,0)+1

#去除标点符号
for word in excludes:
    del counts[word]

#返回遍历得分所有键与值
items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)
sort_list = sorted(counts.values(), reverse=True)

#根据词出现次序进行排序
items.sort(key=lambda x: x[1], reverse=True)

#将数据写入ｔｘｔ文本便于导入Matlab画图
file = open('data.txt', mode='w')

#输出词语与词频
for i in range(10963):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word,count))

    #写入ｔｘｔ文件
    new_context = word + "   " + str(count) + '\n'
    file.write(new_context)

file.close()



plt.title('Zipf-Law',fontsize=18)  #标题
plt.xlabel('rank',fontsize=18)     #排名
plt.ylabel('freq',fontsize=18)     #频度
plt.yticks([pow(10,i) for i in range(0,4)])  # 设置y刻度
plt.xticks([pow(10,i) for i in range(0,4)])  # 设置x刻度
x = [i for i in range(len(sort_list))]
plt.yscale('log')                  #设置纵坐标的缩放
plt.xscale('log')                  #设置横坐标的缩放
plt.plot(x, sort_list , 'r')       #绘图
plt.savefig('./Zipf_Law.jpg')      #保存图片
plt.show()