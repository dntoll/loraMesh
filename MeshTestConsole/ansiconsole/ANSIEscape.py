class ANSIEscape:
    COLORS = {
        "Black": "0",
        "Red": "1",
        "Green": "2",
        "Yellow": "3",
        "Blue": "4",
        "Magenta": "5",
        "Cyan": "6",
        "White": "7",}

    def getTextColor(colorString):
        return "\u001b[3" + ANSIEscape.COLORS[colorString] + "m"

    def getBrightColor(colorString):
        return "\u001b[3" + ANSIEscape.COLORS[colorString] + ";1m"
    
    def getBackgroundColor(colorString):
        return "\u001b[4"+ ANSIEscape.COLORS[colorString] + "m"

    def getBrightBackgroundColor(colorString):
        return "\u001b[4"+ ANSIEscape.COLORS[colorString] + ";1m"

    #RGB between 0-5
    def getColorBackgroundColorRGB(r, g, b):
        index = 16 + 36 * r + 6 * g + b
        return "\u001b[48;5;" + str(index) + "m"
        """ https://en.wikipedia.org/wiki/ANSI_escape_code
        0-  7:  standard colors (as in ESC [ 30–37 m)
        8- 15:  high intensity colors (as in ESC [ 90–97 m)
        16-231:  6 × 6 × 6 cube (216 colors): 16 + 36 × r + 6 × g + b (0 ≤ r, g, b ≤ 5)
        232-255:  grayscale from black to white in 24 steps"""


    def getResetCode():
        return "\u001b[0m"

    def getBold():
        return "\u001b[1m"
    def getUnderline():
        return "\u001b[4m"
    def getReversed(): 
        return "\u001b[7m"
    
    def goToXY(x, y):
        return "\u001b[" +str(y) + ";"+ str(x)+"H"


    def clearScreen():
        return "\u001b[2J"

    def moveCursorUp(n):
        return "\u001b[{n}A"
    
    def moveCursorDown(n):
        return "\u001b[{n}B"
    
    def moveCursorRight(n):
        return "\u001b[{n}C"

    def moveCursorLeft(n):
        return "\u001b[{n}D"

    def clearFromCursorToEnd():
        return "\u001b[0J"
    def clearFromCursorToBeginning():
        return "\u001b[1J"
    def clearScreen():
        return "\u001b[2J"

    def clearLineCursorToEnd(): 
        return "\u001b[0K"
    def clearLineCursorToStart(): 
        return "\u001b[1K"
    def clearLine():
        return "\u001b[2K"

    def saveState():
        return "\u001b7"
    def loadState():
        return "\u001b8"

