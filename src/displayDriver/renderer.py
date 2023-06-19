import json

class FrameBuffer():
    def __init__(self, xDim, yDim, xOverscan = 0, yOverscan = 0):
        self.xDim = xDim
        self.yDim = yDim
        self.xOverscan = xOverscan
        self.yOverscan = yOverscan
        totalYDim = yDim + yDim
        self.buffer = [0 for y in range(totalYDim)]
        f = open('library.json')
        self.library = json.load(f)
        self.masks = self.getMasks()

    def getMasks(self):
        masks = [0]
        for i in range(1, self.xDim):
            masks.append((masks[i-1] << 1) | 0x1)
        return masks

    def getBuffer(self, xStartPos = 0, yStartPos = 0):
        if xStartPos == 0 and yStartPos == 0 and self.xOverscan == 0 and self.yOverscan == 0:
            # base case
            return self.buffer
        retBuff = []
        for y in range(self.yDim):
            buffY = yStartPos + y
            if buffY < len(self.buffer):
                retBuff.append((self.buffer[buffY] >> xStartPos) | self.masks[self.xDim])
            else:
                retBuff.append(0)

        return retBuff

    def drawText(self, string, xStart, yStart, font = "tiny3x5"):
        libFont = self.library[font]

        # pre-scan to find max height and ensure there are no unknown chars
        maxY = 0
        for i in range(len(string)):
            currChar = string[i]
            if currChar in libFont:
                maxY = max(maxY, libFont[currChar][0][1])
            else:
                raise Exception("Unrecognized character: " + currChar + " in font " + font)
        textBuff = [0 for y in range(maxY)]
        for i in reversed(range(len(string))):
            currChar = string[i]
            charDim = libFont[currChar][0]
            charMap = libFont[currChar][1]
            for y in range(maxY):
                row = textBuff[y]
                row = row << (charDim[0] + 1)
                if y < charDim[1]:
                    row |= self.masks[charDim[0]] & charMap[y]
                textBuff[y] = row

        for y in range(maxY):
            self.buffer[y + yStart] |= textBuff[y] << xStart

buff = FrameBuffer(32, 16)
buff.drawText("Hello", 0, 4, "londonReg")
print(buff.getBuffer())
