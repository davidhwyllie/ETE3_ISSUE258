#START_LICENSE###########################################################
#
# Copyright (C) 2009 by Jaime Huerta Cepas. All rights reserved.
# email: jhcepas@gmail.com
#
# This file is part of the Environment for Tree Exploration program (ETE).
# http://ete.cgenomics.org
#
# ETE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ETE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ETE.  If not, see <http://www.gnu.org/licenses/>.
#
# #END_LICENSE#############################################################

from PyQt4 import QtCore, QtGui
from numpy import isfinite as _isfinite, ceil

from main import add_face_to_node, _Background, _Border, COLOR_SCHEMES

isfinite = lambda n: n and _isfinite(n)

_aafgcolors = {
    'A':"#000000" ,
    'R':"#000000" ,
    'N':"#000000" ,
    'D':"#000000" ,
    'C':"#000000" ,
    'Q':"#000000" ,
    'E':"#000000" ,
    'G':"#000000" ,
    'H':"#000000" ,
    'I':"#000000" ,
    'L':"#000000" ,
    'K':"#000000" ,
    'M':"#000000" ,
    'F':"#000000" ,
    'P':"#000000" ,
    'S':"#000000" ,
    'T':"#000000" ,
    'W':"#000000" ,
    'Y':"#000000" ,
    'V':"#000000" ,
    'B':"#000000" ,
    'Z':"#000000" ,
    'X':"#000000",
    '.':"#000000",
    '-':"#000000",
}

_aabgcolors = {
    'A':"#C8C8C8" ,
    'R':"#145AFF" ,
    'N':"#00DCDC" ,
    'D':"#E60A0A" ,
    'C':"#E6E600" ,
    'Q':"#00DCDC" ,
    'E':"#E60A0A" ,
    'G':"#EBEBEB" ,
    'H':"#8282D2" ,
    'I':"#0F820F" ,
    'L':"#0F820F" ,
    'K':"#145AFF" ,
    'M':"#E6E600" ,
    'F':"#3232AA" ,
    'P':"#DC9682" ,
    'S':"#FA9600" ,
    'T':"#FA9600" ,
    'W':"#B45AB4" ,
    'Y':"#3232AA" ,
    'V':"#0F820F" ,
    'B':"#FF69B4" ,
    'Z':"#FF69B4" ,
    'X':"#BEA06E",
    '.':"#FFFFFF",
    '-':"#FFFFFF",
    }

_ntfgcolors = {
    'A':'#000000',
    'G':'#000000',
    'I':'#000000',
    'C':'#000000',
    'T':'#000000',
    'U':'#000000',
    '.':"#000000",
    '-':"#000000",
    ' ':"#000000"
    }

_ntbgcolors = {
    'A':'#A0A0FF',
    'G':'#FF7070',
    'I':'#80FFFF',
    'C':'#FF8C4B',
    'T':'#A0FFA0',
    'U':'#FF8080',
    '.':"#FFFFFF",
    '-':"#FFFFFF",
    ' ':"#FFFFFF"
}

__all__ = ["Face", "TextFace", "AttrFace", "ImgFace",
           "ProfileFace", "SequenceFace", "TreeFace",
           "RandomFace", "DynamicItemFace", "StaticItemFace",
           "CircleFace", "PieChartFace", "BarChartFace"]

class Face(object):
    """ 
    Standard definition of a Face node object.

    This class is not functional and it should only be used to create
    other face objects. By inheriting this class, you set all the
    essential attributes, however the update_pixmap() function is
    required to be reimplemented for convenience.

    User adjustable properties: 

    :param 0 margin_left: in pixels 
    :param 0 margin_right: in pixels
    :param 0 margin_top: in pixels
    :param 0 margin_bottom: in pixels 
    :param 1.0 opacity: a float number in the (0,1) range
    :param True rotable: If True, face will be rotated when necessary
      (i.e. when circular mode is enabled and face occupies an inverted position.)
    :param 0 hz_align: 0 left, 1 center, 2 right
    :param 1 vt_align: 0 top, 1 center, 2 bottom
    :param background: background of face plus its margins
    :param inner_background: background of the face

    :param None border: Border around face margins. Integer number
                        representing the width of the face border line
                        in pixels.  A line width of zero indicates a
                        cosmetic pen. This means that the pen width is
                        always drawn one pixel wide, independent of
                        the transformation set on the painter. A
                        "None" value means invisible border.

    :param None inner_border: Border around face . Integer number
                              representing the width of the face
                              border line in pixels.  A line width of
                              zero indicates a cosmetic pen. This
                              means that the pen width is always drawn
                              one pixel wide, independent of the
                              transformation set on the painter. A
                              "None" value means invisible border.

    """

    def __init__(self):
        self.node        = None
        self.type = "pixmap" # pixmap, text or item

        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0
        self.pixmap = None
        self.opacity = 1.0
        self.rotable = True
        self.hz_align = 0 # 0 left, 1 center, 2 right
        self.vt_align = 1
        self.background = _Background()
        self.border = _Border()
        self.inner_border = _Border()
        self.inner_background = _Background()

    def _size(self):
        if self.pixmap:
            return self._width(),self._height()
        else:
            return 0, 0

    def _width(self):
        if self.pixmap:
            return self.pixmap.width()
        else:
            return 0

    def _height(self):
        if self.pixmap:
            return self.pixmap.height()
        else:
            return 0

    def load_pixmap_from_file(self, filename):
        self.pixmap = QtGui.QPixmap(filename)

    def update_pixmap(self):
        pass

class TextFace(Face):
    """ 
    Static text Face object

    .. currentmodule:: ete_dev
    
    :argument text:     Text to be drawn
    :argument ftype:    Font type, e.g. Arial, Verdana, Courier
    :argument fsize:    Font size, e.g. 10,12,6, (default=10)
    :argument fgcolor:  Foreground font color. RGB code or name in :data:`SVG_COLORS` 
    :argument penwidth: Penwdith used to draw the text.
    :argument fstyle: "normal" or "italic" 
    """

    def __init__(self, text, ftype="Verdana", fsize=10, fgcolor="#000000", penwidth=0, fstyle="normal"):

        Face.__init__(self)

        self.pixmap = None
        self.type = "text"

        self.text = str(text)
        self.fgcolor = fgcolor
        self.ftype = ftype 
        self.fsize = fsize
        self.fstyle = fstyle
        self.penwidth = penwidth

    def _get_font(self):
        font = QtGui.QFont(self.ftype, self.fsize)
        if self.fstyle == "italic":
            font.setStyle(QtGui.QFont.StyleItalic)
        elif self.fstyle == "oblique":
            font.setStyle(QtGui.QFont.StyleOblique)
        return font

    def _height(self):
        fm = QtGui.QFontMetrics(self._get_font())
        h =  fm.boundingRect(QtCore.QRect(), \
                                 QtCore.Qt.AlignLeft, \
                                 self.get_text()).height()
        return h

    def _width(self):
        fm = QtGui.QFontMetrics(self._get_font())
        return fm.size(QtCore.Qt.AlignTop, self.get_text()).width()

    def get_text(self):
        return self.text

