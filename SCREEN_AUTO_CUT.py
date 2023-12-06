import pyautogui
import time
import  keyboard



current_num=264
number=200
time.sleep(3)
for i in range(number):

  time.sleep(0.5)
  im = pyautogui.screenshot()
  print("img caputure successfully")

  im.save("dataset_test_robot/{num}.jpg".format(num=i+current_num))