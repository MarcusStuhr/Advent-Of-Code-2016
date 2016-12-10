import re
from collections import defaultdict

DATA_FILENAME = "data.txt"
BOT_TAG = "bot"
OUTPUT_TAG = "output"
PART_1_CHIP_LIST = [17, 61]

lines = open(DATA_FILENAME).read().split("\n")
bots = defaultdict(list)
outputBins = defaultdict(list)
director = {BOT_TAG: bots, OUTPUT_TAG: outputBins}
commands = {}

for line in lines:
    if line.startswith("value"):
        chipId, botId = map(int, re.findall(r"([\d]+)", line))
        bots[botId].append(chipId)
    else:
        fromBotId, lowId, highId = map(int, re.findall(r"([\d]+)", line))
        lowLoc, highLoc = re.findall(r" ({}|{})".format(BOT_TAG, OUTPUT_TAG), line)
        commands[fromBotId] = [(lowLoc, lowId), (highLoc, highId)]

while bots:
    for botId in list(bots.keys()):
        if len(bots[botId]) == 2:
            chipList = sorted(bots.pop(botId))
            if chipList == PART_1_CHIP_LIST:
                print(botId) #part 1 answer
            for index, (loc, chipId) in enumerate(commands[botId]):
                director[loc][chipId].append(chipList[index])

print(outputBins[0][0] * outputBins[1][0] * outputBins[2][0]) #part 2 answer