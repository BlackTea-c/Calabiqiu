import torch
from screen_shot import  Capturer,Timer
import time
import  cv2
from win32con import HWND_TOPMOST, SWP_NOMOVE, SWP_NOSIZE  # win32core ==>> win32con
from win32gui import FindWindow, SetWindowPos
import  numpy as np
import pydirectinput
import  keyboard
import pyautogui
from  logitech import Logitech
import pandas as pd


pyautogui.FAILSAFE=False
model=torch.hub.load('yolov5-master','custom','yolov5-master/runs/train/exp21/weights/best.pt',source="local")# use "custom"  else it will download .pt from github.
#参数设置：
model.classes=[0]   #coco.yaml
model.conf=0.35
print(model.conf)

region=region = (0, 0,2560, 1440)
title="Visualized Image"
cv2.namedWindow("Visualized Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Visualized Image", 320, 180)
cv2.setWindowProperty("Visualized Image", cv2.WND_PROP_TOPMOST, 1)




#鼠标移动




origion_pos=[1280,720]



def mouse_track(lr,rb):
    #x, y = pyautogui.position()  # 返回鼠标的坐标
    x=origion_pos[0]
    y=origion_pos[1]
    dx = lr - x
    dy = rb - y
    Logitech.mouse.move(dx//4,dy//4)
    Logitech.mouse.move(dx // 4, dy // 4)
    Logitech.mouse.move(dx // 4, dy // 4)
    Logitech.mouse.move(dx // 4, dy // 4)
    print("鼠标移动量:",dx," ",dy)
    return dx,dy



import ctypes
import os
import pynput
import winsound





#相对位移尝试用pydirectinput.move()  move_to不对劲！


#储存移动量与位置 数据
data_dx=[]
data_dy=[]
data_targert_x=[]
data_targert_y=[]
#================
while True:

    t1 = time.perf_counter_ns()
    img = Capturer.backup(region)
    t2 = time.perf_counter_ns()
     #BGR==>RGB
    img = model(img)
    #==========

    #print(type(img))
    #img = img.ims[0]
    #print(dir(img))
    # 获取处理后的图像和检测结果
    #processed_image = img.ims[0]
    # 获取处理后的图像和检测结果
    #print(img)
    processed_image = img.ims[0]
    detections = img.pred[0]

    # 复制图像以避免修改原始图像
    result_image = np.copy(processed_image)

    # 遍历检测结果并绘制边界框
    # 遍历检测结果并绘制边界框  边界框始终画不对！！！！！！！！！
    dxdyes=[]  #store the distance from centre to target box.
    box_position=[] #store the position of boxes
    for det in detections:
        left, top, right, bottom, confidence, class_id = det[0:6].cpu().numpy()
        left, top, right, bottom = int(left), int(top), int(right), int(bottom)

        color = (0, 255, 0)  # 边界框颜色，这里使用绿色
        label = f'Class: {int(class_id)}, Conf: {confidence:.2f}'  # 类别和置信度信息
        #print("坐标:",left,top,right,bottom)


        cv2.rectangle(result_image, (left, top), (right, bottom), color, 2)
        cv2.putText(result_image, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        lr = (left + right) // 2
        rb = (top + bottom) // 2
        box_position.append([lr,rb])
        dxdyes.append((lr-origion_pos[0])**2 + (rb-origion_pos[1])**2)#距离最小准测  #add the linear distance.  so each box has this number in dxdyes
        #dxdyes.append((right-left)*(bottom-top))#面积最大准测,这里取负数是为了跟下面的min切合,有点问题，效果不太好。

        print("conf=",confidence)

    #and we just find the minium distance by the box(I mean the box that is closest to our centre)
    if dxdyes!=[]:
      print("距离/面积：",dxdyes)
      min_index=dxdyes.index(min(dxdyes))
      print("目标起始位置:",box_position[min_index][0],box_position[min_index][1])
      if keyboard.is_pressed('alt'):
       dx,dy=mouse_track(box_position[min_index][0],box_position[min_index][1])
      #data_dx.append(dx)
     # data_dy.append(dy)
      #data_targert_x.append(box_position[min_index][0])
      #data_targert_y.append(box_position[min_index][1])




    # 显示可视化结果

    cv2.imshow("Visualized Image", result_image)
    k = cv2.waitKey(1)  # 0:不自动销毁也不会更新, 1:1ms延迟销毁
    if k % 256 == 27:
        cv2.destroyAllWindows()
        # 保存数据

        # 创建一个字典，其中键是列名，值是数据
       # data = {'dx': data_dx, 'dy': data_dy, 'target_x': data_targert_x, 'target_y': data_targert_y}

        # 使用pandas创建一个DataFrame
        #df = pd.DataFrame(data)

        # 将DataFrame保存为csv文件
        #df.to_csv('data_mouse.csv', index=False)

        exit('ESC ...')
    time.sleep(0.01)







#仍然存在的问题
#1.训练程度貌似不够？  2.鼠标灵敏度与 pydirectinput.move的关系  3.瞄不准？
#4.鼠标 触底现象！ 鼠标达到边框后move失效！ 我们应该即使更新鼠标的位置！！！！
#5.灵敏度为8时定位不准  猜测可能原因1.识别不准（不太可能，因为灵敏度为1时是准的） 2.鼠标移动具有加速度 3.与灵敏度有关需要调整logitech.move的移动量？


#打算收集的数据   1.鼠标相对位移 此即dx，dy  2.目标初始位置/移动后位置    3.鼠标灵敏度


#MOUSE.MOVE 是以一个力来把鼠标抛出去，所以灵敏度不同会导致其不准，比如我设置的8倍数，就会抛过了；我打算收集一下鼠标移动量 目标位置   目标是测出准星的移动量与鼠标移动量的关系？


#有加速度，不是单纯的8倍关系 唉，想放弃了