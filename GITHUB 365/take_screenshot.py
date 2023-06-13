import pyautogui as pg
import time
import os

class screenshot_class():

   def __init__(self):
      self.location = 'C:/Users/DELL/Desktop/GUI_IIITNR/Screenshots'
   
   def create_ss_folder(self):
      try:
         self.location = 'C:/Users/DELL/Desktop/GUI_IIITNR/Screenshots'
         if(os.path.exists(self.location)):
            pass
         else:
            os.makedirs(self.location)

      except:
         print("Error creating screenshot folder")

   def screenshot(self):
      self.filename = (self.location + '/' + time.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg")
      pg.screenshot(self.filename)



