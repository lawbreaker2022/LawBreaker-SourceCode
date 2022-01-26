import matplotlib.pyplot as plt
import numpy as np


name = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S8', 'S9']
value1 = np.array([5, 1, 4, 0, 1, 3, 7, 9])   #创建随机数字
value2 = np.array([3, 0, 2, 0, 0, 2, 3, 4])   #创建随机数字
x = np.array(range(8))

# name = ['S6', 'S8', 'S9']
# value1 = np.array([3, 7, 9])   #创建随机数字
# value2 = np.array([2, 3, 4])   #创建随机数字
# x = np.array(range(3))

"""
绘制条形图
left:长条形中点横坐标
height:长条形高度
width:长条形宽度，默认值0.8
alpha:透明度
color:颜色
label:标签，为后面设置legend准备
"""
bar1 = plt.bar(x-0.2, value1, width=0.4, color='r', label='GA1')                  #第一个图

bar2 = plt.bar(x+0.2, value2, width=0.4, color='b', label='Rand')                   #第二个图

plt.xticks(x, name, fontsize=14)      #设置x轴刻度显示值
plt.yticks(fontsize=14)
# plt.ylim(0,10500)       #y轴的范围
# plt.title('XXX公司')     #标题
plt.xlabel('Scenario', fontsize=16)       #x轴的标签
plt.ylabel('# Issues', fontsize=18)       #y轴的标签
plt.legend(fontsize=14)            #设置图例

'''
get_height:获取值
get_x：获取x轴的位置
get_width:获取图形的宽度
text(x,y,s,fontsize,ha,va)
    x,y:表示坐标值上的值
    s:表示说明文字
    fontsize:表示字体大小
    ha：垂直显示方式{'centee':'中心', 'right':'右', 'left':'左'}
    va：水平显示方式{'center':'中心', 'top':'下', 'bottom':'上', 'baseline':'基线'} 
'''

for rect in bar1:
    height = rect.get_height()  #获得bar1的高度
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), fontsize=12, ha="center", va="bottom")
for rect in bar2:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), fontsize=12, ha="center", va="bottom")

plt.show()