class AttrFace(TextFace):
    """ 

    Dynamic text Face. Text rendered is taken from the value of a
    given node attribute.

    :argument attr:     Node's attribute that will be drawn as text
    :argument ftype:    Font type, e.g. Arial, Verdana, Courier, (default="Verdana")
    :argument fsize:    Font size, e.g. 10,12,6, (default=10)
    :argument fgcolor:  Foreground font color. RGB code or name in :data:`SVG_COLORS` 
    :argument penwidth: Penwdith used to draw the text. (default is 0)
    :argument text_prefix: text_rendered before attribute value
    :argument text_suffix: text_rendered after attribute value
    :argument formatter: a text string defining a python formater to
      process the attribute value before renderer. e.g. "%0.2f"
    :argument fstyle: "normal" or "italic" 
    """

    def __init__(self, attr, ftype="Verdana", fsize=10, fgcolor="#000000", \
                     penwidth=0, text_prefix="", text_suffix="", formatter=None, fstyle="normal"):
        Face.__init__(self)
        TextFace.__init__(self, "", ftype, fsize, fgcolor, penwidth, fstyle)
        self.attr     = attr
        self.type     = "text"
        self.text_prefix = text_prefix
        self.text_suffix = text_suffix
        self.attr_formatter = formatter

    def get_text(self):
        if self.attr_formatter:
            text = self.attr_formatter % getattr(self.node, self.attr)
        else:
            text = str(getattr(self.node, self.attr))
        return ''.join(map(str, [self.text_prefix, \
                                     text, \
                                     self.text_suffix]))

class ImgFace(Face):
    """ 
    Creates a new image face object.

    :argument img_file: Image file in png,jpg,bmp format

    """
    def __init__(self,img_file):
        Face.__init__(self)
        self.img_file = img_file

    def update_pixmap(self):
        self.load_pixmap_from_file(self.img_file)


class ProfileFace(Face):
    """ 
    A profile Face for ClusterNodes 

    :argument max_v: maximum value used to build the build the plot scale.
    :argument max_v: minimum value used to build the build the plot scale.
    :argument center_v: Center value used to scale plot and heatmap.
    :argument 200 width:  Plot width in pixels. 
    :argument 40 height: Plot width in pixels. 
    :argument lines style: Plot style: "lines", "bars", "cbars" or "heatmap".

    :argument 2 colorscheme: colors used to create the gradient from
      min values to max values. 0=green & blue; 1=green & red; 2=red &
      blue. In all three cases, missing values are rendered in black
      and transition color (values=center) is white.
    """

    def __init__(self,max_v,min_v,center_v,width=200,height=40,style="lines", colorscheme=2):
        Face.__init__(self)

        self.width  = width
        self.height = height
        self.max_value = max_v
        self.min_value = min_v
        self.center_v  = center_v
        self.style = style
        self.colorscheme = colorscheme

    def update_pixmap(self):
        if self.style=="lines":
            self.draw_line_profile()
        elif self.style=="heatmap":
            self.draw_heatmap_profile()
        elif self.style=="bars":
            self.draw_bar_profile()
        elif self.style=="cbars":
            self.draw_centered_bar_profile()

    def get_color_gradient(self):
        colors = []
        if self.colorscheme == 0:
            # Blue and Green
            for a in xrange(100,0,-1):
                color=QtGui.QColor()
                color.setRgb( 200-2*a,255,200-2*a )
                colors.append(color)

            colors.append(QtGui.QColor("white"))

            for a in xrange(0,100):
                color=QtGui.QColor()
                color.setRgb( 200-2*a,200-2*a,255 )
                colors.append(color)
#            color=QtGui.QColor()
#            color.setRgb( 0,255,255 )
#            colors.append(color)

        elif self.colorscheme == 1:
            for a in xrange(100,0,-1):
                color=QtGui.QColor()
                color.setRgb( 200-2*a,255,200-2*a )
                colors.append(color)

            colors.append(QtGui.QColor("white"))

            for a in xrange(0,100):
                color=QtGui.QColor()
                color.setRgb( 255,200-2*a,200-2*a )
                colors.append(color)
#            color=QtGui.QColor()
#            color.setRgb(255,255,0 )
#            colors.append(color)

        else:
            # Blue and Red
            for a in xrange(100,0,-1):
                color=QtGui.QColor()
                color.setRgb( 200-2*a,200-2*a,255 )
                colors.append(color)

            colors.append(QtGui.QColor("white"))

            for a in xrange(0,100):
                color=QtGui.QColor()
                color.setRgb( 255,200-2*a,200-2*a )
                colors.append(color)

