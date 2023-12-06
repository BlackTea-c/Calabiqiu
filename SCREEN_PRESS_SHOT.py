import pyautogui
import time
import  keyboard



current_num=264
number=200
time.sleep(3)
i=current_num
while True:
 if keyboard.is_pressed('alt'):
   im = pyautogui.screenshot()
   print("img caputure successfully")

   im.save("dataset_test_robot/{num}.jpg".format(num=i))
   i=i+1