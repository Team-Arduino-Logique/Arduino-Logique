from ElectroComponent import *
from dataCDLT import *


board830pts = {"dimLine":66, "dimColumn":22, "sepAlim":[(0,4),(0,18.5)], "sepDistribution":[(0,10.7)]}

    
dip14 = {"pinCount":14, "chipWidth":2.4, "label":"DIP 14",  "type":"dip14"}
dip7400 = dip14.copy()
dip7400["label"] = "74HC00"  # 74HC00
dip7400["type"] = "74HC00"  # 74HC00
dip7402 = dip14.copy()
dip7402["label"] = "74HC02"  # 74HC02
dip7402["type"] = "74HC02"  # 74HC02
dip7408 = dip14.copy()
dip7408["label"] = "74HC08"  # 74HC08
dip7408["type"] = "74HC08"  # 74HC08
dip7404 = dip14.copy()
dip7404["label"] = "74HC04"  # 74HC04
dip7404["type"] = "74HC04"  # 74HC04
dip7432 = dip14.copy()
dip7432["label"] = "74HC32"  # 74HC32
dip7432["type"] = "74HC32"  # 74HC32
chipCoverOpen = {"open": YES}
chipCoverClose  = {"open": NO}
dip20 = {"pinCount":20, "chipWidth":2.4, "label":"DIP 20", "type": "dip20"}
dip60 = {"pinCount":60, "chipWidth":2.4, "label":"DIP 60", "type": "dip60"}
dip120 = {"pinCount":120, "chipWidth":2.4, "label":"DIP 120", "type": "dip120"}