#            color=QtGui.QColor()
#            color.setRgb( 255,0,255 )
#            colors.append(color)

        return colors

    def draw_bar_profile(self):
        # Calculate vector
        mean_vector = self.node.profile
        deviation_vector = self.node.deviation
        # If no vector, skip
        if mean_vector is None:
            return

        colors = self.get_color_gradient()

        vlength = len(mean_vector)
        # pixels per array position
        profile_width = self.width  - 40
        profile_height= self.height 

        x_alpha = float( profile_width / (len(mean_vector)) )
        y_alpha = float ( (profile_height-1) / (self.max_value-self.min_value) )

        # Creates a pixmap
        self.pixmap = QtGui.QPixmap(self.width,self.height)
        self.pixmap.fill(QtGui.QColor("white"))
        p = QtGui.QPainter(self.pixmap)

        x2 = 0 
        y  = 0

        # Mean and quartiles y positions
        mean_line_y = y + profile_height/2
        line2_y     = mean_line_y + profile_height/4
        line3_y     = mean_line_y - profile_height/4

        # Draw axis and scale
        p.setPen(QtGui.QColor("black"))
        p.drawRect(x2,y,profile_width, profile_height-1)
        p.setFont(QtGui.QFont("Verdana",8))
        p.drawText(profile_width,y+10,"%0.3f" %self.max_value)
        p.drawText(profile_width,y+profile_height,"%0.3f" %self.min_value)

        dashedPen = QtGui.QPen(QtGui.QBrush(QtGui.QColor("#ddd")), 0)
        dashedPen.setStyle(QtCore.Qt.DashLine)

        # Draw hz grid
        p.setPen(dashedPen)
        p.drawLine(x2+1, mean_line_y, profile_width-2, mean_line_y )
        p.drawLine(x2+1, line2_y, profile_width-2, line2_y )
        p.drawLine(x2+1, line3_y, profile_width-2, line3_y )


        # Draw bars
        for pos in xrange(vlength):
            # first and second X pixel positions
            x1 = x2
            x2 = x1 + x_alpha

            dev1 =  self.fit_to_scale(deviation_vector[pos])
            mean1 = self.fit_to_scale(mean_vector[pos])

            # If nan value, skip
            if not isfinite(mean1):
                continue

            # Set heatmap color
            if mean1 > self.center_v:
                color_index = abs(int(ceil(((self.center_v - mean1) * 100) / (self.max_value - self.center_v))))
                customColor = colors[100 + color_index]
            elif mean1 < self.center_v:
                color_index = abs(int(ceil(((self.center_v - mean1) * 100) / (self.min_value - self.center_v))))
                customColor = colors[100 - color_index]
            else:
                customColor = colors[100]

            # mean bar high
            mean_y1     = int ( (mean1 - self.min_value) * y_alpha)

            # Draw bar border
            p.setPen(QtGui.QColor("black"))
            #p.drawRect(x1+2,mean_y1, x_alpha-3, profile_height-mean_y1+1)
            # Fill bar with custom color
            p.fillRect(x1+3,profile_height-mean_y1, x_alpha-4, mean_y1-1, QtGui.QBrush(customColor))

            # Draw error bars
            if dev1 != 0:
                dev_up_y1   = int((mean1+dev1 - self.min_value) * y_alpha)
                dev_down_y1 = int((mean1-dev1 - self.min_value) * y_alpha)
                p.drawLine(x1+x_alpha/2, profile_height-dev_up_y1 ,x1+x_alpha/2, profile_height-dev_down_y1 )
                p.drawLine(x1-1+x_alpha/2,  profile_height-dev_up_y1, x1+1+x_alpha/2, profile_height-dev_up_y1 )
                p.drawLine(x1-1+x_alpha/2,  profile_height-dev_down_y1, x1+1+x_alpha/2, profile_height-dev_down_y1 )

    def draw_centered_bar_profile(self):
        # Calculate vector
        mean_vector  = self.node.profile
        deviation_vector = self.node.deviation
        # If no vector, skip
        if mean_vector is None:
            return

        colors = self.get_color_gradient()

        vlength = len(mean_vector)
        # pixels per array position
        profile_width = self.width - 40
        profile_height= self.height

        x_alpha = float( profile_width / (len(mean_vector)) )
        y_alpha_up = float ( ((profile_height-1)/2) / (self.max_value-self.center_v) )
        y_alpha_down = float ( ((profile_height-1)/2) / (self.min_value-self.center_v) )

        # Creates a pixmap
        self.pixmap = QtGui.QPixmap(self.width,self.height)
        self.pixmap.fill(QtGui.QColor("white"))
        p = QtGui.QPainter(self.pixmap)

        x2 = 0
        y  = 0 

        # Mean and quartiles y positions
        mean_line_y = y + profile_height/2
        line2_y     = mean_line_y + profile_height/4
        line3_y     = mean_line_y - profile_height/4

        # Draw axis and scale
        p.setPen(QtGui.QColor("black"))
        p.drawRect(x2,y,profile_width, profile_height-1)
        p.setFont(QtGui.QFont("Verdana",8))
        p.drawText(profile_width,y+10,"%0.3f" %self.max_value)
        p.drawText(profile_width,y+profile_height,"%0.3f" %self.min_value)
        p.drawText(profile_width,mean_line_y,"%0.3f" %self.center_v)

        dashedPen = QtGui.QPen(QtGui.QBrush(QtGui.QColor("#ddd")), 0)
        dashedPen.setStyle(QtCore.Qt.DashLine)

        # Draw hz grid
        p.setPen(dashedPen)
        p.drawLine(x2+1, mean_line_y, profile_width-2, mean_line_y )
        p.drawLine(x2+1, line2_y, profile_width-2, line2_y )
        p.drawLine(x2+1, line3_y, profile_width-2, line3_y )


        # Draw bars
        for pos in xrange(vlength):
            # first and second X pixel positions
            x1 = x2
            x2 = x1 + x_alpha

            dev1 =  self.fit_to_scale( deviation_vector[pos]   )
            mean1 = self.fit_to_scale( mean_vector[pos]        )

            # If nan value, skip
            if not isfinite(mean1):
                continue

            # Set heatmap color
            if mean1>self.center_v:
                color_index = abs(int(ceil(((self.center_v-mean1)*100)/(self.max_value-self.center_v))))
                customColor = colors[100 + color_index]

                #print mean1, color_index, len(colors), "%x" %colors[100 + color_index].rgb()
                #print abs(((self.center_v-mean1)*100)/(self.max_value-self.center_v))
                #print round(((self.center_v-mean1)*100)/(self.max_value-self.center_v))

            elif mean1<self.center_v:
                color_index = abs(int(ceil(((self.center_v-mean1)*100)/(self.min_value-self.center_v))))
                customColor = colors[100 - color_index]
            else:
                customColor = colors[100]

            # mean bar high
            if mean1 < self.center_v:
                mean_y1 = int(abs((mean1 - self.center_v) * y_alpha_down))
            else:
                mean_y1 = int(abs((mean1 - self.center_v) * y_alpha_up))

            # Draw bar border
            p.setPen(QtGui.QColor("black"))
            #p.drawRect(x1+2,mean_y1, x_alpha-3, profile_height-mean_y1+1)
            # Fill bar with custom color
            if mean1<self.center_v:
                p.fillRect(x1+3, mean_line_y, x_alpha-4, mean_y1, QtGui.QBrush(customColor))
            else:
                p.fillRect(x1+3, mean_line_y-mean_y1, x_alpha-4, mean_y1+1, QtGui.QBrush(customColor))

            # Draw error bars
            if dev1 != 0:
                if mean1<self.center_v:
                    dev_up_y1   = int((mean1+dev1 - self.center_v) * y_alpha_down)
                    dev_down_y1 = int((mean1-dev1 - self.center_v) * y_alpha_down)
                    p.drawLine(x1+x_alpha/2, mean_line_y+dev_up_y1 ,x1+x_alpha/2, mean_line_y+dev_down_y1 )
                    p.drawLine(x1-1+x_alpha/2, mean_line_y+dev_up_y1 ,x1+1+x_alpha/2, mean_line_y+dev_up_y1 )
                    p.drawLine(x1-1+x_alpha/2, mean_line_y+dev_down_y1 ,x1+1+x_alpha/2, mean_line_y+dev_down_y1 )
                else:
                    dev_up_y1   = int((mean1+dev1 - self.center_v) * y_alpha_up)
                    dev_down_y1 = int((mean1-dev1 - self.center_v) * y_alpha_up)
                    p.drawLine(x1+x_alpha/2, mean_line_y-dev_up_y1 ,x1+x_alpha/2, mean_line_y-dev_down_y1 )
                    p.drawLine(x1-1+x_alpha/2, mean_line_y-dev_up_y1 ,x1+1+x_alpha/2, mean_line_y-dev_up_y1 )
                    p.drawLine(x1-1+x_alpha/2, mean_line_y-dev_down_y1 ,x1+1+x_alpha/2, mean_line_y-dev_down_y1 )

    def draw_line_profile(self):
        # Calculate vector
        mean_vector = self.node.profile
        deviation_vector = self.node.deviation
        if mean_vector is None:
            return

        vlength = len(mean_vector)
        # pixels per array position
        profile_width = self.width - 40
        profile_height= self.height 


        x_alpha = float( profile_width / (len(mean_vector)-1) )
        y_alpha = float ( (profile_height-1) / (self.max_value-self.min_value) )

        # Creates a pixmap
        self.pixmap = QtGui.QPixmap(self.width,self.height)
        self.pixmap.fill(QtGui.QColor("white"))
        p = QtGui.QPainter(self.pixmap)

        x2 = 0
        y  = 0

        # Mean and quartiles y positions
        mean_line_y = y + profile_height/2
        line2_y     = mean_line_y + profile_height/4
        line3_y     = mean_line_y - profile_height/4
        
        # Draw axis and scale
        p.setPen(QtGui.QColor("black"))
        p.drawRect(x2,y,profile_width, profile_height-1)
        p.setFont(QtGui.QFont("Verdana",8))
        p.drawText(profile_width,y+10,"%0.3f" %self.max_value)
        p.drawText(profile_width,y+profile_height,"%0.3f" %self.min_value)
        p.drawText(profile_width,mean_line_y+5,"%0.3f" %self.center_v)

        dashedPen = QtGui.QPen(QtGui.QBrush(QtGui.QColor("#ddd")), 0)
        dashedPen.setStyle(QtCore.Qt.DashLine)

        # Draw hz grid
        p.setPen(dashedPen)
        p.drawLine(x2+1, mean_line_y, profile_width-2, mean_line_y )
        p.drawLine(x2+1, line2_y, profile_width-2, line2_y )
        p.drawLine(x2+1, line3_y, profile_width-2, line3_y )

        # Draw lines
        for pos in xrange(0,vlength-1):
            dev1 =  self.fit_to_scale(mean_vector[pos] + deviation_vector[pos])
            dev2 =  self.fit_to_scale(mean_vector[pos+1] + deviation_vector[pos+1])
            mean1 = self.fit_to_scale(mean_vector[pos])
            mean2 = self.fit_to_scale(mean_vector[pos+1])
            # first and second X pixel positions
            x1 = x2
            x2 = x1 + x_alpha

            # Draw vt grid
            if x2 < profile_width:
                p.setPen(dashedPen)
                p.drawLine(x2, y+1, x2, profile_height-2)

            # If nan values, continue
            if not isfinite(mean1) or not isfinite(mean2):
                continue

            # First Y postions for mean
            mean_y1 = (mean1 - self.min_value) * y_alpha
            # Second Y postions for mean
            mean_y2 = (mean2 - self.min_value) * y_alpha
            if dev1!= 0 and dev2!=0:
                # First Y postions for deviations
                dev_y1   = (dev1 - self.min_value) * y_alpha
                # Second Y postions for deviations
                dev_y2   = (dev2 - self.min_value) * y_alpha
                # Draw red deviation lines
                p.setPen(QtGui.QColor("red"))
                p.drawLine(x1, profile_height-dev_y1, x2, profile_height-dev_y2)
                p.drawLine(x1, profile_height+dev_y1, x2, profile_height+dev_y2)
            # Draw blue mean line
            p.setPen(QtGui.QColor("blue"))
            p.drawLine(x1, profile_height-mean_y1, x2, profile_height-mean_y2)
 

    def draw_heatmap_profile(self):
        # Calculate vector
        vector = self.node.profile
        deviation = self.node.deviation
        # If no vector, skip
        if vector is None:
            return

        colors = self.get_color_gradient()

        leaves = self.node.get_leaves()

        vlength = len(vector)
        # pixels per array position
        img_height = self.height * len(leaves)
        profile_width = self.width 
        profile_height= img_height 

        x_alpha = float( profile_width / (len(vector)) )

        # Creates a pixmap
        self.pixmap = QtGui.QPixmap(self.width,img_height)
        self.pixmap.fill(QtGui.QColor("white"))
        p = QtGui.QPainter(self.pixmap)

        x2 = 0
        y  = 0
        y_step = self.height
        for leaf in leaves:
            mean_vector = leaf.profile
            deviation_vector = leaf.deviation
            # Draw heatmap
            for pos in xrange(vlength):
                # first and second X pixel positions
                x1 = x2
                x2 = x1 + x_alpha
                dev1 =  self.fit_to_scale( deviation_vector[pos]   )
                mean1 = self.fit_to_scale( mean_vector[pos]        )
                # Set heatmap color
                if not isfinite(mean1):
                    customColor = QtGui.QColor("#000000")
                elif mean1>self.center_v:
                    color_index = abs(int(ceil(((self.center_v-mean1)*100)/(self.max_value-self.center_v))))
                    customColor = colors[100 + color_index]
                elif mean1<self.center_v:
                    color_index = abs(int(ceil(((self.center_v-mean1)*100)/(self.min_value-self.center_v))))
                    customColor = colors[100 - color_index]
                else:
                    customColor = colors[100]

                # Fill bar with custom color
                p.fillRect(x1, y, x_alpha, y_step, QtGui.QBrush(customColor))
            y+= y_step
            x2 = 0

    def fit_to_scale(self,v):
        if v<self.min_value:
            return float(self.min_value)
        elif v>self.max_value:
            return float(self.max_value)
        else:
            return float(v)


