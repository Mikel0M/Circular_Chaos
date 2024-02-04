import csv
import pandas as pd
import sortingFunctions as sf

#print(pd.read_csv('DataList.csv'))
df = pd.read_csv("Datalist.csv")

completeListParts = []
#Create Objects acording to the list using the sortingFunctios
for n in range (len(df.index)):
    completeListParts.append(
        sf.parts(df.iloc[n]['type'], df.iloc[n]['name'], df.iloc[n]['height'], df.iloc[n]['width'],
              df.iloc[n]['depth'], df.iloc[n]['material'], df.iloc[n]['number'], 0,
              df.iloc[n]['number'], 0))

#Now let us find a match for a
length = 117
sumLength = 0
listNewElements = []
while length > 0:
    result = sf.findMatch(length,200,completeListParts)
    for char in result:
        length -= char.getWidth()
        sumLength += char.getWidth()
        listNewElements.append(char)
if sumLength < length:
        listNewElements.pop()

totalLength = 0
for char in listNewElements:
    print(char.getName())
    totalLength += char.getWidth()

print(totalLength)