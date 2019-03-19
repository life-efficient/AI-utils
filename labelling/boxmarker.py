import matplotlib.pyplot as plt
from matplotlib import image
from matplotlib.widgets import Cursor
import glob
import pandas as pd
import sys, os
import json

root_dir = '../../adla/data/image_data'
save_dir = '../../adla/data/product_annotations'

def get_img_files(root):
    files = [os.path.join(root, brand, product, file)
             for brand in os.listdir(root)
             for product in os.listdir(os.path.join(root, brand))
             for file in os.listdir(os.path.join(root, brand, product))]
    return files

class BoxMarker():
    def __init__(self, root_dir, save_dir):
        self.bndboxes = []
        self.locations = ['x', 'y', 'w', 'h']
        self.root_dir = root_dir
        self.save_dir = save_dir
        self.got_data = False

        self.fig = plt.figure()
        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key) # link this name to this function
        self.ax = self.fig.add_subplot(111)
        cursor = Cursor(self.ax, useblit=True, color='red', linewidth=1)
        #rec = RectangleSelector(self.ax, onselect=self.onclick, drawtype='box', useblit=True, spancoords='pixels',
        #                        interactive=True)#, minspanx=5, minspany=5)
        self.files = get_img_files(root_dir)
        print(self.files)
        if len(self.files) == 0:
            print('Make sure all of your images are in a folder called \'{}\' within this one.'.format(self.root_dir),
            '\nIf you\'re sure they are, then you\'ve already labelled all of these images.')

        self.set_up_image()

        plt.ion()
        plt.show(block=True)

    def set_up_image(self):
        print('Moving to next image')
        plt.cla()
        print(len(self.files), 'images remaining')
        self.filename = self.files.pop(0)
        self.im = image.imread(self.filename)
        print(self.im.shape)
        self.ax.imshow(self.im)
        print('Image name:', self.filename, '\t{} files remaining'.format(len(self.files)))
        print('Mark the top left of the box and then the bottom right')
        self.fig.canvas.draw() # update the plot
        self.image_box = []

    def finish_with_image(self):

        # change xmin, ymin, xmax, ymin -> x, y, w, h
        xmin, ymin, xmax, ymax = self.image_box
        w = xmax - xmin
        h = ymax - ymin
        x = xmin + w / 2
        y = ymin + h / 2

        # NORMALISE
        h /= self.im.shape[0]
        y /= self.im.shape[0]
        w /= self.im.shape[1]
        x /= self.im.shape[1]

        annotation = {
            "width": w,
            "height": h,
            "centre_x": x,
            "centre_y": y
        }
        print(self.filename)
        print(annotation)
        save_name = self.filename.split('/')[-1]
        save_name = save_name.split('.')[0]
        save_name += '.json'
        save_path = os.path.join(self.save_dir, save_name)
        with open(save_path, 'w') as f:
            f.write(json.dumps(annotation))

    def onclick(self, event):
        if len(self.image_box) < 4:

            print(len(self.image_box))
            x, y = float(event.xdata), float(event.ydata)   # event.x gives coordinates of x in data visualised
            print('X', x, 'Y', y)
            self.image_box.append(x)
            self.image_box.append(y)
            self.cross = plt.plot(event.xdata, event.ydata, marker='x', color='r') # xdata gives pixel coordinates
            self.fig.canvas.draw()
        else:
            print('You\'re done, press enter. If you\'ve made a mistake, press backspace and remark this image')

    def on_key(self, event):
        print('\nYou pressed', event.key)

        if event.key == 'backspace':    # use backspace to remove previously placed crosses
            plt.cla()
            self.ax.imshow(self.im)
            self.image_box = []

        if event.key == 'k':
            self.set_up_image()

        if event.key == 'enter' or event.key == 'ctrl+w': # press enter when youre done with an image
            self.finish_with_image()
            if len(self.files) > 0:
                print('Images remaining:', len(self.files))
                self.set_up_image()
            else:
                print('All images done')
                self.close()

        if event.key == 'escape':
            self.close()

    def close(self):
        '''
        if self.got_data:
            print('Writing collected data')
            self.bndboxes= pd.DataFrame(self.bndboxes)
            print(len(self.bndboxes))
            print(self.bndboxes)
            self.bndboxes.columns = ['Filename'] + self.locations
            self.bndboxes = self.bndboxes.set_index('Filename')
            if self.csv_already_exists: # if the csv already exists then append to it
                print('The csv already exists')
                #print('old shit:', pd.read_csv(self.root + self.csv))
                self.bndboxes = pd.read_csv(self.csv, index_col=0).append(self.bndboxes)
            self.bndboxes.to_csv(self.csv)
            print(self.bndboxes)
        print('Closing ImageMarker')
        '''
        sys.exit(0)


mymarker = BoxMarker(root_dir=root_dir, save_dir=save_dir)