class OLD_SequenceFace(Face):
    """ Creates a new molecular sequence face object.


    :argument seq:  Sequence string to be drawn
    :argument seqtype: Type of sequence: "nt" or "aa"
    :argument fsize:   Font size,  (default=10)

    You can set custom colors for aminoacids or nucleotides: 

    :argument aafg: a dictionary in which keys are aa codes and values
      are foreground RGB colors

    :argument aabg: a dictionary in which keys are aa codes and values
      are background RGB colors

    :argument ntfg: a dictionary in which keys are nucleotides codes
      and values are foreground RGB colors

    :argument ntbg: a dictionary in which keys are nucleotides codes and values
      are background RGB colors

    """

    def __init__(self, seq, seqtype, fsize=10, aafg=None,  \
                     aabg=None, ntfg=None, ntbg=None):

        Face.__init__(self)
        self.seq  = seq
        self.fsize= fsize
        self.fsize = fsize
        self.style = seqtype

        if not aafg:
            aafg = _aafgcolors
        if not aabg: 
            aabg = _aabgcolors
        if not ntfg:
            ntfg = _ntfgcolors
        if not ntbg:
            ntbg = _ntbgcolors

        self.aafg = aafg
        self.aabg = aabg
        self.ntfg = ntfg
        self.ntbg = ntbg


    def update_pixmap(self):
        font = QtGui.QFont("Courier", self.fsize)
        fm = QtGui.QFontMetrics(font)
        height = fm.leading() + fm.overlinePos() + fm.underlinePos()
        #width  = fm.size(QtCore.Qt.AlignTop, self.seq).width()
        width = self.fsize * len(self.seq)

        self.pixmap = QtGui.QPixmap(width,height)
        self.pixmap.fill()
        p = QtGui.QPainter(self.pixmap)
        x = 0
        y = height - fm.underlinePos()*2

        p.setFont(font)

        for letter in self.seq:
            letter = letter.upper()
            if self.style=="nt":
                letter_brush = QtGui.QBrush(QtGui.QColor(self.ntbg.get(letter,"#ffffff" )))
                letter_pen = QtGui.QPen(QtGui.QColor(self.ntfg.get(letter, "#000000")))
            else:
                letter_brush = QtGui.QBrush(QtGui.QColor(self.aabg.get(letter,"#ffffff" )))
                letter_pen = QtGui.QPen(QtGui.QColor(self.aafg.get(letter,"#000000" )))

            p.setPen(letter_pen)
            p.fillRect(x,0,width, height,letter_brush)
            p.drawText(x, y, letter)
            x += float(width)/len(self.seq)
        p.end()


