def defineTagWorkingArea(orderOfTags, dxfWorkingArea):
    anchorXY = dict()
    
#     dxfWorkingArea = sorted(dxfWorkingArea, key=itemgetter(0,1))
    
    for i in range(len(orderOfTags)):
        anchorXY.update({orderOfTags[i]: dxfWorkingArea[i]})
    
    return anchorXY

def parseDeca(decaData, anchorXY):
    baseX = min([anchorXY[pt][0] for pt in anchorXY.keys()])
    baseY = min([anchorXY[pt][1] for pt in anchorXY.keys()])
    
    tagX = decaData['TAG'][0]
    tagY = decaData['TAG'][1]
    
    tagDXFX = baseX + tagX
    tagDXFY = baseY + tagY
    
    tagPosition =(round(tagDXFX,2), round(tagDXFY,2))
    
    return tagPosition