import re, pytesseract
from PIL import Image

SCREEN_WIDTH = 50
SCREEN_HEIGHT = 6
PIXEL_ON = '#'
PIXEL_OFF = '.'
screen = [[PIXEL_OFF] * SCREEN_WIDTH for i in range(SCREEN_HEIGHT)]
DATA_FILENAME = "data.txt"
lines = open(DATA_FILENAME).read().split("\n")

def rect(screen, a ,b):
    for col in range(a):
        for row in range(b):
            screen[row][col] = PIXEL_ON

def rotateCol(screen, colIndex, amount):
    amount %= SCREEN_HEIGHT
    colData = [screen[r][colIndex] for r in range(SCREEN_HEIGHT)]
    colData = colData[-amount:] + colData[:-amount]
    for r in range(SCREEN_HEIGHT):
        screen[r][colIndex] = colData[r]

def rotateRow(screen, rowIndex, amount):
    amount %= SCREEN_WIDTH
    screen[rowIndex] = screen[rowIndex][-amount:] + screen[rowIndex][:-amount]

def countLit(screen):
    return sum(row.count(PIXEL_ON) for row in screen)

def printScreen(screen):
    for row in screen:
        print(''.join(row))

def screenToText(screen):
    multiplier = 9
    im = Image.new('RGBA', (SCREEN_WIDTH, SCREEN_HEIGHT), (255,255,255,255))
    pix = im.load()
    for r in range(len(screen)):
        for c in range(len(screen[r])):
            if screen[r][c] == PIXEL_ON:
                color = (0, 0, 0, 255)
            else:
                color = (255, 255, 255, 255)
            pix[c, r] = color
    im = im.resize((SCREEN_WIDTH * multiplier, SCREEN_HEIGHT * multiplier))
    im.save("test.png", "PNG")
    return pytesseract.image_to_string(im)

for line in lines:
    a, b = map(int, re.findall("\d+", line))
    splitline = line.split()
    if splitline[0] == "rect":
        rect(screen, a, b)
    else:
        if splitline[1] == "row":
            rotateRow(screen, a, b)
        else:
            rotateCol(screen, a, b)

print(countLit(screen)) #part 1 answer
printScreen(screen) #part 2 answer, afbupzbjps
print("OCR scan attempt: <" + screenToText(screen) + ">") #TODO: Still blank