class StaticItemFace(Face):
    """
    .. versionadded:: 2.1

    Creates a face based on an external QtGraphicsItem object.
    QGraphicsItem object is expected to be independent from tree node
    properties, so its content is assumed to be static (drawn only
    once, no updates when tree changes). 

    :arguments item: an object based on QGraphicsItem
    """
    def __init__(self, item):
        Face.__init__(self)
        self.type = "item"
        self.item = item

    def update_items(self):
        return 

    def _width(self):
        return self.item.rect().width()

    def _height(self):
        return self.item.rect().height()
        

class SequenceFace(StaticItemFace, Face):
    """ Creates a new molecular sequence face object.


    :argument seq:  Sequence string to be drawn
    :argument seqtype: Type of sequence: "nt" or "aa"
    :argument fsize:   Font size,  (default=10)

    You can set custom colors for amino-acids or nucleotides: 

    :argument None  codon       : a string that corresponds to the reverse translation of the amino-acid sequence
    :argument None  col_w       : width of the column (if col_w is lower than font size, letter wont be displayed)
    :argument None  fg_colors   : dictionary of colors for foreground, with as keys each possible character in sequences, and as value the colors
    :argument None  bg_colors   : dictionary of colors for background, with as keys each possible character in sequences, and as value the colors
    :argument 3     alt_col_w   : works together with special_col option, defines the width of given columns
    :argument None  special_col : list of lists containing the bounds of columns to be displayed with alt_col_w as width
    :argument False interactive : more info can be displayed when mouse over sequence

    """
    def __init__(self, seq, seqtype="aa", fsize=10,
                 fg_colors=None, bg_colors=None,
                 codon=None, col_w=None, alt_col_w=3,
                 special_col=None, interactive=False):
        self.seq         = seq
        self.codon       = codon
        self.fsize       = fsize
        self.style       = seqtype
        self.col_w       = float(self.fsize + 1) if col_w is None else float(col_w)
        self.alt_col_w   = float(alt_col_w)
        self.special_col = special_col if special_col else []
        self.width       = 0 # will store the width of the whole sequence
        self.interact    = interactive

        if self.style == "aa":
            if not fg_colors:
                fg_colors = _aafgcolors
            if not bg_colors:
                bg_colors = _aabgcolors
        else:
            if not fg_colors:
                fg_colors = _ntfgcolors
            if not bg_colors:
                bg_colors = _ntbgcolors

        self.fg_col = self.__init_col(fg_colors)
        self.bg_col = self.__init_col(bg_colors)
            
        # for future?
        self.row_h       = 13.0

        super(SequenceFace,
              self).__init__(QtGui.QGraphicsRectItem(0, 0, self.width,
                                                     self.row_h))

    def __init_col(self, color_dic):
        """to speed up the drawing of colored rectangles and characters"""
        new_color_dic = {}
        for car in color_dic:
            new_color_dic[car] = QtGui.QBrush(QtGui.QColor(color_dic[car]))
        return new_color_dic
        
    def update_items(self):
        #self.item = QGraphicsRectItem(0,0,self._total_w, self.row_h)
        seq_width = 0
        nopen = QtGui.QPen(QtCore.Qt.NoPen)
        font = QtGui.QFont("Courier", self.fsize)
        rect_cls = self.InteractiveLetterItem if self.interact \
                   else QtGui.QGraphicsRectItem
        for i, letter in enumerate(self.seq):
            width = self.col_w
            for m in self.special_col:
                if m[0] < i <= m[1]:
                    width = self.alt_col_w
                    break
            #load interactive item if called correspondingly
            rectItem = rect_cls(0, 0, width, self.row_h, parent=self.item)
            rectItem.setX(seq_width) # to give correct X to children item
            rectItem.setBrush(self.bg_col[letter])
            rectItem.setPen(nopen)
            if self.interact:
                if self.codon:
                    rectItem.codon = '%s, %d: %s' % (self.seq[i], i,
                                                     self.codon[i*3:i*3+3])
                else:
                    rectItem.codon = '%s, %d' % (self.seq[i], i)
            # write letter if enough space
            if width >= self.fsize:
                text = QtGui.QGraphicsSimpleTextItem(letter, parent=rectItem)
                text.setFont(font)
                text.setBrush(self.fg_col[letter])
                # Center text according to rectItem size
                tw = text.boundingRect().width()
                th = text.boundingRect().height()
                text.setPos((width - tw)/2, (self.row_h - th)/2)
            seq_width += width
        self.width = seq_width

    class InteractiveLetterItem(QtGui.QGraphicsRectItem):
        """This is a class"""
        def __init__(self, *arg, **karg):
            QtGui.QGraphicsRectItem.__init__(self, *arg, **karg)
            self.codon = None
            self.label = None
            self.setAcceptsHoverEvents(True)
    
        def hoverEnterEvent (self, e):
            """ when mouse is over"""
            if not self.label:
                self.label = QtGui.QGraphicsRectItem(parent=self)
                #self.label.setY(-18)
                self.label.setX(11)
                self.label.setBrush(QtGui.QBrush(QtGui.QColor("white")))
                self.label.text = QtGui.QGraphicsSimpleTextItem(parent=self.label)
    
            self.setZValue(1)
            self.label.text.setText(self.codon)
            self.label.setRect(self.label.text.boundingRect())
            self.label.setVisible(True)
    
        def hoverLeaveEvent(self, e):
            """when mouse leaves area"""
            if self.label: 
                self.label.setVisible(False)
                self.setZValue(0)

        
class TreeFace(Face):
    """ 
    .. versionadded:: 2.1

    Creates a Face containing a Tree object. Yes, a tree within a tree :)

    :argument tree: An ETE Tree instance (Tree, PhyloTree, etc...)
    :argument tree_style: A TreeStyle instance defining how tree show be drawn 
    
    """
    def __init__(self, tree, tree_style):
        Face.__init__(self)
        self.type = "item"
        self.root_node = tree
        self.img = tree_style
        self.item = None

    def update_items(self):
        from qt4_render import render
        hide_root = False
        if self.root_node is self.node:
            hide_root = True
        self.item, self.n2i, self.n2f = render(self.root_node, self.img, hide_root)

    def _width(self):
        return self.item.rect().width()

    def _height(self):
        return self.item.rect().height()


