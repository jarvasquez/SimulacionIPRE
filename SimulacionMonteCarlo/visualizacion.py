# Librerias Externas
import matplotlib.pyplot as plt

# Librerias Propias
from parametros import View

class Visual:

    def __init__ (self, data_1, data_2):
        self.fig = plt.figure ()
        self.ax = self.fig.add_subplot(111)
        self.line1, self.line2 = self.ax.plot(*data_1, 'r.', *data_2, 'b.') # Returns a tuple of line objects, thus the comma

        # Set limits
        self.line1.axes.set_xlim (View.MIN_LIMIT_X, View.MAX_LIMIT_X)
        self.line1.axes.set_ylim (View.MIN_LIMIT_Y, View.MAX_LIMIT_Y)
        self.line2.axes.set_xlim (View.MIN_LIMIT_X, View.MAX_LIMIT_X)
        self.line2.axes.set_ylim (View.MIN_LIMIT_Y, View.MAX_LIMIT_Y)

        # Leyenda
        self.line1.set_label ('Robot')
        self.line2.set_label ('Obstaculo')

        plt.legend ()
        plt.grid ()
        self.fig.canvas.draw ()

    def update (self, data_1, data_2):

        # Robot se mueve
        self.line1.set_data (*data_1)
        # Obstaculo se mueve
        self.line2.set_data (*data_2)

        self.fig.canvas.draw ()
        # self.fig.canvas.flush_events()
        plt.pause(View.Ts)

if __name__ == "__main__":
    data_1 = [0, 1]
    data_2 = [2, 0]
    view = Visual (data_1, data_2)

    for i in range (10):
        data_1 = [i, 1]

        view.update (data_1, data_2)
        

# REFERENCIAS
# [1] Update Lines in matplotlib https://stackoverflow.com/questions/11371255/update-lines-in-matplotlib
# [2] How to update a plot in matplotlib https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib