# importing various libraries
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
   
# main window
# which inherits QDialog
class Window(QDialog):
       
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
   
        # a figure instance to plot on
        self.figure = plt.figure()
        plt.rc('font', size=25) 
        
        # set the paths
        self.base_path = "C:/Users/zmezl/Desktop/University/AI/Thesis/eXAI_thesis/"
        self.path = self.base_path + "Amin_dataset/"
        
        # set lists
        self.plaats_list = "Undetermined", "Scalp", "Face", "Neck", "Throat", "Upper_arm", "Lower_arm", "Elbow", "Wrist", "Hand_palm", "Hand_other", "Chest", "Upper_back", "Shoulders", "Abdomen", "Lower_back", "Groin", "Genitals", "Buttocks", "Upper_leg", "Knee", "Lower_leg", "Foot_sole", "Foot_other"
        self.rangschikking_list = "Undetermined", "Unique", "Grouped", "Disseminated", "En_bouquet", "Diffuse", "Discrete", "Circumscript", "Confluent", "Segmental", "Regional", "Generalised", "Universal", "Linear", "Annular", "Circinar", "Corymbiform", "Concentric", "Follicular", "Reticular"
        self.omvang_grootte_list = "Undetermined", "Millar", "Lenticular", "Nummular", "Child_palm_sized", "Palm_sized"
        self.omvang_aantal_list = "Undetermined", "One", "Few", "Tens", "Innumerable"
        self.vorm_vorm_list = "Undetermined", "Round", "Oval", "Polygonal", "Polycyclic", "Rectangle", "Linear", "Gyrated", "Dendritic"
        self.vorm_textuur_list = "Undetermined", "Bulbous", "Bulbous_with_crater", "Hemispheric", "Flat", "Sharp", "Stemmed", "Bumpy", "Pleated", "Wrinkled", "Verrucous", "Pappilomatous"
        self.omtrek_list = "Undetermined", "Sharp", "Medium_sharp", "Unsharp"
        self.kleur_list = "Undetermined", "Skin_coloured", "Light_red", "Dark_red", "Bright_red", "Purple", "Blue", "Light_brown", "Dark_brown", "Black", "Pale_or_white", "Yellow", "Green", "Orange"
        self.efflorescentie_list = "Undetermined", "Macula", "Erythema", "Purpura", "Teleangiectasia", "Papula", "Urtica", "Nodulus", "Nodus", "Tumor", "Plaque", "Vesicula", "Bulla", "Pustula", "Squama", "Crusta", "Comedo", "Lichenification", "Erosion", "Excoriation", "Vulnus", "Ulcus", "Ragade", "Atrophia", "Scar"
        
        # set the excel  
        self.wb = pd.read_excel(self.base_path + "fitzpatrick17k-amin-annotation.xlsx") 
        
        # set the coordinates
        self.x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        
        # set the array
        self.reg_array = np.zeros((10,10))
   
        # Setting the main canvas
        self.canvas = FigureCanvas(self.figure)
     
        # creating a Vertical Box layout
        window_layout = QVBoxLayout()
           
        # adding canvas to the layout
        window_layout.addWidget(self.canvas, 60)
        
        # creating the button box
        button_layout = QHBoxLayout()
        button_box = QGroupBox("Image controls")
        
        # instructions box
        instructions_box = QGroupBox("Instructions")
        instructions_layout = QVBoxLayout()
        instructions_layout.addWidget(QLabel("Left (blue) is background, right (red) is lesion"))
        instructions_box.setLayout(instructions_layout)
        
        # PROVOKE box
        provoke_layout = QHBoxLayout()
        provoke_box = QGroupBox("PROVOKE controls")
        provoke_box.setLayout(provoke_layout)
        
        ## Adding buttons to the PROVOKE box
        ### Plaats
        self.plaats_selector = QComboBox()
        for plaats in self.plaats_list:
            self.plaats_selector.addItem(plaats)
            
        ### Rangschikking
        self.rangschikking_selector = QComboBox()
        for rangschikking in self.rangschikking_list:
            self.rangschikking_selector.addItem(rangschikking)
        
        ### Omvang grootte
        self.omvang_grootte_selector = QComboBox()
        for omvang_grootte in self.omvang_grootte_list:
            self.omvang_grootte_selector.addItem(omvang_grootte)
        
        ### Omvang aantal
        self.omvang_aantal_selector = QComboBox()
        for omvang_aantal in self.omvang_aantal_list:
            self.omvang_aantal_selector.addItem(omvang_aantal)
        
        ### Vorm vorm
        self.vorm_vorm_selector = QComboBox()
        for vorm_vorm in self.vorm_vorm_list:
            self.vorm_vorm_selector.addItem(vorm_vorm)
        
        ### Vorm textuur
        self.vorm_textuur_selector = QComboBox()
        for vorm_textuur in self.vorm_textuur_list:
            self.vorm_textuur_selector.addItem(vorm_textuur)
        
        ### Omtrek
        self.omtrek_selector = QComboBox()
        for omtrek in self.omtrek_list:
            self.omtrek_selector.addItem(omtrek)
        
        ### Kleur
        self.kleur_selector = QComboBox()
        for kleur in self.kleur_list:
            self.kleur_selector.addItem(kleur)

        ### Efflorescentie   
        self.efflorescentie_selector = QComboBox()
        for efflorescentie in self.efflorescentie_list:
            self.efflorescentie_selector.addItem(efflorescentie)     
        
        # Actually putting the buttons in place
        provoke_layout.addWidget(self.plaats_selector)
        provoke_layout.addWidget(self.rangschikking_selector)
        provoke_layout.addWidget(self.omvang_grootte_selector)
        provoke_layout.addWidget(self.omvang_aantal_selector)
        provoke_layout.addWidget(self.vorm_vorm_selector)
        provoke_layout.addWidget(self.vorm_textuur_selector)
        provoke_layout.addWidget(self.omtrek_selector)
        provoke_layout.addWidget(self.kleur_selector)
        provoke_layout.addWidget(self.efflorescentie_selector)
        
        # adding an (un)show button to the layout
        self.show_button = QPushButton('Hide colours')
        self.show_button.clicked.connect(self.unshow)
        button_layout.addWidget(self.show_button)
                
        # adding close button to the layout
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_app)
        button_layout.addWidget(self.close_button)
                  
        # adding previous button to the layout
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.back)
        button_layout.addWidget(self.back_button)
        
        # adding next button to the layout
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next)
        button_layout.addWidget(self.next_button)
           
        # setting layout to the main window
        button_box.setLayout(button_layout)
        window_layout.addWidget(instructions_box, 10)
        window_layout.addWidget(button_box, 10)
        window_layout.addWidget(provoke_box, 20)
        self.setLayout(window_layout)
        
        # Set the initial image
        self.im = 0
        
        # Set the paths
        self.base_path = "C:/Users/zmezl/Desktop/University/AI/Thesis/eXAI_thesis/"
        self.path = self.base_path + "Amin_dataset/"
        
        self.show_bool = True
        
        # Start 
        self.init_step()
        self.showMaximized()
   
    # action called by thte push button
    def init_step(self):
        self.figure.clear()
        self.im += 1
        self.render_image()
    
    def next(self):
        self.save_and_reset()
        self.im += 1
        self.render_image()
        
    def reload(self):
        self.save_and_reset()
        self.render_image()
        
    def back(self):
        self.save_and_reset()
        self.im += -1
        self.render_image()
        
    def save_and_reset(self):
        self.save_colours_local()
        self.save_provoke_local()
        # print(self.reg_array)
        self.figure.clear()
        self.reg_array[self.reg_array != 0] = 0
        
    def render_image(self):
        # clearing and printing
        self.figure.suptitle('IM_'+ str(self.im))
   
        # create an axis
        self.ax = self.figure.add_subplot(111)
   
        # plot data
        img = mpimg.imread(self.path + 'IM_'+ str(self.im) + '.jpg')
        self.ax.imshow(img, extent=[0, 50, 0, 50])
        
        self.ax.set_xticks(self.x)
        self.ax.set_yticks(self.x)
        self.ax.grid(True)
        
        self.ax.figure.canvas.mpl_connect('button_press_event', self.draw_colours)
        
        # Adding the colours
        self.check_colours()
        self.check_provoke()
        
        # refresh canvas
        self.canvas.draw()
        
    def draw_existing_colours(self):
        for r in range(0,10):
                for c in range(0,10):
                    if self.reg_array[r,c] != 0:
                        value = self.reg_array[r,c]
                        x_pos = self.x[c + 1] - 5
                        y_pos = self.x[10 - r] - 5
                        if value == 10.0:
                            # Lesion
                            rec_col = 'red'
                        elif value == -10.0:
                            # Background
                            rec_col = 'blue'
                            
                        self.ax.add_patch(Rectangle((x_pos, y_pos), width=5, height=5, color=rec_col, alpha=0.2))  
                        self.ax.figure.canvas.draw()
   
    def save_colours_local(self):
        reg_array_reshaped_list = self.reg_array.reshape((100)).tolist()
        self.wb['Interest_boxes'][self.im - 1] = str(reg_array_reshaped_list)
        
    def close_app(self):
        print("Trying to save to Excel...")
        self.wb.to_excel(self.base_path + "fitzpatrick17k-amin-annotation.xlsx")
        print("Saved to Excel")
        self.close()
        print("Closed correctly")
        
    def check_colours(self):        
        interest_box = self.wb['Interest_boxes'][self.im - 1]
        
        if isinstance(interest_box,str) and '[' in interest_box:
            # print("Found the following coloration")
            
            self.reg_array = np.asarray(interest_box.strip("[").strip("]").split(",")).reshape((10,10)).astype(float)
            
            if self.show_bool == True:
                self.draw_existing_colours()

    def draw_colours(self, event):
        
        if event.inaxes == self.ax:       
            x_co = event.xdata
            y_co = event.ydata
            
            if event.button is MouseButton.LEFT:
                # Background
                rec_col = 'blue'
                value = -10   
            if event.button is MouseButton.RIGHT:
                # Lesion
                rec_col = 'red'
                value = 10
            
            i = 0
            
            for i in range(0, 11):
                if x_co < self.x[i]:
                    x_pos = self.x[i] - 5
                    col = i - 1
                    break
                else:
                    i += 1
                
            z = 0
            
            for z in range(0, 11):
                if y_co < self.x[z]:
                    y_pos = self.x[z] - 5
                    row = 10 - z
                    break
                else:
                    z += 1
            
            if self.reg_array[row, col] == 0:
                self.ax.add_patch(Rectangle((x_pos, y_pos), width=5, height=5, color=rec_col, alpha=0.2))  
                self.ax.figure.canvas.draw()
                self.reg_array[row, col] = value
            elif self.reg_array[row, col] == value:
                self.reg_array[row, col] = 0
                self.show_bool = True
                self.reload()
            elif self.reg_array[row, col] != value:
                self.reg_array[row, col] = value
                self.show_bool = True
                self.reload()
                            
    def save_provoke_local(self):
        self.provoke = self.plaats_selector.currentText(), self.rangschikking_selector.currentText(), self.omvang_grootte_selector.currentText(), self.omvang_aantal_selector.currentText(), self.vorm_vorm_selector.currentText(), self.vorm_textuur_selector.currentText(), self.omtrek_selector.currentText(), self.kleur_selector.currentText(), self.efflorescentie_selector.currentText()
        
        self.wb['PROVOKE'][self.im - 1] = self.provoke
    
    def check_provoke(self):
        self.provoke = self.wb['PROVOKE'][self.im - 1]
        
        if isinstance(self.provoke,str):
            self.provoke = self.provoke.strip('(').strip(')').replace("'", "").split(', ')
            
            self.set_provoke() 
        elif not isinstance(self.provoke,float) and len(self.provoke) > 0:
            self.set_provoke()
            
    def set_provoke(self):
        self.plaats_selector.setCurrentText(self.provoke[0])
        self.rangschikking_selector.setCurrentText(self.provoke[1])
        self.omvang_grootte_selector.setCurrentText(self.provoke[2])
        self.omvang_aantal_selector.setCurrentText(self.provoke[3])
        self.vorm_vorm_selector.setCurrentText(self.provoke[4])
        self.vorm_textuur_selector.setCurrentText(self.provoke[5])
        self.omtrek_selector.setCurrentText(self.provoke[6])
        self.kleur_selector.setCurrentText(self.provoke[7])
        self.efflorescentie_selector.setCurrentText(self.provoke[8])
        
    def unshow(self):
        self.show_bool = not self.show_bool
        
        if self.show_bool:
            self.show_button.setText("Hide colours")
        else:
            self.show_button.setText("Show colours")
            
        self.reload()
        
            
            
                                                 
# driver code
if __name__ == '__main__':
       
    # creating apyqt5 application
    app = QApplication(sys.argv)
    
    app.setStyleSheet("QLabel{font-size: 12pt;}"
                      "QComboBox{font-size: 14pt;}"
                      "QPushButton{font-size: 14pt;}")
   
    # creating a window object
    main = Window()
       
    # showing the window
    main.show()
   
    # loop
    sys.exit(app.exec_())