class _SphereItem(QtGui.QGraphicsEllipseItem):
    def __init__(self, radius, color, solid=False):
        r = radius
        d = r*2 
        QtGui.QGraphicsEllipseItem.__init__(self, 0, 0, d, d)
        self.gradient = QtGui.QRadialGradient(r, r, r,(d)/3,(d)/3)
        self.gradient.setColorAt(0.05, QtCore.Qt.white)
        self.gradient.setColorAt(1, QtGui.QColor(color))
        if solid:
            self.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        else:
            self.setBrush(QtGui.QBrush(self.gradient))
        self.setPen(QtGui.QPen(QtGui.QColor(color)))
        #self.setPen(QtCore.Qt.NoPen)

class CircleFace(Face):
    """
    .. versionadded:: 2.1

    Creates a Circle or Sphere Face.

    :arguments radius: integer number defining the radius of the face
    :arguments color: Color used to fill the circle. RGB code or name in :data:`SVG_COLORS` 
    :arguments "circle" style: Valid values are "circle" or "sphere"
    """

    def __init__(self, radius, color, style="circle"):
        Face.__init__(self)
        self.radius = radius
        self.style = style
        self.color = color
        self.type = "item"
        self.rotable = False

    def update_items(self):
        if self.style == "circle":
            self.item = _SphereItem(self.radius, self.color, solid=True)
        elif self.style == "sphere":
            self.item = _SphereItem(self.radius, self.color)

    def _width(self):
        return self.item.rect().width()

    def _height(self):
        return self.item.rect().height()


class DynamicItemFace(Face):
    """
    .. versionadded:: 2.1

    Creates a face based on an external QGraphicsItem object whose
    content depends on the node that is linked to. 

    :arguments constructor: A pointer to a method (function or class
      constructor) returning a QGraphicsItem based
      object. "constructor" method is expected to receive a node
      instance as the first argument. The rest of arguments passed to
      ItemFace are optional and will passed also to the constructor
      function.
    """

    def __init__(self, constructor, *args, **kargs):
        Face.__init__(self)
        self.type = "item"
        self.item = None
        self.constructor = constructor
        self.args = args
        self.kargs = kargs

    def update_items(self):
        self.item = self.constructor(self.node, self.args, self.kargs)

    def _width(self):
        return self.item.rect().width()

    def _height(self):
        return self.item.rect().height()


class RandomFace(Face):
    def __init__(self):
        faces.Face.__init__(self)
        self.type = "item"

    def update_items(self):
        import random
        w = random.randint(4, 100)
        h = random.randint(4, 100)
        self.tree_partition = QtGui.QGraphicsRectItem(0,0,w, h)
        self.tree_partition.setBrush(QtGui.QBrush(QtGui.QColor("green")))

    def _width(self):
        return self.tree_partition.rect().width()

    def _height(self):
        return self.tree_partition.rect().height()


class BackgroundFace(Face):
    def __init__(self, min_width=0, min_height=0):
        faces.Face.__init__(self)
        self.type = "background"
        self.min_height = min_height
        self.min_height = min_width

    def _width(self):
        return self.min_width

    def _height(self):
        return self.min_height


class _PieChartItem(QtGui.QGraphicsRectItem):
    def __init__(self, percents, width, height, colors, line_color=None):
        QtGui.QGraphicsRectItem.__init__(self, 0, 0, width, height)
        self.percents = percents
        self.colors = colors
        self.line_color = line_color
        
    def paint(self, painter, option, widget):
        a = 5760
        angle_start = 0
        if not self.line_color:
            painter.setPen(QtCore.Qt.NoPen)
        else:
            painter.setPen(QtGui.QColor(self.line_color))
            
        for i, p in enumerate(self.percents):
            col = self.colors[i]
            painter.setBrush(QtGui.QBrush(QtGui.QColor(col)))
            angle_span = (p/100.) * a
            painter.drawPie(self.rect(), angle_start, angle_span )
            angle_start += angle_span


class PieChartFace(StaticItemFace,Face):
    """ 
    .. versionadded:: 2.2

    :arguments percents: a list of values summing up 100. 
    :arguments width: width of the piechart 
    :arguments height: height of the piechart
    :arguments colors: a list of colors (same length as percents)
   
    """
    def __init__(self, percents, width, height, colors=None, line_color=None):
        Face.__init__(self)
        if round(sum(percents),3) != 100:
            raise ValueError("PieChartItem: percentage values should sum up 100")

        self.type = "item"
        self.item = None
        self.percents = percents
        if not colors:
            colors = COLOR_SCHEMES["paired"]
        self.colors =  colors
        self.width = width
        self.height = height
        self.line_color = line_color
        
    def update_items(self):
        self.item = _PieChartItem(self.percents, self.width,
                                  self.height, self.colors, self.line_color)
        
    def _width(self):
        return self.item.rect().width()

    def _height(self):
        return self.item.rect().height()


class BarChartFace(Face):
    """ 
    .. versionadded:: 2.2

    :arguments percents: a list of values summing up 100. 
    :arguments width: width of the piechart 
    :arguments height: height of the piechart
    :arguments colors: a list of colors (same length as percents)
   
    """
    def __init__(self, values, deviations=None, width=200, height=100, colors=None, labels=None, min_value=0, max_value=None):
        Face.__init__(self)
        self.type = "item"
        self.item = None
        self.values = values
        if not deviations:
            self.deviations = [0] * len(values)
        else:
            self.deviations = deviations

        if not colors:
            colors = COLOR_SCHEMES["paired"]
        self.colors =  colors
       
        
        self.width = width
        self.height = height
        self.labels = labels
        self.max_value = max_value
        self.min_value = min_value
        self.margin_left = 1
        self.margin_right = 1
        self.margin_top = 2
        self.margin_bottom = 2
        
    def update_items(self):
        self.item = _BarChartItem(self.values, self.deviations, self.width,
                                  self.height, self.colors, self.labels, 
                                  self.min_value, self.max_value)
        
    def _width(self):
        return self.item.rect().width()

    def _height(self):
        return self.item.rect().height()


