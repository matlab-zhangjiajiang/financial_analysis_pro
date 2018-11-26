# coding=utf-8
from matplotlib import pyplot as plt

class draw_histogram(object):


  # 参数依次为list,抬头,X轴标签,Y轴标签,XY轴的范围
  def draw_hist(myList,Title,Xlabel,Ylabel,Xmin,Xmax,Ymin,Ymax):
    plt.hist(myList,100)
    plt.xlabel(Xlabel)
    plt.xlim(Xmin,Xmax)
    plt.ylabel(Ylabel)
    plt.ylim(Ymin,Ymax)
    plt.title(Title)
    plt.show()


##draw_hist(areaList,'AreasList','Area','number',50.0,250,0.0,8)   # 直方图展示
##draw_hist(perimeterList,'perimeterList','Area','number',40.0,80,0.0,8)