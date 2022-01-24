# importing various libraries
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QGridLayout, QComboBox, QCheckBox, QStackedWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from matplotlib.backend_bases import MouseButton
import numpy as np
import pandas as pd 
import os

   
# main window
# which inherits QDialog
class Window(QDialog):
       
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        
        print("Starting the application...")
   
        # a figure instance to plot on
        self.figure = plt.figure()
        plt.rc('font', size=25) 
        
        # set the paths
        self.base_path = str(os.path.dirname(os.path.abspath(__file__))) + "/"
        self.path = self.base_path + "Amin_dataset/"
        
        # set lists        
        self.provoke_dict = {   "Plaats" : {            "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Head": ["Scalp", "Face"],
                                                                        "Neck": ["Neck", "Throat"],
                                                                        "Upper extremity": ["Upper_arm", "Lower_arm", "Elbow", "Wrist", "Hand_palm", "Hand_other"],
                                                                        "Torso": ["Chest", "Upper_back", "Shoulders", "Abdomen", "Lower_back", "Groin", "Genitals", "Buttocks"],
                                                                        "Lower extremity": ["Upper_leg", "Knee", "Lower_leg", "Foot_sole", "Foot_other"],
                                                                        "Whole body": ["Whole body"]},
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                             
                                 "Omvang grootte" : {   "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Millar": ["Millar"],
                                                                        "Lenticular": ["Lenticular"],
                                                                        "Nummular": ["Nummular"],
                                                                        "Child palm sized": ["Child palm sized"],
                                                                        "Palm sized": ["Palm_sized"],
                                                                        "Regional": ["Regional"],
                                                                        "Generalised": ["Generalised"]},
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                                 
                                "Omvang aantal" : {     "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "One": ["One"],
                                                                        "Few": ["Few"],
                                                                        "Tens": ["Tens"],
                                                                        "Innumerable": ["Innumerable"]},
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                                
                                "Vorm vorm" : {         "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Polycyclic": ["Polyciclic", "Round", "Oval"],
                                                                        "Polygonal": ["Polygonal", "Rectangle"],
                                                                        "Linear": ["Linear", "Gyrated"],
                                                                        "Dendritic": ["Dendritic"],
                                                                        "Capricious" : ["Capricious"]},
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                                
                                "Vorm textuur" : {      "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Not raised": ["Not raised"],
                                                                        "Flat": ["Flat", "Bumpy", "Pleated", "Wrinkled", "Verrucous", "Raised edge"],
                                                                        "Hemispheric": ["Hemispheric", "Dome-shaped", "Dome-shaped with crater"],
                                                                        "Sharp": ["Sharp"],
                                                                        "Stemmed" : ["Stemmed"]},
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                                
                                "Omtrek" : {            "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Sharp": ["Sharp"],
                                                                        "Medium sharp": ["Medium sharp"],
                                                                        "Unsharp": ["Unsharp"]},
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                                
                                "Kleur" : {             "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Skin coloured": ["Skin coloured"],
                                                                        "Red": ["Light red", "Dark red", "Bright red"],
                                                                        "Brown": ["Brown", "Light brown", "Dark brown"],
                                                                        "Abnormal colours" : [ "Black", "Pale or white", "Yellow", "Green", "Orange", "Purple", "Blue"]},
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                                
                            "Efflorescentie" : {        "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Squama": ["Squama"],
                                                                        "Bloeduitstorting": ["Ecchymosis", "Teleangiectasie", "Purpura", "Petechiae"],
                                                                        "Skin defect": ["Vulnus", "Rhagade", "Erosion", "Excoriation", "Fistula", "Ulcus"],
                                                                        "Skin thickening" : ["Tumor", "Vegetation", "Hyperkeratose", "Lichenification", "Urtica", "Plaque"],
                                                                        "Bump on skin" : ["Abces", "Pusula", "Bulla", "Vesicula", "Cyst", "Comedo", "Nodus or papula", "Nodulus"],
                                                                        "Unraised defects" : ["Dyschromia", "Macula", "Erythema", "Craquelé"],
                                                                        "Crusta" : ["Crusta"]}, 
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                            
                            "Rangschikking groep" : {   "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Solitary": ["Solitary"],
                                                                        "Grouped": ["Discrete group", "Diffuse group", "Confluent group"]}, 
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                            
                            "Rangschikking plaats" : {  "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Regional": ["Regional", "Segmental", "Ptychotropic"],
                                                                        "Generalised": ["Generalised", "Universal"],
                                                                        "Follicular": ["Follicular"]}, 
                                                        "Selected" :  [],
                                                        "Not_selected": []},
                            
                            "Rangschikking vorm" : {    "data_dict" : { "Undetermined" : ["Undetermined"],
                                                                        "Linear": ["Linear", "Arciform"], 
                                                                        "Annular": ["Annular", "Circinair", "Concentric", "Cocardic"],
                                                                        "Corymbiform": ["Corymbiform", "En bouquet"],
                                                                        "Reticular" : ["Reticular"]}, 
                                                        "Selected" :  [],
                                                        "Not_selected": []},}
        
        
        # set the excel  
        self.wb = pd.read_excel(self.base_path + "fitzpatrick17k-amin-annotation.xlsx") 
        self.wb.is_copy = False
        
        # set the coordinates, array and counters
        self.x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
        self.reg_array = np.zeros((10,10))
        self.im = 0
        self.show_bool = True
        self.checkbox_list = []
   
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
        
        # Creating the PROVOKE label box
        provoke_label_box = QGroupBox("PROVOKE - labels")
        provoke_label_layout = QVBoxLayout()
        provoke_label_box.setLayout(provoke_label_layout)   
        
        self.plaats_label = QLabel("Plaats: empty")
        self.rangschikking_label = QLabel("Rangschikking: empty")
        self.omvang_label = QLabel("Omvang: empty")
        self.vorm_label = QLabel("Vorm: empty")
        self.omtrek_label = QLabel("Omtrek: empty")
        self.kleur_label = QLabel("Kleur: empty")
        self.efflorescentie_label = QLabel("Efflorescentie: empty")
        
        self.label_dict ={"Plaats" : self.plaats_label, 
                     "Rangschikking" : self.rangschikking_label, 
                     "Omvang" : self.omvang_label, 
                     "Vorm": self.vorm_label, 
                     "Omtrek" : self.omtrek_label, 
                     "Kleur" : self.kleur_label, 
                     "Efflorescentie" : self.efflorescentie_label} 
        
        for key in self.label_dict.keys():
            provoke_label_layout.addWidget(self.label_dict[key])   
        
        # CREATING THE INSTURCTIONS BOX
        instructions_box = QGroupBox("Instructions and PROVOKE")
        instructions_layout = QVBoxLayout()
        instructions_box.setLayout(instructions_layout)        
        
        instructions_layout.addWidget(instructions_box)
        
        ## Adding the instructions
        instructions_layout.addWidget(QLabel("Left (blue) is background, right (red) is lesion"))        
        
        # Creating an empty widget
        self.empty_box = QGroupBox()
        self.empty_layout = QVBoxLayout()
        
        # CREATING THE PROVOKE BOX
        provoke_box = QGroupBox("PROVOKE controls")
        self.provoke_layout = QHBoxLayout()
        provoke_box.setLayout(self.provoke_layout)
        ## CREATING THE INDIVIDUAL PROVOKE BOXES AND ADDING PROVOKE
        ### Plaats        
        self.plaats_box = QGroupBox("Plaats")
        self.plaats_layout = QVBoxLayout()
        self.plaats_combobox = QComboBox()
        self.plaats_stacked = QStackedWidget()
        
        self.plaats_undetermined_box = QGroupBox()
        self.plaats_undetermined_layout = QVBoxLayout()
        self.head_box = QGroupBox()
        self.head_layout = QVBoxLayout()
        self.neck_box = QGroupBox()
        self.neck_layout = QVBoxLayout()
        self.upper_extremity_box = QGroupBox()
        self.upper_extremity_layout = QVBoxLayout()
        self.torso_box = QGroupBox()
        self.torso_layout = QVBoxLayout()
        self.lower_extremity_box = QGroupBox()
        self.lower_extremity_layout = QVBoxLayout() 
        self.whole_body_box = QGroupBox()
        self.whole_body_layout = QVBoxLayout()      
        
        self.build_combobox(self.plaats_combobox, self.provoke_dict["Plaats"]["data_dict"].keys())
        
        self.plaats_box.setLayout(self.plaats_layout)
        self.plaats_layout.addWidget(self.plaats_combobox)    
        self.plaats_layout.addWidget(self.plaats_stacked) 
        self.provoke_layout.addWidget(self.plaats_box)   
        ### Rangschikking
        rangschikking_box = QGroupBox("Rangschikking")
        rangschikking_layout = QHBoxLayout()
        rangschikking_left_box = QGroupBox()
        rangschikking_left_layout = QVBoxLayout()
        rangschikking_layout.addWidget(rangschikking_left_box)
        rangschikking_left_box.setLayout(rangschikking_left_layout)
        rangschikking_box.setLayout(rangschikking_layout)
        self.provoke_layout.addWidget(rangschikking_box)
        
        ### Rangschikking groep
        self.rangschikking_groep_box = QGroupBox("Rangschikking groep")
        self.rangschikking_groep_layout = QVBoxLayout()
        self.rangschikking_groep_combobox = QComboBox()
        self.rangschikking_groep_stacked = QStackedWidget()
        
        self.rangschikking_groep_undetermined_box = QGroupBox()
        self.rangschikking_groep_undetermined_layout = QVBoxLayout()
        self.solitary_box = QGroupBox()
        self.solitary_layout = QVBoxLayout()
        self.grouped_box = QGroupBox()
        self.grouped_layout = QVBoxLayout()              
        
        self.build_combobox(self.rangschikking_groep_combobox, self.provoke_dict["Rangschikking groep"]["data_dict"].keys())
        
        self.rangschikking_groep_box.setLayout(self.rangschikking_groep_layout)
        self.rangschikking_groep_layout.addWidget(self.rangschikking_groep_combobox)    
        self.rangschikking_groep_layout.addWidget(self.rangschikking_groep_stacked)
        ### Rangschikking plaats
        self.rangschikking_plaats_box = QGroupBox("Rangschikking plaats")
        self.rangschikking_plaats_layout = QVBoxLayout()
        self.rangschikking_plaats_combobox = QComboBox()
        self.rangschikking_plaats_stacked = QStackedWidget()
        
        self.rangschikking_plaats_undetermined_box = QGroupBox()
        self.rangschikking_plaats_undetermined_layout = QVBoxLayout()
        self.rangschikking_regional_box = QGroupBox()
        self.rangschikking_regional_layout = QVBoxLayout()  
        self.generalised_box = QGroupBox()
        self.generalised_layout = QVBoxLayout() 
        self.follicular_box = QGroupBox()
        self.follicular_layout = QVBoxLayout()        
        
        self.build_combobox(self.rangschikking_plaats_combobox, self.provoke_dict["Rangschikking plaats"]["data_dict"].keys())
        
        self.rangschikking_plaats_box.setLayout(self.rangschikking_plaats_layout)
        self.rangschikking_plaats_layout.addWidget(self.rangschikking_plaats_combobox)    
        self.rangschikking_plaats_layout.addWidget(self.rangschikking_plaats_stacked)
        ### Rangschikking vorm
        self.rangschikking_vorm_box = QGroupBox("Rangschikking vorm")
        self.rangschikking_vorm_layout = QVBoxLayout()
        self.rangschikking_vorm_combobox = QComboBox()
        self.rangschikking_vorm_stacked = QStackedWidget()
        
        self.rangschikking_vorm_undetermined_box = QGroupBox()
        self.rangschikking_vorm_undetermined_layout = QVBoxLayout()
        self.linear_box = QGroupBox()
        self.linear_layout = QVBoxLayout()
        self.annular_box = QGroupBox()
        self.annular_layout = QVBoxLayout() 
        self.corymbiform_box = QGroupBox()
        self.corymbiform_layout = QVBoxLayout() 
        self.reticular_box = QGroupBox()
        self.reticular_layout = QVBoxLayout()         
        
        self.build_combobox(self.rangschikking_vorm_combobox, self.provoke_dict["Rangschikking vorm"]["data_dict"].keys())
        
        self.rangschikking_vorm_box.setLayout(self.rangschikking_vorm_layout)
        self.rangschikking_vorm_layout.addWidget(self.rangschikking_vorm_combobox)    
        self.rangschikking_vorm_layout.addWidget(self.rangschikking_vorm_stacked)
        
        ### Rangschikking totaal
        rangschikking_left_layout.addWidget(self.rangschikking_groep_box)
        rangschikking_left_layout.addWidget(self.rangschikking_plaats_box)
        rangschikking_layout.addWidget(self.rangschikking_vorm_box)
        
        ### Omvang 
        omvang_box = QGroupBox("Omvang en omtrek")
        omvang_layout = QVBoxLayout()
        omvang_box.setLayout(omvang_layout)
        self.provoke_layout.addWidget(omvang_box)
        #### Omvang grootte
        self.omvang_grootte_box = QGroupBox("Omvang grootte")
        self.omvang_grootte_layout = QVBoxLayout()
        self.omvang_grootte_combobox = QComboBox()
        self.omvang_grootte_stacked = QStackedWidget()
        
        self.omvang_grootte_undetermined_box = QGroupBox()
        self.omvang_grootte_undetermined_layout = QVBoxLayout()
        self.millar_box = QGroupBox()
        self.millar_layout = QVBoxLayout()  
        self.lenticular_box = QGroupBox()
        self.lenticular_layout = QVBoxLayout()  
        self.nummular_box = QGroupBox()
        self.nummular_layout = QVBoxLayout()  
        self.child_palm_sized_box = QGroupBox()
        self.child_palm_sized_layout = QVBoxLayout()  
        self.palm_sized_box = QGroupBox()
        self.palm_sized_layout = QVBoxLayout()  
        self.regional_box = QGroupBox()
        self.regional_layout = QVBoxLayout()  
        self.generalised_box = QGroupBox()
        self.generalised_layout = QVBoxLayout()        
        
        self.build_combobox(self.omvang_grootte_combobox, self.provoke_dict["Omvang grootte"]["data_dict"].keys())
        
        self.omvang_grootte_box.setLayout(self.omvang_grootte_layout)
        self.omvang_grootte_layout.addWidget(self.omvang_grootte_combobox)    
        self.omvang_grootte_layout.addWidget(self.omvang_grootte_stacked)
        #### Omvang aantal
        self.omvang_aantal_box = QGroupBox("Omvang aantal")
        self.omvang_aantal_layout = QVBoxLayout()
        self.omvang_aantal_combobox = QComboBox()
        self.omvang_aantal_stacked = QStackedWidget()
        
        self.omvang_aantal_undetermined_box = QGroupBox()
        self.omvang_aantal_undetermined_layout = QVBoxLayout()
        self.one_box = QGroupBox()
        self.one_layout = QVBoxLayout()
        self.few_box = QGroupBox()
        self.few_layout = QVBoxLayout()    
        self.tens_box = QGroupBox()
        self.tens_layout = QVBoxLayout()    
        self.innumerable_box = QGroupBox()
        self.innumerable_layout = QVBoxLayout()              
        
        self.build_combobox(self.omvang_aantal_combobox, self.provoke_dict["Omvang aantal"]["data_dict"].keys())
        
        self.omvang_aantal_box.setLayout(self.omvang_aantal_layout)
        self.omvang_aantal_layout.addWidget(self.omvang_aantal_combobox)    
        self.omvang_aantal_layout.addWidget(self.omvang_aantal_stacked)
        
        omvang_layout.addWidget(self.omvang_aantal_box)
        omvang_layout.addWidget(self.omvang_grootte_box)
        
        ### Vorm 
        vorm_box = QGroupBox("Vorm")
        vorm_layout = QVBoxLayout()
        vorm_box.setLayout(vorm_layout)
        self.provoke_layout.addWidget(vorm_box)
        #### Vorm vorm
        self.vorm_vorm_box = QGroupBox("Vorm vorm")
        self.vorm_vorm_layout = QVBoxLayout()
        self.vorm_vorm_combobox = QComboBox()
        self.vorm_vorm_stacked = QStackedWidget()
        
        self.vorm_vorm_undetermined_box = QGroupBox()
        self.vorm_vorm_undetermined_layout = QVBoxLayout()  
        self.polycyclic_box = QGroupBox()
        self.polycyclic_layout = QVBoxLayout()
        self.polygonal_box = QGroupBox()
        self.polygonal_layout = QVBoxLayout()   
        self.linear_vorm_box = QGroupBox()
        self.linear_vorm_layout = QVBoxLayout()   
        self.dendritic_box = QGroupBox()
        self.dendritic_layout = QVBoxLayout()     
        self.capricious_box = QGroupBox()
        self.capricious_layout = QVBoxLayout()    
        
        self.build_combobox(self.vorm_vorm_combobox, self.provoke_dict["Vorm vorm"]["data_dict"].keys())
        
        self.vorm_vorm_box.setLayout(self.vorm_vorm_layout)
        self.vorm_vorm_layout.addWidget(self.vorm_vorm_combobox)    
        self.vorm_vorm_layout.addWidget(self.vorm_vorm_stacked)
        #### Vorm textuur
        self.vorm_textuur_box = QGroupBox("Vorm textuur")
        self.vorm_textuur_layout = QVBoxLayout()
        self.vorm_textuur_combobox = QComboBox()
        self.vorm_textuur_stacked = QStackedWidget()
        
        self.vorm_textuur_undetermined_box = QGroupBox()
        self.vorm_textuur_undetermined_layout = QVBoxLayout()  
        self.not_raised_box = QGroupBox()
        self.not_raised_layout = QVBoxLayout()
        self.flat_box = QGroupBox()
        self.flat_layout = QVBoxLayout()   
        self.hemispheric_box = QGroupBox()
        self.hemispheric_layout = QVBoxLayout()   
        self.sharp_vorm_box = QGroupBox()
        self.sharp_vorm_layout = QVBoxLayout()     
        self.stemmed_box = QGroupBox()
        self.stemmed_layout = QVBoxLayout()      
        
        self.build_combobox(self.vorm_textuur_combobox, self.provoke_dict["Vorm textuur"]["data_dict"].keys())
        
        self.vorm_textuur_box.setLayout(self.vorm_textuur_layout)
        self.vorm_textuur_layout.addWidget(self.vorm_textuur_combobox)    
        self.vorm_textuur_layout.addWidget(self.vorm_textuur_stacked)  
        
        vorm_layout.addWidget(self.vorm_vorm_box)
        vorm_layout.addWidget(self.vorm_textuur_box)
        
        ### Omtrek 
        self.omtrek_box = QGroupBox("Omtrek")
        self.omtrek_layout = QVBoxLayout()
        self.omtrek_combobox = QComboBox()
        self.omtrek_stacked = QStackedWidget()
        
        self.omtrek_undetermined_box = QGroupBox()
        self.omtrek_undetermined_layout = QVBoxLayout()  
        self.sharp_box = QGroupBox()
        self.sharp_layout = QVBoxLayout()
        self.medium_sharp_box = QGroupBox()
        self.medium_sharp_layout = QVBoxLayout()   
        self.unsharp_box = QGroupBox()
        self.unsharp_layout = QVBoxLayout()      
        
        self.build_combobox(self.omtrek_combobox, self.provoke_dict["Omtrek"]["data_dict"].keys())
        
        self.omtrek_box.setLayout(self.omtrek_layout)
        self.omtrek_layout.addWidget(self.omtrek_combobox)    
        self.omtrek_layout.addWidget(self.omtrek_stacked) 
        self.provoke_layout.addWidget(self.omtrek_box) 
        ### Kleur 
        self.kleur_box = QGroupBox("Kleur")
        self.kleur_layout = QVBoxLayout()
        self.kleur_combobox = QComboBox()
        self.kleur_stacked = QStackedWidget()
        
        self.kleur_undetermined_box = QGroupBox()
        self.kleur_undetermined_layout = QVBoxLayout()  
        self.skin_coloured_box = QGroupBox()
        self.skin_coloured_layout = QVBoxLayout()
        self.red_box = QGroupBox()
        self.red_layout = QVBoxLayout()   
        self.brown_box = QGroupBox()
        self.brown_layout = QVBoxLayout()   
        self.abnormal_colours_box = QGroupBox()
        self.abnormal_colours_layout = QVBoxLayout()        
        
        self.build_combobox(self.kleur_combobox, self.provoke_dict["Kleur"]["data_dict"].keys())
        
        self.kleur_box.setLayout(self.kleur_layout)
        self.kleur_layout.addWidget(self.kleur_combobox)    
        self.kleur_layout.addWidget(self.kleur_stacked) 
        self.provoke_layout.addWidget(self.kleur_box)   
        ### Efflorescentie
        self.efflorescentie_box = QGroupBox("Efflorescentie")
        self.efflorescentie_layout = QVBoxLayout()
        self.efflorescentie_combobox = QComboBox()
        self.efflorescentie_stacked = QStackedWidget()
        
        self.efflorescentie_undetermined_box = QGroupBox()
        self.efflorescentie_undetermined_layout = QVBoxLayout()
        self.squama_box = QGroupBox()
        self.squama_layout = QVBoxLayout()
        self.bloeduistorting_box = QGroupBox()
        self.bloeduistorting_layout = QVBoxLayout() 
        self.skin_defect_box = QGroupBox()
        self.skin_defect_layout = QVBoxLayout() 
        self.skin_thickening_box = QGroupBox()
        self.skin_thickening_layout = QVBoxLayout() 
        self.bump_on_skin_box = QGroupBox()
        self.bump_on_skin_layout = QVBoxLayout() 
        self.unraised_defects_box = QGroupBox()
        self.unraised_defects_layout = QVBoxLayout() 
        self.crusta_box = QGroupBox()
        self.crusta_layout = QVBoxLayout()     
        
        self.build_combobox(self.efflorescentie_combobox, self.provoke_dict["Efflorescentie"]["data_dict"].keys())
        
        self.efflorescentie_box.setLayout(self.efflorescentie_layout)
        self.efflorescentie_layout.addWidget(self.efflorescentie_combobox)    
        self.efflorescentie_layout.addWidget(self.efflorescentie_stacked) 
        self.provoke_layout.addWidget(self.efflorescentie_box)   
        
        # Widget dict
        self.widget_dict = { "Plaats" : {               "Undetermined" : [self.plaats_undetermined_box, self.plaats_undetermined_layout, self.plaats_stacked],
                                                        "Head" : [self.head_box, self.head_layout, self.plaats_stacked],
                                                        "Neck" : [self.neck_box, self.neck_layout, self.plaats_stacked],
                                                        "Upper extremity" : [self.upper_extremity_box, self.upper_extremity_layout, self.plaats_stacked],
                                                        "Torso": [self.torso_box, self.torso_layout, self.plaats_stacked],
                                                        "Lower extremity" : [self.lower_extremity_box, self.lower_extremity_layout, self.plaats_stacked],
                                                        "Whole body": [self.whole_body_box, self.whole_body_layout, self.plaats_stacked]},
                             "Kleur" : {                "Undetermined" : [self.kleur_undetermined_box, self.kleur_undetermined_layout, self.kleur_stacked],
                                                        "Skin coloured" : [self.skin_coloured_box, self.skin_coloured_layout, self.kleur_stacked],
                                                        "Red" : [self.red_box, self.red_layout, self.kleur_stacked],
                                                        "Brown" : [self.brown_box, self.brown_layout, self.kleur_stacked],
                                                        "Abnormal colours" : [self.abnormal_colours_box, self.abnormal_colours_layout, self.kleur_stacked]},
                             "Efflorescentie" : {       "Undetermined" : [self.efflorescentie_undetermined_box, self.efflorescentie_undetermined_layout, self.efflorescentie_stacked],
                                                        "Squama" : [self.squama_box, self.squama_layout, self.efflorescentie_stacked],
                                                        "Bloeduitstorting" : [self.bloeduistorting_box, self.bloeduistorting_layout, self.efflorescentie_stacked],
                                                        "Skin defect" : [self.skin_defect_box, self.skin_defect_layout, self.efflorescentie_stacked],
                                                        "Skin thickening" : [self.skin_thickening_box, self.skin_thickening_layout, self.efflorescentie_stacked],
                                                        "Bump on skin" : [self.bump_on_skin_box, self.bump_on_skin_layout, self.efflorescentie_stacked],
                                                        "Unraised defects" : [self.unraised_defects_box, self.unraised_defects_layout, self.efflorescentie_stacked],
                                                        "Crusta" : [self.crusta_box, self.crusta_layout, self.efflorescentie_stacked]},
                             "Omvang grootte" : {       "Undetermined" : [self.omvang_grootte_undetermined_box, self.omvang_grootte_undetermined_layout, self.omvang_grootte_stacked],
                                                        "Millar" : [self.millar_box, self.millar_layout, self.omvang_grootte_stacked],
                                                        "Lenticular" : [self.lenticular_box, self.lenticular_layout, self.omvang_grootte_stacked],
                                                        "Nummular" : [self.nummular_box, self.nummular_layout, self.omvang_grootte_stacked],
                                                        "Child palm sized" : [self.child_palm_sized_box, self.child_palm_sized_layout, self.omvang_grootte_stacked],
                                                        "Palm sized" : [self.palm_sized_box, self.palm_sized_layout, self.omvang_grootte_stacked],
                                                        "Regional" : [self.regional_box, self.regional_layout, self.omvang_grootte_stacked],
                                                        "Generalised" : [self.generalised_box, self.generalised_layout, self.omvang_grootte_stacked]},
                             "Omvang aantal" : {        "Undetermined" : [self.omvang_aantal_undetermined_box, self.omvang_aantal_undetermined_layout, self.omvang_aantal_stacked],
                                                        "One" : [self.one_box, self.one_layout, self.omvang_aantal_stacked],
                                                        "Few" : [self.few_box, self.few_layout, self.omvang_aantal_stacked],
                                                        "Tens" : [self.tens_box, self.tens_layout, self.omvang_aantal_stacked],
                                                        "Innumerable" : [self.innumerable_box, self.innumerable_layout, self.omvang_aantal_stacked]},
                             "Omtrek" : {               "Undetermined" : [self.omtrek_undetermined_box, self.omtrek_undetermined_layout, self.omtrek_stacked],
                                                        "Sharp" : [self.sharp_box, self.sharp_layout, self.omtrek_stacked],
                                                        "Medium sharp" : [self.medium_sharp_box, self.medium_sharp_layout, self.omtrek_stacked],
                                                        "Unsharp" : [self.unsharp_box, self.unsharp_layout, self.omtrek_stacked]},
                             "Vorm vorm" : {            "Undetermined" : [self.vorm_vorm_undetermined_box, self.vorm_vorm_undetermined_layout, self.vorm_vorm_stacked],
                                                        "Polycyclic" : [self.polycyclic_box, self.polycyclic_layout, self.vorm_vorm_stacked],
                                                        "Polygonal" : [self.polygonal_box, self.polygonal_layout, self.vorm_vorm_stacked],
                                                        "Linear" : [self.linear_vorm_box, self.linear_vorm_layout, self.vorm_vorm_stacked],
                                                        "Dendritic" : [self.dendritic_box, self.dendritic_layout, self.vorm_vorm_stacked],
                                                        "Capricious" : [self.capricious_box, self.capricious_layout, self.vorm_vorm_stacked]},
                             "Vorm textuur" : {         "Undetermined" : [self.vorm_textuur_undetermined_box, self.vorm_textuur_undetermined_layout, self.vorm_textuur_stacked],
                                                        "Not raised" : [self.not_raised_box, self.not_raised_layout, self.vorm_textuur_stacked],
                                                        "Flat" : [self.flat_box, self.flat_layout, self.vorm_textuur_stacked],
                                                        "Hemispheric" : [self.hemispheric_box, self.hemispheric_layout, self.vorm_textuur_stacked],
                                                        "Sharp" : [self.sharp_vorm_box, self.sharp_vorm_layout, self.vorm_textuur_stacked],
                                                        "Stemmed" : [self.stemmed_box, self.stemmed_layout, self.vorm_textuur_stacked]},
                             "Rangschikking groep" : {  "Undetermined" : [self.rangschikking_groep_undetermined_box, self.rangschikking_groep_undetermined_layout, self.rangschikking_groep_stacked],
                                                        "Solitary" : [self.solitary_box, self.solitary_layout, self.rangschikking_groep_stacked],
                                                        "Grouped" : [self.grouped_box, self.grouped_layout, self.rangschikking_groep_stacked]},
                             "Rangschikking plaats" : { "Undetermined" : [self.rangschikking_plaats_undetermined_box, self.rangschikking_plaats_undetermined_layout, self.rangschikking_plaats_stacked],
                                                        "Regional" : [self.rangschikking_regional_box, self.rangschikking_regional_layout, self.rangschikking_plaats_stacked],
                                                        "Generalised" : [self.generalised_box, self.generalised_layout, self.rangschikking_plaats_stacked],
                                                        "Follicular" : [self.follicular_box, self.follicular_layout, self.rangschikking_plaats_stacked]},
                             "Rangschikking vorm" : {   "Undetermined" : [self.rangschikking_vorm_undetermined_box, self.rangschikking_vorm_undetermined_layout, self.rangschikking_vorm_stacked],
                                                        "Linear" : [self.linear_box, self.linear_layout, self.rangschikking_vorm_stacked],
                                                        "Annular" : [self.annular_box, self.annular_layout, self.rangschikking_vorm_stacked],
                                                        "Corymbiform" : [self.corymbiform_box, self.corymbiform_layout, self.rangschikking_vorm_stacked],
                                                        "Reticular" : [self.reticular_box, self.reticular_layout, self.rangschikking_vorm_stacked]}
                                                        }
              
        
        for key in self.widget_dict.keys():
            self.build_stack(key)    
        
        # MAKING THE CANVAS LAYOUT LOOK NICE
        ## Creating the box for the controls and instructions
        right_layout = QVBoxLayout()
        right_box = QGroupBox()
        right_box.setLayout(right_layout)
        ## Creating the box for the canvas and the controls
        main_layout = QHBoxLayout()
        main_box = QGroupBox()
        main_box.setLayout(main_layout)
        main_layout.addWidget(provoke_label_box)
        main_layout.addWidget(self.canvas)
        main_layout.addWidget(right_box)
        
        # ADDING THE BOXES TO THE MAIN LAYOUT
        window_layout.addWidget(main_box,80)
        right_layout.addWidget(instructions_box)
        right_layout.addWidget(button_box)
        window_layout.addWidget(provoke_box, 20)
        ## Setting the main layout
        self.setLayout(window_layout)
        
        print("Application started!")
        
        self.combobox_dict = {"Plaats" : self.plaats_combobox,
                             "Kleur" : self.kleur_combobox,
                             "Efflorescentie" : self.efflorescentie_combobox,
                             "Omvang grootte" : self.omvang_grootte_combobox,
                             "Omvang aantal" : self.omvang_aantal_combobox,
                             "Omtrek" : self.omtrek_combobox,
                             "Vorm vorm" : self.vorm_vorm_combobox,
                             "Vorm textuur" : self.vorm_textuur_combobox,
                             "Rangschikking groep" : self.rangschikking_groep_combobox,
                             "Rangschikking plaats" : self.rangschikking_plaats_combobox,
                             "Rangschikking vorm" : self.rangschikking_vorm_combobox}
        
        # Start 
        self.init_step()
        self.showMaximized()
        
    def build_combobox(self, combobox, list):        
        for item in list:
            combobox.addItem(item)
        
        combobox.currentTextChanged.connect(self.changed_text)
        
    def build_stack(self, provoke):
        chapter_dict = self.widget_dict[provoke]
        
        keys = chapter_dict.keys()
        
        for key in keys:
            box = chapter_dict[key][0]
            layout = chapter_dict[key][1]
            stack = chapter_dict[key][2]
            content = self.provoke_dict[provoke]["data_dict"][key]
                      
            for item in content:
                checkbox = QCheckBox(item)
                layout.addWidget(checkbox)
                checkbox.toggled.connect(self.clicked)
                self.checkbox_list.append([provoke, key, checkbox, item])
                
            box.setLayout(layout)    
            stack.addWidget(box)
             
    def changed_text(self):
        key = self.sender().currentText()
        parent = self.sender().parent().title()
        
        # print("Key: " + str(parent))
        # print("Key: " + str(key))
        
        self.widget_dict[parent][key][2].setCurrentWidget(self.widget_dict[parent][key][0])
            
    def clicked(self):
        key = self.sender().text()
        parent = self.sender().parent().parent().parent().title()
                
        # print(self.sender().parent().parent().parent().title())
        # print(self.sender().text() + " is " + str(self.sender().isChecked()))
        
        if self.sender().isChecked():
            self.provoke_dict[parent]["Selected"].append(key)
        elif not self.sender().isChecked() and key in self.provoke_dict[parent]["Selected"]:
            self.provoke_dict[parent]["Selected"].remove(key)
            
        self.update_labels()
    
    def update_labels(self):
        
        self.label_dict["Plaats"].setText("Plaats: " + str(self.provoke_dict["Plaats"]["Selected"]))
        self.label_dict["Rangschikking"].setText("Rangschikking: " + str(self.provoke_dict["Rangschikking groep"]["Selected"]) 
                                                              + str(self.provoke_dict["Rangschikking plaats"]["Selected"])
                                                              + str(self.provoke_dict["Rangschikking vorm"]["Selected"]))
        self.label_dict["Omvang"].setText("Omvang: " + str(self.provoke_dict["Omvang grootte"]["Selected"])
                                                + str(self.provoke_dict["Omvang aantal"]["Selected"]))
        self.label_dict["Vorm"].setText("Vorm: " + str(self.provoke_dict["Vorm vorm"]["Selected"])
                                            + str(self.provoke_dict["Vorm textuur"]["Selected"]))
        self.label_dict["Omtrek"].setText("Omtrek: " + str(self.provoke_dict["Omtrek"]["Selected"]))
        self.label_dict["Kleur"].setText("Kleur: " + str(self.provoke_dict["Kleur"]["Selected"]))
        self.label_dict["Efflorescentie"].setText("Efflorescentie: " + str(self.provoke_dict["Efflorescentie"]["Selected"]))
    
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
        print("Saving and resetting the figure...")
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
        
        self.ax.set_xticks(self.x, labels="")
        self.ax.set_yticks(self.x, labels="")        
        self.ax.grid(True)
        
        self.ax.figure.canvas.mpl_connect('button_press_event', self.draw_colours)
        
        # Adding the colours
        self.check_colours()
        self.check_provoke()
        
        # refresh canvas
        self.canvas.draw()
        
        print("IM_" + str(self.im) + ": Image rendered")
        
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
                        
        print("IM_" + str(self.im) + ": Colours drawn")
   
    def save_colours_local(self):
        reg_array_reshaped_list = self.reg_array.reshape((100)).tolist()
        self.wb['Interest_boxes'][self.im - 1] = str(reg_array_reshaped_list)
        
        print("IM_" + str(self.im) + ": Colours saved")
        
    def close_app(self):
        self.save_and_reset()
        print("Trying to save to Excel...")
        self.wb.to_excel(self.base_path + "fitzpatrick17k-amin-annotation.xlsx")
        print("Saved to Excel")
        print("Closing application...")
        self.close()
        print("Application closed correctly!")
        
    def check_colours(self):        
        interest_box = self.wb['Interest_boxes'][self.im - 1]
        
        if isinstance(interest_box,str) and '[' in interest_box:
            print("IM_" + str(self.im) + ": Colours retrieved")
            
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
                
        for key in self.provoke_dict.keys():
            self.wb[key][self.im - 1] = str(self.provoke_dict[key]["Selected"])
        
        print("IM_" + str(self.im) + ": PROVOKE saved")
        
        for checkbox in self.checkbox_list:
            checkbox[2].setChecked(False)
            
        for key in self.provoke_dict.keys():
            self.provoke_dict[key]["Selected"] = []
    
    def check_provoke(self):
        
        for key in self.provoke_dict.keys():
            provoke_temp = self.wb[key][self.im - 1]
            if isinstance(provoke_temp,str) and len(eval(str(provoke_temp))) > 0: 
                self.update_checkboxes(eval(str(provoke_temp)),key)
                print("IM_" + str(self.im) + ": " + str(key) + " retrieved")
            else:
                self.provoke_dict[key]["Selected"] = []
                print("IM_" + str(self.im) + ": no " + str(key) + " found")
                
        print("IM_" + str(self.im) + ": PROVOKE set")
        
    def update_checkboxes(self, new_dict,key):
        for item in new_dict:
            for checkbox in self.checkbox_list:
                if checkbox[0] == key and checkbox[3] == item:
                    checkbox[2].setChecked(True)
                    self.combobox_dict[checkbox[0]].setCurrentText(checkbox[1])
                                            
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
