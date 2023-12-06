#recall :  perceptron  ;  f=sign(w*x+b)

#loss function :  -sum(M)(yi*(wx+b))

import numpy as np
#数据点
x=np.array([[3,3],[4,3],[1,1]])
y=np.array([1,1,-1])
def muti_matrix(a,b):
    result=0
    for i in range(len(a)):
        result+=a[i]*b[i]
    return  result
def opti_target(i,a,b,Gram):  #i为xi
    sum=0
    for j in range(len(x)):
        sum+=a[j]*y[j]*Gram[j][i]
    return y[i]*(sum+b)



#初始参数
a=np.array([0,0,0])
b=0

#计算Gram矩阵
Gram=np.zeros((len(x),len(x)))
for i in range(len(x)):
    for j in range(len(x)):
        Gram[i][j]=muti_matrix(x[i],x[j])



sp=False  #标记是否没有误分类数据
nata=1 #learning rate
while(sp==False):
    sp=True
    for i in range(len(x)):
        print(i,"opti:", opti_target(i, a, b, Gram))
        if(opti_target(i,a,b,Gram)<=0):

            a[i]=a[i]+nata
            b=b+nata*y[i]
            sp = False
        print("a:",a,"b:",b)
print("result:",a,b)








