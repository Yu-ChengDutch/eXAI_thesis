import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd


def initialize():
    plt.suptitle("Right = lesion \n left = background")
    plt.subplots_adjust(bottom=0.2)
    plt.xticks(ticks=x)
    plt.yticks(ticks=x)


class Index:
    
    global reg_array
    
    im = 0
    
    def next(self, event, ):
        global reg_array
        
        # Save the data to local representation of Excel file
        print("Save the following reg_array to " + 'IM_'+ str(self.im) +  ": ")
        print(reg_array)
        
        reg_array_reshaped_list = reg_array.reshape((100)).tolist()
        
        wb['Interest_boxes'][self.im - 1] = str(reg_array_reshaped_list)
        
        # Reset things    
        self.im += 1
        ax_image.clear()
        reg_array[reg_array != 0] = 0
        
        # Draw the picture
        img = mpimg.imread(path + 'IM_'+ str(self.im) + '.jpg')
        imgplot = ax_image.imshow(img, extent=[0, 50, 0, 50])
        
        ax_image.set_xticks(x)
        ax_image.set_yticks(x)
        ax_image.grid(True)
        
        ax_image.draw()
        
        # Visual reader
        if isinstance(wb['Interest_boxes'][self.im - 1],str) and '[' in wb['Interest_boxes'][self.im - 1]:
            print("Found the following coloration")
            
            reg_array = np.asarray(wb['Interest_boxes'][self.im - 1].strip("[").strip("]").split(",")).reshape((10,10)).astype(float)
            
            print(reg_array)
            
            ## Visual iterator
            for r in range(0,9):
                for c in range(0,9):
                    if reg_array[r,c] != 0:
                        value = reg_array[r,c]
                        x_pos = x[c + 1] - 5
                        y_pos = x[10 - r] - 5
                        if value == 10.0:
                            # Lesion
                            rec_col = 'red'
                        elif value == -10.0:
                            # Background
                            rec_col = 'blue'
                            
                        ax_image.add_patch(Rectangle((x_pos, y_pos), width=5, height=5, color=rec_col, alpha=0.2))  
                        ax_image.figure.canvas.draw()
                        
        
        fig.suptitle('IM_'+ str(self.im))
        
        print("Now working on IM_" + str(self.im))
                
        
    def prev(self, event):
        self.im -= 1

        img = mpimg.imread(path + 'IM_'+ str(self.im) + '.jpg')
        imgplot = ax_image.imshow(img, extent=[0, 50, 0, 50])
        plt.draw()
        
    def close(self, event):
        # Save stuff to the actual Excel file
        wb.to_excel(base_path + "fitzpatrick17k-amin-annotation.xlsx")
        # Close window
        plt.close('all')
        # Print out 
        print("Saved to Excel")
 
   
class Visual_annotator(object):
    def __init__(self):
        self.ax = plt.gca()
        # self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        # self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        
        def redraw():
            self.ax.clear()
        
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
            
            for i in range(0, 8):
                if x_co < x[i]:
                    x_pos = x[i] - 5
                    col = i - 1
                    break
                else:
                    i += 1
                
            z = 0
            
            for z in range(0, 11):
                if y_co < x[z]:
                    y_pos = x[z] - 5
                    row = 10 - z
                    print(row)
                    break
                else:
                    z += 1
            
            print(row)
            print(col)
            
            reg_array[row, col] = value
                
            self.ax.add_patch(Rectangle((x_pos, y_pos), width=5, height=5, color=rec_col, alpha=0.2))  
            self.ax.figure.canvas.draw()                  
            

# Setting everything that has to be set
base_path = "C:/Users/zmezl/Desktop/University/AI/Thesis/eXAI_thesis/"
path = base_path + "Amin_dataset/"
fig = plt.figure()
grid = gridspec.GridSpec(3,1)

ax_image = fig.add_subplot(grid[0])
ax_buttons = fig.add_subplot(grid[1])
ax_provoke = fig.add_subplot(grid[2])

reg_array = np.zeros((10,10))
wb = pd.read_excel(base_path + "fitzpatrick17k-amin-annotation.xlsx") 
a = Visual_annotator()
x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
callback = Index()    

initialize() 


axprev = plt.axes([0.5, 0.05, 0.1, 0.075])
ax_next = plt.axes([0.61, 0.05, 0.2, 0.075])
axclose = plt.axes([0.82, 0.05, 0.1, 0.075])
bnext = Button(ax_next, 'Next and save')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)
bclose = Button(axclose, 'Close')
bclose.on_clicked(callback.close)

plt.show()