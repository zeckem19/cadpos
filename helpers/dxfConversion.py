def defineTagWorkingArea(orderOfTags, dxfWorkingArea):
    anchorXY = dict()
    
#     dxfWorkingArea = sorted(dxfWorkingArea, key=itemgetter(0,1))
    
    for i in range(len(orderOfTags)):
        anchorXY.update({orderOfTags[i]: dxfWorkingArea[i]})
    
    return anchorXY

def parseDeca(decaData, anchorXY):
    X = anchorXY.keys()[0]
    baseX = anchorXY[X][0]
    baseY = anchorXY[X][1]
    
    tagX = decaData['TAG'][0]
    tagY = decaData['TAG'][1]
    
    tagDXFX = baseX + tagX
    tagDXFY = baseY + tagY
    
    tagPosition =(round(tagDXFX,2), round(tagDXFY,2))
    
    return tagPosition