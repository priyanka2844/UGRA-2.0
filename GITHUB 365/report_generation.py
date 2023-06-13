import os

class generate_report_directory():

   def __init__(self):
        self.location = 'C:/Users/DELL/Desktop/GUI_IIITNR/Report'
   
   def create_report_folder(self):
        try:
            self.location = 'C:/Users/DELL/Desktop/GUI_IIITNR/Report'
            if(os.path.exists(self.location)):
                pass
            else:
                os.makedirs(self.location)

        except:
            print("Error creating Reports folder")

        return self.location