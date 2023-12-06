#求f(x)=sign(w*x+b) linear classifier
import time
import numpy as np
#数据点
x=np.array([[3,3],[4,3],[1,1]])
y=np.array([1,1,-1])
#初始参数
w=np.array([0,0])
b=0
#同n阶的矩阵乘法
def muti_matrix(a,b):
    result=0
    for i in range(len(a)):
        result+=a[i]*b[i]
    return  result

#判别模型
def classifier_result(w,b,x):
    if((muti_matrix(w,x)+b)>0):
        return 1
    if ((muti_matrix(w,x)+b)<0):
        return -1
    if ((muti_matrix(w,x)+b)==0):
        return  0


#损失函数
def loss_function_L(w,b,x,y):
    L=0
    record=[] #记录误分类点
    for i in range(len(x)):
        #print(classifier_result(w,b,x[i]))
        if(classifier_result(w,b,x[i])!=y[i]):
            L+=-y[i]*(muti_matrix(w,x[i])+b)
            record.append(i)
    return L,record


#优化器
#nata : 学习率
def optimizer(nata,record):
    #dl/dw 梯度
    Lw=[0,0]
    #dl/b
    Lb=0
    #if record !=[]
    i=record[0]
    Lw+=-y[i]*x[i]
    Lb+=-y[i]
    return nata*Lw,nata*Lb



#主程序
L,record=loss_function_L(w,b,x,y)
#print(L,record)
while(record!=[]):
    w-=optimizer(1,record)[0]  #梯度的反方向!
    b-=optimizer(1,record)[1]
    L,record=loss_function_L(w,b,x,y)
    print(w,b,L)
    #time.sleep(1.5)
print("results:",L," ",w," ",b)