class _BarChartItem(QtGui.QGraphicsRectItem):
    def __init__(self, values, deviations, width, height, colors, labels, min_value, max_value):
        QtGui.QGraphicsRectItem.__init__(self, 0, 0, width, height)
        self.values = values
        self.colors = colors
        self.width = width
        self.height = height
        self.draw_border = False
        self.draw_grid = False
        self.draw_scale = True
        self.labels = labels
        self.max_value = max_value
        self.min_value = min_value
        self.deviations = deviations
        
    def paint(self, p, option, widget):
        colors = self.colors
        values = self.values
        deviations = self.deviations

        spacer = 3
        spacing_length = (spacer*(len(values)-1))
        height=  self.height 
        
        if self.max_value is None:
            max_value = max([v+d for v,d in zip(values, deviations) if isfinite(v)])
        else:
            max_value = self.max_value

        if self.min_value is None:
            min_value = min([v+d for v,d in zip(values, deviations) if isfinite(v)])
        else:
            min_value = 0
            
        scale_length = 0
        scale_margin = 2
        if self.draw_scale: 
            p.setFont(QtGui.QFont("Verdana", 8))
            max_string = "%g" %max_value
            min_string = "%g" %min_value
            fm = QtGui.QFontMetrics(p.font())
            max_string_metrics = fm.boundingRect(QtCore.QRect(), \
                                                 QtCore.Qt.AlignLeft, \
                                                 max_string)
            min_string_metrics = fm.boundingRect(QtCore.QRect(), \
                                                 QtCore.Qt.AlignLeft, \
                                                 min_string)
            scale_length = scale_margin + max(max_string_metrics.width(),
                              min_string_metrics.width())
        

        real_width = self.width - scale_length
        x_alpha = float((real_width - spacing_length) / (len(values))) 
        if x_alpha < 1:
            raise ValueError("BarChartFace is too small")
        
        y_alpha = float ( (height-1) / float(max_value - min_value) )
        x = 0 
        y  = 0

        # Mean and quartiles y positions
        mean_line_y = y + height / 2
        line2_y     = mean_line_y  + height/4
        line3_y     = mean_line_y - height/4

        if self.draw_border:
            p.setPen(QtGui.QColor("black"))
            p.drawRect(x, y, real_width + scale_margin - 1 , height)
            
        if self.draw_scale: 
            p.drawText(real_width + scale_margin, max_string_metrics.height(), max_string)
            p.drawText(real_width + scale_margin, height - 2, min_string)
            p.drawLine(real_width + scale_margin - 1, 0, real_width + scale_margin - 1, height)
            p.drawLine(real_width + scale_margin - 1, 0, real_width + scale_margin + 2, y)
            p.drawLine(real_width + scale_margin - 1, height, real_width + scale_margin + 2, height)
            
        if self.draw_grid: 
            dashedPen = QtGui.QPen(QtGui.QBrush(QtGui.QColor("#ddd")), 0)
            dashedPen.setStyle(QtCore.Qt.DashLine)
            p.setPen(dashedPen)
            p.drawLine(x+1, mean_line_y, real_width - 2, mean_line_y )
            p.drawLine(x+1, line2_y, real_width - 2, line2_y )
            p.drawLine(x+1, line3_y, real_width - 2, line3_y )

        # Draw bars
        for pos in xrange(len(values)):
            # first and second X pixel positions
            x1 = x
            x = x1 + x_alpha + spacer

            std =  deviations[pos]
            val = values[pos]

            # If nan value, skip
            if not isfinite(val):
                continue

            color = QtGui.QColor(colors[pos])
            # mean bar high
            mean_y1     = int((val - min_value) * y_alpha)
            # Draw bar border
            p.setPen(QtGui.QColor("black"))

            # Fill bar with custom color
            p.fillRect(x1, height-mean_y1, x_alpha, mean_y1 - 1, QtGui.QBrush(color))

            # Draw error bars
            if std != 0:
                dev_up_y1   = int((val + std - min_value) * y_alpha)
                dev_down_y1 = int((val - std - min_value) * y_alpha)
                center_x = x1 + (x_alpha / 2)
                p.drawLine(center_x, height - dev_up_y1, center_x, height - dev_down_y1)
                p.drawLine(center_x + 1, height - dev_up_y1, center_x -1, height - dev_up_y1)
                p.drawLine(center_x + 1, height - dev_down_y1, center_x -1, height - dev_down_y1)

            if self.labels: 
                p.save()
                p.translate(x1, -height-30)
                p.rotate(90)
                p.drawText(0, 0, str(self.labels[pos]))
                p.restore()


