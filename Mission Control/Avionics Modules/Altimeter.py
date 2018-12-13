import sys
import math as maths
from PySide2 import QtCore, QtWidgets as qtw, QtGui as qtg

class Altimeter(qtw.QWidget):

    #unit size defenition and default size
    unit_size = 200
    size = 1

    #colors YAY!!!!
    pane_color = '#76787a'
    dial_fill_color = '#000000'
    dial_boarder_color = '#dbdbdb'
    major_ax_color = '#FFFFFF'
    needle_axle_color = '#dbdbdb'

    #
    max_value = 10000
    min_value = 0
    value = 0

    #default constructor
    def __init__(self):
        super(Altimeter, self).__init__()

        self.show()


    #paint method
    def paintEvent(self, event):
        width = self.unit_size*self.size
        painter = qtg.QPainter()
        painter.begin(self)

        brush = qtg.QBrush()
        brush.setStyle(QtCore.Qt.SolidPattern)
        brush.setColor(self.pane_color)
        painter.setBrush(brush)
        painter.setPen(qtg.QPen(QtCore.Qt.NoPen))

        #paint back pane
        pane = painter.drawRect(0, 0, width, width)

        #paint paint dial background
        brush.setColor(self.dial_fill_color)
        pen = qtg.QPen(self.dial_boarder_color)
        pen.setWidth(width / 50)
        painter.setPen(pen)
        painter.setBrush(brush)
        dial = painter.drawEllipse(width/20, width/20, 18*width/20, 18*width/20)


        #---paint axes---
        #set pen color
        pen = qtg.QPen(self.major_ax_color)
        pen.setWidth(width/50)
        painter.setPen(pen)

        #define the center of the dial
        dial_center_x = width/2
        dial_center_y = width/2
        dial_radius = (9*width)/20

        #maths to calculate
        span = 235
        num_majTick = 4
        num_minTick = 9
        num_ticks = ((num_majTick-1)*num_minTick)+num_majTick
        tick_span = span/(num_ticks-1)
        val_per_tick = (self.max_value - self.min_value)/float(num_ticks-1)
        ticks = list()

        #paint tick marks
        for i in range(0, num_ticks):
            if((i%(num_minTick+1))==0):                   #if major tick mark, increase length and thickness
                pen.setWidth(width / 50)
                ticklength = 0.2
                label = True
            else:
                pen.setWidth(width / 100)
                ticklength = 0.1
                label = False

            painter.setPen(pen)     #set pen

            #calculate the endpoints of the linefor the tick mark
            x1 = dial_center_x + dial_radius * 0.97 * maths.cos(i*tick_span * (maths.pi / 180))
            y1 = dial_center_y - dial_radius * 0.97 * maths.sin(i*tick_span * (maths.pi / 180))
            x2 = dial_center_x + dial_radius * (0.97-ticklength) * maths.cos((i*tick_span) * (maths.pi / 180))
            y2 = dial_center_y - dial_radius * (0.97-ticklength) * maths.sin((i*tick_span) * (maths.pi / 180))

            tick = painter.drawLine(x1, y1, x2, y2) #draw line
            ticks.append(tick)  #append to ticks array

            if(label):  #if a lable needs to be placed
                #configure the font
                font = qtg.QFont()
                font.setPixelSize(width*0.06)
                painter.setFont(font)

                tick_label_text = str(int(self.max_value - (i * val_per_tick + self.min_value))) #build the text string

                #calculate x and y locations
                x_label = dial_center_x + dial_radius * (0.77-ticklength) * maths.cos((i*tick_span) * (maths.pi / 180))
                y_label = dial_center_y - dial_radius * (0.77-ticklength) * maths.sin((i*tick_span) * (maths.pi / 180))

                painter.drawText(x_label-.21*width,y_label - 0.03*width, 0.4*width, 0.06*width, QtCore.Qt.AlignCenter, tick_label_text)  #paint to screen

        #draw tick lables


        #draw center circle at needle pivot 'axel'
        brush.setColor(self.needle_axle_color)
        painter.setBrush(brush)
        painter.setPen(qtg.QPen(QtCore.Qt.NoPen))

        axel_width = dial_radius/4
        painter.drawEllipse(dial_center_x - (axel_width/2), dial_center_y - (axel_width/2), axel_width, axel_width,)


        self.update()



app = qtw.QApplication([])
alt = Altimeter()

sys.exit(app.exec_())