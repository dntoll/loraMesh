
from ansiconsole.ANSIEscape import ANSIEscape
import math

class ValueView:
    def __init__(self, value, title, unit, decimals, x, y, color, background, detail):
        self.value = value
        self.title = title
        self.unit = unit
        self.x = x 
        self.y = y
        self.decimals = decimals #number of decimals
        self.color = color #forground color
        self.background = background #background color
        self.detail = detail
    
    def getText(self, number):
        numberFormat = "{:." + str(self.decimals) + "f}"
        return  numberFormat.format(number) + self.unit

    def get(self, height):
        val = self.value

        ret = ""
        #ret += self.bufferGraph(height)
        ret += ANSIEscape.goToXY(self.x, self.y) + ANSIEscape.getBackgroundColor(self.background) + ANSIEscape.getTextColor(self.color)

        if self.detail == 0:
            ret += self.getText(val.value)
        if self.detail >= 1:
            ret += self.title + ": " + self.getText(val.value) + ANSIEscape.goToXY(self.x, self.y+1)
        if self.detail >= 2:
            ret += "max :" + self.getText(val.max) + ANSIEscape.goToXY(self.x, self.y+2)
            ret += "avg :" + self.getText(val.getAverage()) + ANSIEscape.goToXY(self.x, self.y+3)
            ret += "min :" + self.getText(val.min) + ANSIEscape.goToXY(self.x, self.y+4)

        if self.detail >= 3:
            ran = val.max - val.min
            if ran > 0:
                fraktion = (val.value - val.min) / ran
                at = int(10.0 * fraktion)
            else:
                at = 0
            
            ret += "[" + '-' *at + 'O' + '-' * (10-at)  + "]"

        return ret + ANSIEscape.getResetCode()

