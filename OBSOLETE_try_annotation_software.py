# importing various libraries
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QGridLayout, QListWidget, QCheckBox
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
        self.plaats_list = ["Undetermined", "Scalp", "Face", "Neck", "Throat", "Upper_arm", "Lower_arm", "Elbow", "Wrist", "Hand_palm", "Hand_other", "Chest", "Upper_back", "Shoulders", "Abdomen", "Lower_back", "Groin", "Genitals", "Buttocks", "Upper_leg", "Knee", "Lower_leg", "Foot_sole", "Foot_other"]
        
        self.rangschikking_verdeling_list = ["Undetermined", "Solitary", "Grouped"]
        self.rangschikking_plaats_list = ["Undetermined", "Regional", "Segmental", "Ptychotropic", "Generalised", "Universal", "Follicular"]
        self.rangschikking_confluentie_list = ["Undetermined", "Discrete", "Touching", "Confluent"]
        self.rangschikking_vorm_list = ["Undetermined", "Linear", "Arciform", "Annular", "Circinar", "Concentric", "Cocardic", "Corymbiform", "En_bouquet", "Reticular"]
        
        self.rangschikking_list = ["Undetermined", "Verdeling - solitair", "Verdeling - grouped", 
                                   "Plaats - regionaal", "Plaats - segmenteel", "Plaats - ptychotroop", "Plaats - gegeneraliseerd", "Plaats - universeel", "Plaats - folliculair",
                                   "Confluentie - discreet", "Confluentie - diffuus", "Confluentie - confluerend",
                                   "Vorm - Lineair", "Vorm - Arciform", "Vorm - Annulair", "Vorm - Circinair", "Vorm - concentrisch", "Vorm - cocardisch", "Vorm - Corymbiform", "Vorm - En bouquet", "Vorm - Reticulair"]
        
        self.omvang_grootte_list = ["Undetermined", "Millar", "Lenticular", "Nummular", "Child_palm_sized", "Palm_sized", "Regional", "Generalised"]
        self.omvang_aantal_list = ["Undetermined", "One", "Few", "Tens", "Innumerable"]
        
        self.omvang_list = ["Undetermined", "Grootte - millair", "Grootte - lenticulair", "Grootte - nummulair", "Grootte - kinderhandpalm", "Grootte - handpalm", "Grootte"]
        
        self.vorm_vorm_list = ["Undetermined", "Round", "Oval", "Polygonal", "Polycyclic", "Rectangle", "Linear", "Gyrated", "Dendritic"]
        self.vorm_textuur_list = ["Undetermined", "Bulbous", "Bulbous_with_crater", "Hemispheric", "Flat", "Sharp", "Stemmed", "Bumpy", "Pleated", "Wrinkled", "Verrucous", "Pappilomatous"]
        self.omtrek_list = ["Undetermined", "Sharp", "Medium_sharp", "Unsharp"]
        self.kleur_list = ["Undetermined", "Skin_coloured", "Light_red", "Dark_red", "Bright_red", "Purple", "Blue", "Light_brown", "Dark_brown", "Black", "Pale_or_white", "Yellow", "Green", "Orange"]
        self.efflorescentie_list = ["Undetermined", "Macula", "Erythema", "Purpura", "Teleangiectasia", "Papula", "Urtica", "Nodulus", "Nodus", "Tumor", "Plaque", "Vesicula", "Bulla", "Pustula", "Squama", "Crusta", "Comedo", "Lichenification", "Erosion", "Excoriation", "Vulnus", "Ulcus", "Ragade", "Atrophia", "Scar"]
        
        # set the excel  
        self.wb = pd.read_excel(self.base_path + "fitzpatrick17k-amin-annotation.xlsx") 
        
        # set the coordinates, array and counters
        self.x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        self.reg_array = np.zeros((10,10))
        self.im = 19
        self.show_bool = True
   
        # Setting the canvas
        self.canvas = FigureCanvas(self.figure)
     
        # creating a Vertical Box layout
        window_layout = QVBoxLayout()
        
        # CREATING THE BUTTON BOX AND BUTTONS
        button_layout = QGridLayout()
        button_box = QGroupBox("Image controls")
        button_box.setLayout(button_layout)
        ## (un)show button
        self.show_button = QPushButton('Hide colours')
        self.show_button.clicked.connect(self.unshow)
        button_layout.addWidget(self.show_button)
        ## close button
        self.close_button = QPushButton('Close')
        self.close_button.clicked.connect(self.close_app)
        button_layout.addWidget(self.close_button)
        ## back button
        self.back_button = QPushButton('Back')
        self.back_button.clicked.connect(self.back)
        button_layout.addWidget(self.back_button)
        ## next button
        self.next_button = QPushButton('Next')
        self.next_button.clicked.connect(self.next)
        button_layout.addWidget(self.next_button)
        
        # CREATING THE INSTURCTIONS BOX
        instructions_box = QGroupBox("Instructions")
        instructions_layout = QVBoxLayout()
        ## Adding the instructions
        instructions_layout.addWidget(QLabel("Left (blue) is background, right (red) is lesion"))
        instructions_box.setLayout(instructions_layout)
        
        ## Adding buttons to the PROVOKE box
        ### Plaats
        self.plaats_non_selected_selector = QListWidget()
        self.plaats_selected_selector = QListWidget()
        ### Rangschikking
        self.rangschikking_non_selected_selector = QListWidget()
        self.rangschikking_selected_selector = QListWidget()
        ### Omvang grootte
        self.omvang_grootte_non_selected_selector = QListWidget()
        self.omvang_grootte_selected_selector = QListWidget()
        ### Omvang aantal
        self.omvang_aantal_non_selected_selector = QListWidget()
        self.omvang_aantal_selected_selector = QListWidget()
        ### Vorm vorm
        self.vorm_vorm_non_selected_selector = QListWidget()
        self.vorm_vorm_selected_selector = QListWidget()
        ### Vorm textuur
        self.vorm_textuur_non_selected_selector = QListWidget()
        self.vorm_textuur_selected_selector = QListWidget()
        ### Omtrek
        self.omtrek_non_selected_selector = QListWidget()
        self.omtrek_selected_selector = QListWidget()
        ### Kleur
        self.kleur_non_selected_selector = QListWidget()
        self.kleur_selected_selector = QListWidget()
        ### Efflorescentie   
        self.efflorescentie_non_selected_selector = QListWidget()
        self.efflorescentie_selected_selector = QListWidget()
        
        # CREATING THE PROVOKE BOX
        provoke_box = QGroupBox("PROVOKE controls")
        provoke_layout = QHBoxLayout()
        provoke_box.setLayout(provoke_layout)
        ## CREATING THE INDIVIDUAL PROVOKE BOXES AND ADDING PROVOKE
        ### Plaats
        plaats_box = QGroupBox("Plaats")
        plaats_layout = QVBoxLayout()
        plaats_box.setLayout(plaats_layout)
        provoke_layout.addWidget(plaats_box)
        plaats_layout.addWidget(QLabel("Non-selected"))
        plaats_layout.addWidget(self.plaats_non_selected_selector)
        plaats_layout.addWidget(QLabel("Selected"))
        plaats_layout.addWidget(self.plaats_selected_selector)
        ### Rangschikking
        rangschikking_box = QGroupBox("Rangschikking")
        rangschikking_layout = QVBoxLayout()
        rangschikking_box.setLayout(rangschikking_layout)
        provoke_layout.addWidget(rangschikking_box)
        rangschikking_layout.addWidget(QLabel("Non-selected"))
        rangschikking_layout.addWidget(self.rangschikking_non_selected_selector)
        rangschikking_layout.addWidget(QLabel("Selected"))
        rangschikking_layout.addWidget(self.rangschikking_selected_selector)
        ### Omvang 
        omvang_box = QGroupBox("Omvang")
        omvang_layout = QHBoxLayout()
        omvang_box.setLayout(omvang_layout)
        provoke_layout.addWidget(omvang_box)
        #### Omvang grootte
        omvang_grootte_box = QGroupBox("Omvang - grootte")
        omvang_grootte_layout = QVBoxLayout()
        omvang_grootte_box.setLayout(omvang_grootte_layout)
        omvang_grootte_layout.addWidget(QLabel("Non-selected"))
        omvang_grootte_layout.addWidget(self.omvang_grootte_non_selected_selector)
        omvang_grootte_layout.addWidget(QLabel("Selected"))
        omvang_grootte_layout.addWidget(self.omvang_grootte_selected_selector)
        omvang_layout.addWidget(omvang_grootte_box)
        #### Omvang aantal
        omvang_aantal_box = QGroupBox("Omvang - aantal")
        omvang_aantal_layout = QVBoxLayout()
        omvang_aantal_box.setLayout(omvang_aantal_layout)
        omvang_aantal_layout.addWidget(QLabel("Non-selected"))
        omvang_aantal_layout.addWidget(self.omvang_aantal_non_selected_selector)
        omvang_aantal_layout.addWidget(QLabel("Selected"))
        omvang_aantal_layout.addWidget(self.omvang_aantal_selected_selector)
        omvang_layout.addWidget(omvang_aantal_box)
        
        ### Vorm 
        vorm_box = QGroupBox("Vorm")
        vorm_layout = QHBoxLayout()
        vorm_box.setLayout(vorm_layout)
        provoke_layout.addWidget(vorm_box)
        #### Vorm vorm
        vorm_vorm_box = QGroupBox("Vorm - vorm")
        vorm_vorm_layout = QVBoxLayout()
        vorm_vorm_box.setLayout(vorm_vorm_layout)
        vorm_vorm_layout.addWidget(QLabel("Non-selected"))
        vorm_vorm_layout.addWidget(self.vorm_vorm_non_selected_selector)
        vorm_vorm_layout.addWidget(QLabel("Selected"))
        vorm_vorm_layout.addWidget(self.vorm_vorm_selected_selector)
        vorm_layout.addWidget(vorm_vorm_box)
        #### Vorm textuur
        vorm_textuur_box = QGroupBox("Vorm - textuur")
        vorm_textuur_layout = QVBoxLayout()
        vorm_textuur_box.setLayout(vorm_textuur_layout)
        vorm_textuur_layout.addWidget(QLabel("Non-selected"))
        vorm_textuur_layout.addWidget(self.vorm_textuur_non_selected_selector)
        vorm_textuur_layout.addWidget(QLabel("Selected"))
        vorm_textuur_layout.addWidget(self.vorm_textuur_selected_selector)
        vorm_layout.addWidget(vorm_textuur_box)
          
        ### Omtrek 
        omtrek_box = QGroupBox("Omtrek")
        omtrek_layout = QVBoxLayout()
        omtrek_box.setLayout(omtrek_layout)
        provoke_layout.addWidget(omtrek_box)
        omtrek_layout.addWidget(QLabel("Non-selected"))
        omtrek_layout.addWidget(self.omtrek_non_selected_selector)
        omtrek_layout.addWidget(QLabel("Selected"))
        omtrek_layout.addWidget(self.omtrek_selected_selector)   
        ### Kleur 
        kleur_box = QGroupBox("Kleur")
        kleur_layout = QVBoxLayout()
        kleur_box.setLayout(kleur_layout)
        provoke_layout.addWidget(kleur_box)
        kleur_layout.addWidget(QLabel("Non-selected"))
        kleur_layout.addWidget(self.kleur_non_selected_selector)
        kleur_layout.addWidget(QLabel("Selected"))
        kleur_layout.addWidget(self.kleur_selected_selector)   
        ### Efflorescentie
        efflorescentie_box = QGroupBox("Efflorescentie")
        efflorescentie_layout = QVBoxLayout()
        efflorescentie_box.setLayout(efflorescentie_layout)
        provoke_layout.addWidget(efflorescentie_box)
        efflorescentie_layout.addWidget(QLabel("Non-selected"))
        efflorescentie_layout.addWidget(self.efflorescentie_non_selected_selector)
        efflorescentie_layout.addWidget(QLabel("Selected"))
        efflorescentie_layout.addWidget(self.efflorescentie_selected_selector)      
        
        right_layout = QVBoxLayout()
        right_box = QGroupBox()
        right_box.setLayout(right_layout)
        
        main_layout = QHBoxLayout()
        main_box = QGroupBox()
        main_box.setLayout(main_layout)
        
        # adding canvas to the layout
        main_layout.addWidget(self.canvas, 70)
        main_layout.addWidget(right_box)
        
        # ADDING THE BOXES TO THE MAIN LAYOUT
        window_layout.addWidget(main_box,80)
        right_layout.addWidget(instructions_box)
        right_layout.addWidget(button_box)
        window_layout.addWidget(provoke_box, 20)
        ## Setting the main layout
        self.setLayout(window_layout)
        
    
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
        # self.provoke = self.plaats_selector.currentItem(), self.rangschikking_selector.currentText(), self.omvang_grootte_selector.currentText(), self.omvang_aantal_selector.currentText(), self.vorm_vorm_selector.currentText(), self.vorm_textuur_selector.currentText(), self.omtrek_selector.currentText(), self.kleur_selector.currentText(), self.efflorescentie_selector.currentText()
        
        self.wb['PROVOKE'][self.im - 1] = self.provoke
    
    def check_provoke(self):
        print("Check provoke")
        self.provoke = self.wb['PROVOKE'][self.im - 1]
        
        if isinstance(self.provoke,str):
            self.provoke = self.provoke.strip('(').strip(')').replace("'", "").split(', ')
            self.determine_provoke()
        else:
            print("Creating empty lists")
            self.plaats_selected_list = []
            self.rangschikking_selected_list = []
            self.omvang_grootte_selected_list = []
            self.omvang_aantal_selected_list = []
            self.vorm_vorm_selected_list = []
            self.vorm_textuur_selected_list = []
            self.omtrek_selected_list = []
            self.kleur_selected_list = []
            self.efflorescentie_selected_list = []
        
        self.set_provoke()
            
    def determine_provoke(self):        
        
        print("Determining provoke")
        
        self.plaats_selected_list = [self.provoke[0]]
        self.plaats_non_selected_list = self.getDifference(self.plaats_selected_list, self.plaats_list)
        
        self.rangschikking_selected_list = [self.provoke[1]]
        self.rangschikking_non_selected_list = self.getDifference(self.rangschikking_selected_list, self.rangschikking_list)
        
        self.omvang_grootte_selected_list = [self.provoke[2]]
        self.omvang_grootte_non_selected_list = self.getDifference(self.omvang_grootte_selected_list, self.omvang_grootte_list)
        
        self.omvang_aantal_selected_list = [self.provoke[3]]
        self.omvang_aantal_non_selected_list = self.getDifference(self.omvang_aantal_selected_list, self.omvang_aantal_list)
        
        self.vorm_vorm_selected_list = [self.provoke[4]]
        self.vorm_vorm_non_selected_list = self.getDifference(self.vorm_vorm_selected_list, self.vorm_vorm_list)
        
        self.vorm_textuur_selected_list = [self.provoke[5]]
        self.vorm_textuur_non_selected_list = self.getDifference(self.vorm_textuur_selected_list, self.vorm_textuur_list)
        
        self.omtrek_selected_list = [self.provoke[6]]
        self.omtrek_non_selected_list = self.getDifference(self.omtrek_selected_list, self.omtrek_list)
        
        self.kleur_selected_list = [self.provoke[7]]
        self.kleur_non_selected_list = self.getDifference(self.kleur_selected_list, self.kleur_list)
        
        self.efflorescentie_selected_list = [self.provoke[8]]
        self.efflorescentie_non_selected_list = self.getDifference(self.efflorescentie_selected_list, self.efflorescentie_list)
    
    def set_provoke(self):
        
        print("Setting provoke")        
        
        self.setter(self.plaats_selected_selector, self.plaats_selected_list)
        self.setter(self.plaats_non_selected_selector, self.plaats_non_selected_list)                
        self.plaats_selected_selector.itemClicked.connect(self.clicked_plaats)
        self.plaats_non_selected_selector.itemClicked.connect(self.clicked_plaats)
        
        
        self.setter(self.rangschikking_selected_selector, self.rangschikking_selected_list)
        self.setter(self.rangschikking_non_selected_selector, self.rangschikking_non_selected_list)
        #self.rangschikking_selected_selector.itemClicked.connect(self.clicked_rangschikking)
        #self.rangschikking_non_selected_selector.itemClicked.connect(self.clicked_rangschikking)
        
        self.setter(self.omvang_grootte_selected_selector, self.omvang_grootte_selected_list)
        self.setter(self.omvang_grootte_non_selected_selector, self.omvang_grootte_non_selected_list)
        #self.omvang_grootte_selected_selector.itemClicked.connect(self.clicked_grootte)
        #self.omvang_grootte_non_selected_selector.itemClicked.connect(self.clicked_grootte)
        
        self.setter(self.omvang_aantal_selected_selector, self.omvang_aantal_selected_list)
        self.setter(self.omvang_aantal_non_selected_selector, self.omvang_aantal_non_selected_list)
        #self.omvang_aantal_selected_selector.itemClicked.connect(self.clicked_aantal)
        #self.omvang_aantal_non_selected_selector.itemClicked.connect(self.clicked_aantal)
        
        self.setter(self.vorm_vorm_selected_selector, self.vorm_vorm_selected_list)
        self.setter(self.vorm_vorm_non_selected_selector, self.vorm_vorm_non_selected_list)
        #self.vorm_vorm_selected_selector.itemClicked.connect(self.clicked_vorm_vorm)
        #self.vorm_vorm_non_selected_selector.itemClicked.connect(self.clicked_vorm_vorm)
        
        self.setter(self.vorm_textuur_selected_selector, self.vorm_textuur_selected_list)
        self.setter(self.vorm_textuur_non_selected_selector, self.vorm_textuur_non_selected_list)
        #self.vorm_textuur_selected_selector.itemClicked.connect(self.clicked_vorm_textuur)
        #self.vorm_textuur_non_selected_selector.itemClicked.connect(self.clicked_vorm_textuur)
        
        self.setter(self.omtrek_selected_selector, self.omtrek_selected_list)
        self.setter(self.omtrek_non_selected_selector, self.omtrek_non_selected_list)
        #self.omtrek_selected_selector.itemClicked.connect(self.clicked_omtrek)
        #self.omtrek_non_selected_selector.itemClicked.connect(self.clicked_omtrek)
        
        self.setter(self.kleur_selected_selector, self.kleur_selected_list)
        self.setter(self.kleur_non_selected_selector, self.kleur_non_selected_list)
        #self.kleur_selected_selector.itemClicked.connect(self.clicked_kleur)
        #self.kleur_non_selected_selector.itemClicked.connect(self.clicked_kleur)
        
        self.setter(self.efflorescentie_selected_selector, self.efflorescentie_selected_list)
        self.setter(self.efflorescentie_non_selected_selector, self.efflorescentie_non_selected_list)
        #self.efflorescentie_selected_selector.itemClicked.connect(self.clicked_efflorescentie)
        #self.efflorescentie_non_selected_selector.itemClicked.connect(self.clicked_efflorescentie)
        
        print("Set provoke")
        
    def getDifference(self, li1, li2):   
        print("Getting the difference")     
        new_list = []
        
        for item in li2:
            if item not in li1:
                new_list.append(item)
        
        return new_list
    
    def makeList(self, input):
        if isinstance(input,str):
            return [input]
        else:
            return input
 
    def unshow(self):
        self.show_bool = not self.show_bool
        
        if self.show_bool:
            self.show_button.setText("Hide colours")
        else:
            self.show_button.setText("Show colours")
            
        self.reload()
        
    def setter(self, selector, list_in):
        print("In the setter")
        selector.clear()
        print("Cleared")
        if isinstance(list_in, list):         
            for item in self.makeList(list_in):
                if item:
                    selector.addItem(item)
        print("Set up a setter")
        
    def clicked_plaats(self, item):
        thing = item.text()
        print("Clicked plaats: " + thing)
        
        if thing in self.plaats_non_selected_list:
            self.plaats_non_selected_list.remove(thing)
            self.plaats_selected_list.append(thing)
        elif thing in self.plaats_selected_list:
            self.plaats_non_selected_list.append(thing)
            self.plaats_selected_list.remove(thing)
            
        self.set_provoke()
        
    def clicked_not_select(self, item):
        print("Clicked not select")
        thing = item.text()
        print("Clicked " + thing)
        selections = [[self.efflorescentie_non_selected_list,self.efflorescentie_selected_list], 
                      [self.plaats_non_selected_list,self.plaats_selected_list], 
                      [self.rangschikking_non_selected_list,self.rangschikking_selected_list], 
                      [self.omvang_grootte_non_selected_list,self.omvang_grootte_selected_list], 
                      [self.kleur_non_selected_list,self.kleur_selected_list], 
                      [self.omvang_aantal_non_selected_list,self.omvang_aantal_selected_list], 
                      [self.omtrek_non_selected_list,self.omtrek_selected_list], 
                      [self.vorm_textuur_non_selected_list,self.vorm_textuur_selected_list], 
                      [self.vorm_vorm_non_selected_list,self.vorm_vorm_selected_list]]
        
        for selection in selections:
            if thing in selection[0]:
                selection[0].remove(thing)
                selection[1].append(thing)
                print("Preparing to set provoke...")
                self.set_provoke()
                break
                
        
                                           
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