pins7400 = {"logicFunction":symbNAND, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7402 = {"logicFunction":symbNOR, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7404 = {"logicFunction":symbNOT, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7408 = {"logicFunction":symbAND, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}
pins7432 = {"logicFunction":symbOR, "io":[([1, 2],[3,]), ([4, 5], [6,]), ([9, 10], [8,]), ([12, 13], [11,])]}

chipDIP14 = [(drawChip,1, {**dip14 , **chipCoverClose, "internalFunc":internalFunc})]    #, **pins7408
chip7400 = [(drawChip,1, {**dip7400 ,**chipCoverClose,  "internalFunc":internalFunc, **pins7400})]    
chip7402 = [(drawChip,1, {**dip7402 ,**chipCoverClose,  "internalFunc":internalFunc, **pins7402})]    
chip7404 = [(drawChip,1, {**dip7404 ,**chipCoverClose,  "internalFunc":internalFunc, **pins7404})]    
chip7408 = [(drawChip,1, {**dip7408 ,**chipCoverClose,  "internalFunc":internalFunc, **pins7408})]    
chip7432 = [(drawChip,1, {**dip7432 ,**chipCoverClose,  "internalFunc":internalFunc, **pins7432})]    
wireTest   = [(drawWire,1,{"color":(255,0,0,255), "mode":AUTO, "coords":[(1,3,3,2)], "matrix": matrix1260pts}), \
               (drawWire,1,{"color":(10,10,10,255), "mode":AUTO, "coords":[(35,12,35,13)], "matrix": matrix1260pts}), \
               (drawWire,1,{"color":(0,80,0,255), "mode":AUTO, "coords":[(5,10,15,10)], "matrix": matrix1260pts}), \
               (drawWire,1,{"color":(0,255,0,255), "mode":AUTO, "coords":[(2,6,40,1)], "matrix": matrix1260pts}),
               (drawWire,1,{"color":(128,128,0,255), "mode":AUTO, "coords":[(51,1,48,13)], "matrix": matrix1260pts}),
               (drawWire,1,{"color":(128,128,0,255), "mode":AUTO, "coords":[(51,15,48,27)], "matrix": matrix1260pts}),]

    
lineDistribution = [ (drawHole, 63)] #, {"colors":("#400010","#c00040","#200008")}
blocAlim = [(drawHole,5), (drawBlank,1)] #, {"colors":("#400010","#c00040","#200008")}
#railAlimMoins = [(drawBlank,1),(drawChar,1),(drawRail,60)]
railAlimMoins = [(drawBlank,1),(drawChar,1, {"deltaY":1.3,"scaleChar":2}),(drawRail,60),(drawHalfBlank,1),(drawBlank,1),(drawChar,1, {"deltaY":1.3,"scaleChar":2})]
railAlimPlus = [(drawBlank,1),(drawChar,1,{"color":"#ff0000", "text":"+", "deltaY":-0.6, "scaleChar":2}),(drawredRail,60),(drawBlank,1),(drawHalfBlank,1),(drawChar,1,{"color":"#ff0000", "text":"+", "deltaY":-0.6, "scaleChar":2})]
lineAlim = [(drawBlank,3), (blocAlim,10,{"direction":HORIZONTAL})]
bandeAlim = [(railAlimMoins,1,{"direction":VERTICAL}), (lineAlim,2,{"direction":VERTICAL}), (railAlimPlus,1,{"direction":VERTICAL})]
bandeDistribution = [(lineDistribution,5,{"direction":VERTICAL})]  
numerotation = [(drawBlank,1), (drawNumIter,1,{"beginNum":1, "endNum":63, "direction":HORIZONTAL, "deltaY":-1.5})]
#board600pts = [(drawBoard,1),(drawHalfBlank,1,HORIZONTAL),(drawHalfBlank,1,VERTICAL),(bandeAlim,1,VERTICAL), (drawBlank,1,VERTICAL), (bandeDistribution,1,VERTICAL), ([(drawBlank,1)],2,VERTICAL), (bandeDistribution,1,VERTICAL),(drawBlank,1,VERTICAL),(bandeAlim,1,VERTICAL)]
board830pts = [(setXYOrigin,1,{"idOrigin":"plq830"}),(drawBoard,1),(drawHalfBlank,1,{"direction":HORIZONTAL}),(drawHalfBlank,1,{"direction":VERTICAL}),(bandeAlim,1,{"direction":VERTICAL}), \
                   (numerotation,1,{"direction":VERTICAL}), (goXY,1,{"line":5.5, "column":0.5, "idOrigin":"plq830"}), \
                   (drawCharIter,1,{"beginChar":"f", "numChars":5, "anchor":"center", "deltaY":0.7}),(bandeDistribution,1,{"direction":VERTICAL}),(goXY,1,{"line":5.5, "column":64.5, "idOrigin":"plq830"}),(drawHalfBlank,1),(drawCharIter,1,{"beginChar":"f", "numChars":5, "direction":VERTICAL, "deltaY":0.7}), \
                   (goXY,1,{"line":12.5, "column":0.5, "idOrigin":"plq830"}), \
                   (drawCharIter,1,{"beginChar":"a", "numChars":5, "deltaY":0.7}), (bandeDistribution,1,{"direction":VERTICAL}), (goXY,1,{"line":12.5, "column":64.5, "idOrigin":"plq830"}),(drawHalfBlank,1),(drawCharIter,1,{"beginChar":"a", "numChars":5, "direction":VERTICAL, "deltaY":0.7}), \
                   (goXY,1,{"line":18.8, "column":0.5, "idOrigin":"plq830"}), (numerotation,1,{"direction":VERTICAL}),
                   (goXY,1,{"line":18.5, "column":0.5, "idOrigin":"plq830"}), (bandeAlim,1,{"direction":VERTICAL})]    # ,1,{"direction":VERTICAL})]
#,(setFoncTrou,1,{"function":drawRoundHole})
boardTest = [(setXYOrigin,1),(bandeAlim,1,{"direction":HORIZONTAL})]
boardTestMinimal = [(setXYOrigin,1),(railAlimPlus,4,{"direction":VERTICAL})]
board1260pts =[(board830pts,2,{"direction":PERSO, "dXY": (0, 1.3)})]
circuitTest = [(setXYOrigin,1,{"idOrigin":"circTest"}),(board1260pts,1), (goXY,1,{"line":10.1, "column":1.4, "idOrigin":"circTest"}), (chip7408,1,{"direction":HORIZONTAL}), \
               (chip7402,1,{"direction":HORIZONTAL}), (chip7404,1,{"direction":HORIZONTAL}), (chip7400,1,{"direction":HORIZONTAL}), (chip7432,1,{"direction":HORIZONTAL}), \
               (goXY,1,{"line":0, "column":0, "idOrigin":"circTest"}),(wireTest,1)]