class SequencePlotFace(StaticItemFace):
    """
    To draw plots, usually correlated to columns in alignment

    :argument      values    : a list of values
    :argument None errors    : a list of errors associated to each value. elements of the list can contain a list with lower and upper error, if they are different.
    :argument None colors    : a list of colors associated to each value
    :argument None header    : a title for the plot
    :argument bar  kind      : kind of plot, one of bar, curve or sticks.
    :argument None fsize     : font size for header and labels
    :argument 100  height    : height of the plot (excluding labels)
    :argument None hlines    : list of y values of horizontal dashed lines to be drawn across plot
    :argument None hlines_col: list of colors associated to each horizontal line
    :argument None col_width : width of a column in the alignment
    :argument red  error_col : color of error bars
    
    """
    def __init__(self, values, errors=None, colors=None, header='',
                 fsize=9, height = 100, hlines=None, kind='bar',
                 hlines_col = None, extras=None, col_width=11,
                 ylim=None, xlabel='', ylabel=''):
        
        self.col_w  = float(col_width)
        self.height = height
        self.values = [float(v) for v in values]
        self.width  = self.col_w * len (self.values)
        self.errors = errors if errors else []
        self.colors = colors if colors else ['gray'] * len(self.values)
        self.header = header
        self.fsize  = fsize
        if ylim:
            self.ylim = tuple((float(y) for y in ylim))
        else:
            dif = (max(self.values) - min(self.values))/20
            if dif >= 1:
                self.ylim = (int(min(self.values)-0.5), int(max(self.values)+0.5))
            else:
                from math import log10
                exp = str(-int(log10(min(self.values))-0.5))
                self.ylim = (float(int(min(self.values)*float('1e'+exp)-0.5))/float('1e'+exp),
                             float(int(max(self.values)/float('1e'+exp)+0.5))/float('1e'+exp))
        self.xlabel = xlabel
        self.ylabel = ylabel

        if self.errors:
            if type(self.errors[0]) is list or type(self.errors[0]) is tuple:
                self._up_err = [float(e[1])  for e in self.errors]
                self._dw_err = [float(-e[0]) for e in self.errors]
            else:
                self._up_err = [float(e)  for e in self.errors]
                self._dw_err = [float(-e) for e in self.errors]
        if kind == 'bar':
            self.draw_fun = self.draw_bar
        elif kind == 'stick':
            self.draw_fun = self.draw_stick
        elif kind == 'curve':
            self.draw_fun = self.draw_curve
        else:
            raise('kind %s not yet implemented... ;)'%kind)
        
        self.hlines     = [float(h) for h in hlines] if hlines else [1.0]
        self.hlines_col = hlines_col if hlines_col else ['black']*len(self.hlines)

        self.extras = extras if extras else ['']
        if len (self.extras) != len (self.values):
            self.extras = ['']
        
        super(SequencePlotFace,
              self).__init__(QtGui.QGraphicsRectItem(-40, 0, self.width+40,
                                                     self.height+50))
        self.item.setPen(QtGui.QPen(QtGui.QColor('white')))

    def update_items(self):
        # draw lines
        for line, col in zip(self.hlines, self.hlines_col):
            self.draw_hlines(line, col)
        # draw plot
        width = self.col_w
        for i, val in enumerate(self.values):
            self.draw_fun(width * i + self.col_w / 2 , val, i)
        # draw error bars
        if self.errors:
            for i in range(len(self.errors)):
                self.draw_errors(width * i + self.col_w / 2 , i)
        # draw x axis
        self.draw_x_axis()
        # draw y axis
        self.draw_y_axis()
        # put header
        self.write_header()

    def write_header(self):
        text = QtGui.QGraphicsSimpleTextItem(self.header)
        text.setFont(QtGui.QFont("Arial", self.fsize))
        text.setParentItem(self.item)
        text.setPos(0, 5)
        
    def draw_y_axis(self):
        lineItem = QtGui.QGraphicsLineItem(0, self.coordY(self.ylim[0]),
                                           0, self.coordY(self.ylim[1]),
                                           parent=self.item)
        lineItem.setPen(QtGui.QPen(QtGui.QColor('black')))
        lineItem.setZValue(10)
        max_w = 0
        for y in set(self.hlines + list(self.ylim)):
            lineItem = QtGui.QGraphicsLineItem(0, self.coordY(y),
                                               -5, self.coordY(y),
                                               parent=self.item)
            lineItem.setPen(QtGui.QPen(QtGui.QColor('black')))
            lineItem.setZValue(10)
            text = QtGui.QGraphicsSimpleTextItem(str(y))
            text.setFont(QtGui.QFont("Arial", self.fsize-2))
            text.setParentItem(self.item)
            tw = text.boundingRect().width()
            max_w = tw if tw > max_w else max_w
            th = text.boundingRect().height()
            # Center text according to masterItem size
            text.setPos(-tw - 5, self.coordY(y)-th/2)
        if self.ylabel:
            text = QtGui.QGraphicsSimpleTextItem(self.ylabel)
            text.setFont(QtGui.QFont("Arial", self.fsize-1))
            text.setParentItem(self.item)
            text.rotate(-90)
            tw = text.boundingRect().width()
            th = text.boundingRect().height()
            # Center text according to masterItem size
            text.setPos(-th -5-max_w, tw/2+self.coordY(sum(self.ylim)/2))
      
    def draw_x_axis(self):
        lineItem = QtGui.QGraphicsLineItem(self.col_w/2,
                                           self.coordY(self.ylim[0])+2,
                                           self.width-self.col_w/2,
                                           self.coordY(self.ylim[0])+2,
                                           parent=self.item)
        lineItem.setPen(QtGui.QPen(QtGui.QColor('black')))
        lineItem.setZValue(10)
        all_vals = range(0, len(self.values), 5)
        if (len(self.values)-1)%5:
            all_vals += [len(self.values)-1]
        for x in all_vals:
            lineItem = QtGui.QGraphicsLineItem(0, self.coordY(self.ylim[0])+2,
                                               0, self.coordY(self.ylim[0])+6,
                                               parent=self.item)
            lineItem.setX(x*self.col_w + self.col_w/2)
            lineItem.setPen(QtGui.QPen(QtGui.QColor('black')))
            lineItem.setZValue(10)
            text = QtGui.QGraphicsSimpleTextItem(str(x))
            text.setFont(QtGui.QFont("Arial", self.fsize-2))
            text.setParentItem(self.item)
            tw = text.boundingRect().width()
            # Center text according to masterItem size
            text.setPos(x*self.col_w-tw/2 + self.col_w/2,
                        self.coordY(self.ylim[0])+6)
        
    def coordY(self, y):
        """
        return the transformation of Y according to mean value
        (that is last element of lines)
        """
        y_offset = 30
        if self.ylim[1] <= y: return y_offset
        if self.ylim[1] == 0: return self.height + y_offset
        if self.ylim[0] >= y: return self.height + y_offset
        #return self.height - y * self.height / self.ylim[1]
        return self.height + y_offset - (y-self.ylim[0]) / (self.ylim[1]-self.ylim[0]) * self.height
            
    def draw_hlines (self, line, col):
        lineItem = QtGui.QGraphicsLineItem(0, self.coordY(line),
                                           self.width, self.coordY(line),
                                           parent=self.item)
        lineItem.setPen(QtGui.QPen(QtGui.QColor(col), 1, QtCore.Qt.DashLine))
        lineItem.setZValue(10)

    def draw_bar(self, x, y, i):
        h = self.coordY(self.ylim[0])#self.height
        coordY = self.coordY
        item = self.item
        # if value stands out of bound
        if y < self.ylim[0]: return
        if y < self.ylim[1]:
            # left line
            lineItem = QtGui.QGraphicsLineItem(0, h, 0, coordY(y), parent=item)
            lineItem.setX(x-3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
            # right line
            lineItem = QtGui.QGraphicsLineItem(0, h, 0, coordY(y), parent=item)
            lineItem.setX(x+3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
            # top line
            lineItem = QtGui.QGraphicsLineItem(0, coordY(y), 6, coordY(y), parent=item)
            lineItem.setX(x-3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
        else:
            # lower left line
            lineItem = QtGui.QGraphicsLineItem(0, h, 0, coordY(y), parent=item)
            lineItem.setX(x-3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
            # lower right line
            lineItem = QtGui.QGraphicsLineItem(0, h, 0, coordY(y), parent=item)
            lineItem.setX(x+3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
            # upper left line
            lineItem = QtGui.QGraphicsLineItem(0, coordY(y)-4, 0, coordY(y)-7, parent=item)
            lineItem.setX(x-3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
            # upper right line
            lineItem = QtGui.QGraphicsLineItem(0, coordY(y)-4, 0, coordY(y)-7, parent=item)
            lineItem.setX(x+3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
            # top line
            lineItem = QtGui.QGraphicsLineItem(0, coordY(y)-7, 6, coordY(y)-7, parent=item)
            lineItem.setX(x-3)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
        
    def draw_stick(self, x, y, i):
        lineItem = QtGui.QGraphicsLineItem(0, self.coordY(self.ylim[0]),
                                           0, self.coordY(y),
                                           parent=self.item)
        lineItem.setX(x)
        lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))

    def draw_errors(self, x, i):
        lower = self.values[i]+self._dw_err[i]
        upper = self.values[i]+self._up_err[i]
        lineItem = QtGui.QGraphicsLineItem(0, self.coordY(lower), 0,
                                           self.coordY(upper), parent=self.item)
        lineItem.setX(x)
        lineItem.setPen(QtGui.QPen(QtGui.QColor('black'),1))
        
    def draw_curve(self, x, y, i):
        # top line
        lineItem = QtGui.QGraphicsLineItem(0, self.coordY(y), 4,
                                           self.coordY(y), parent=self.item)
        lineItem.setX(x-2)
        lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))
        if i > 0:
            prev = self.values[i-1] if i>0 else self.values[i]
            lineItem = QtGui.QGraphicsLineItem(0, self.coordY(prev), self.col_w-4,
                                               self.coordY(y), parent=self.item)
            lineItem.setX(x - self.col_w+2)
            lineItem.setPen(QtGui.QPen(QtGui.QColor(self.colors[i]),2))


            
