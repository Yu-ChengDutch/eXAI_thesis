import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import Button
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
import numpy as np

path = "C:/Users/zmezl/Desktop/University/AI/Thesis/eXAI_thesis/Amin_dataset/"

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
x = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
plt.xticks(ticks=x)
plt.yticks(ticks=x)

reg_array = np.zeros((10,10))            

class Index:
    im = 0

    def next(self, event):
        ax.clear()
        
        print(reg_array)
        
        reg_array[reg_array != 0] = 0
               
        self.im += 1

        img = mpimg.imread(path + 'IM_'+ str(self.im) + '.jpg')
        imgplot = ax.imshow(img, extent=[0, 50, 0, 50])
        
        ax.set_xticks(x)
        ax.set_yticks(x)
        ax.grid(True)
        
        plt.draw()
        
        
    def prev(self, event):
        self.im -= 1

        img = mpimg.imread(path + 'IM_'+ str(self.im) + '.jpg')
        imgplot = ax.imshow(img, extent=[0, 50, 0, 50])
        plt.draw()
   

class Annotate(object):
    def __init__(self):
        self.ax = plt.gca()
        # self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        # self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_click)

    def on_click(self, event):
        
        if event.inaxes == self.ax:       
            x_co = event.xdata
            y_co = event.ydata
            
            i = 0
            
            for i in range(0, 11):
                if x_co < x[i]:
                    x_pos = x[i] - 5
                    row = i - 1
                    break
                else:
                    i += 1
                
            z = 0
            
            for i in range(0, 11):
                if y_co < x[z]:
                    y_pos = x[z] - 5
                    col = 9 - (z - 1)
                    break
                else:
                    z += 1
            
            if event.button is MouseButton.LEFT:
                # Background
                rec_col = 'blue'
                value = 10   
            if event.button is MouseButton.RIGHT:
                # Lesion
                rec_col = 'red'
                value = -10
            
            print(str(row) + " " + str(col))
            
            reg_array[col, row] = value      
                
            self.ax.add_patch(Rectangle((x_pos, y_pos), width=5, height=5, color=rec_col, alpha=0.2))  
            self.ax.figure.canvas.draw()
        
a = Annotate()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()