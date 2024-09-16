from component_params import DIP14_PARAMS
from component_sketch import ComponentSketcher
from dataCDLT import AUTO, YES, NO, matrix1260pts, HORIZONTAL, VERTICAL, PERSO

# TODO: refactor to use small data classes for chips, boards, etc.
class ComponentData:

    def __init__(self, sketcher: ComponentSketcher):
        self.sketcher = sketcher

        dip7400 = DIP14_PARAMS.copy()
        dip7400["label"] = "74HC00"  # 74HC00
        dip7400["type"] = "74HC00"  # 74HC00
        dip7402 = DIP14_PARAMS.copy()
        dip7402["label"] = "74HC02"  # 74HC02
        dip7402["type"] = "74HC02"  # 74HC02
        dip7408 = DIP14_PARAMS.copy()
        dip7408["label"] = "74HC08"  # 74HC08
        dip7408["type"] = "74HC08"  # 74HC08
        dip7404 = DIP14_PARAMS.copy()
        dip7404["label"] = "74HC04"  # 74HC04
        dip7404["type"] = "74HC04"  # 74HC04
        dip7432 = DIP14_PARAMS.copy()
        dip7432["label"] = "74HC32"  # 74HC32
        dip7432["type"] = "74HC32"  # 74HC32
        chipCoverOpen = {"open": YES}
        chipCoverClose = {"open": NO}
        dip20 = {"pinCount": 20, "chipWidth": 2.4, "label": "DIP 20", "type": "dip20"}
        dip60 = {"pinCount": 60, "chipWidth": 2.4, "label": "DIP 60", "type": "dip60"}
        dip120 = {"pinCount": 120, "chipWidth": 2.4, "label": "DIP 120", "type": "dip120"}


        pins7400 = {
            "logicFunction": self.sketcher.symbNAND,
            "io": [
                (
                    [1, 2],
                    [
                        3,
                    ],
                ),
                (
                    [4, 5],
                    [
                        6,
                    ],
                ),
                (
                    [9, 10],
                    [
                        8,
                    ],
                ),
                (
                    [12, 13],
                    [
                        11,
                    ],
                ),
            ],
        }
        pins7402 = {
            "logicFunction": self.sketcher.symbNOR,
            "io": [
                (
                    [1, 2],
                    [
                        3,
                    ],
                ),
                (
                    [4, 5],
                    [
                        6,
                    ],
                ),
                (
                    [9, 10],
                    [
                        8,
                    ],
                ),
                (
                    [12, 13],
                    [
                        11,
                    ],
                ),
            ],
        }
        pins7404 = {
            "logicFunction": self.sketcher.symbNOT,
            "io": [
                (
                    [1, 2],
                    [
                        3,
                    ],
                ),
                (
                    [4, 5],
                    [
                        6,
                    ],
                ),
                (
                    [9, 10],
                    [
                        8,
                    ],
                ),
                (
                    [12, 13],
                    [
                        11,
                    ],
                ),
            ],
        }
        pins7408 = {
            "logicFunction": self.sketcher.symbAND,
            "io": [
                (
                    [1, 2],
                    [
                        3,
                    ],
                ),
                (
                    [4, 5],
                    [
                        6,
                    ],
                ),
                (
                    [9, 10],
                    [
                        8,
                    ],
                ),
                (
                    [12, 13],
                    [
                        11,
                    ],
                ),
            ],
        }
        pins7432 = {
            "logicFunction": self.sketcher.symbOR,
            "io": [
                (
                    [1, 2],
                    [
                        3,
                    ],
                ),
                (
                    [4, 5],
                    [
                        6,
                    ],
                ),
                (
                    [9, 10],
                    [
                        8,
                    ],
                ),
                (
                    [12, 13],
                    [
                        11,
                    ],
                ),
            ],
        }

        chipDIP14 = [(self.sketcher.drawChip, 1, {**DIP14_PARAMS, **chipCoverClose, "internalFunc": self.sketcher.internalFunc})]  # , **pins7408
        chip7400 = [(self.sketcher.drawChip, 1, {**dip7400, **chipCoverClose, "internalFunc": self.sketcher.internalFunc, **pins7400})]
        chip7402 = [(self.sketcher.drawChip, 1, {**dip7402, **chipCoverClose, "internalFunc": self.sketcher.internalFunc, **pins7402})]
        chip7404 = [(self.sketcher.drawChip, 1, {**dip7404, **chipCoverClose, "internalFunc": self.sketcher.internalFunc, **pins7404})]
        chip7408 = [(self.sketcher.drawChip, 1, {**dip7408, **chipCoverClose, "internalFunc": self.sketcher.internalFunc, **pins7408})]
        chip7432 = [(self.sketcher.drawChip, 1, {**dip7432, **chipCoverClose, "internalFunc": self.sketcher.internalFunc, **pins7432})]
        wireTest = [
            (self.sketcher.drawWire, 1, {"color": (255, 0, 0, 255), "mode": AUTO, "coords": [(1, 3, 3, 2)], "matrix": matrix1260pts}),
            (self.sketcher.drawWire, 1, {"color": (10, 10, 10, 255), "mode": AUTO, "coords": [(35, 12, 35, 13)], "matrix": matrix1260pts}),
            (self.sketcher.drawWire, 1, {"color": (0, 80, 0, 255), "mode": AUTO, "coords": [(5, 10, 15, 10)], "matrix": matrix1260pts}),
            (self.sketcher.drawWire, 1, {"color": (0, 255, 0, 255), "mode": AUTO, "coords": [(2, 6, 40, 1)], "matrix": matrix1260pts}),
            (self.sketcher.drawWire, 1, {"color": (128, 128, 0, 255), "mode": AUTO, "coords": [(51, 1, 48, 13)], "matrix": matrix1260pts}),
            (self.sketcher.drawWire, 1, {"color": (128, 128, 0, 255), "mode": AUTO, "coords": [(51, 15, 48, 27)], "matrix": matrix1260pts}),
        ]


        self.line_distribution = [(self.sketcher.drawHole, 63)]  # , {"colors":("#400010","#c00040","#200008")}
        blocAlim = [(self.sketcher.drawHole, 5), (self.sketcher.drawBlank, 1)]  # , {"colors":("#400010","#c00040","#200008")}
        # railAlimMoins = [(self.sketcher.drawBlank,1),(self.sketcher.drawChar,1),(self.sketcher.drawRail,60)]
        railAlimMoins = [
            (self.sketcher.drawBlank, 1),
            (self.sketcher.drawChar, 1, {"deltaY": 1.3, "scaleChar": 2}),
            (self.sketcher.drawRail, 60),
            (self.sketcher.drawHalfBlank, 1),
            (self.sketcher.drawBlank, 1),
            (self.sketcher.drawChar, 1, {"deltaY": 1.3, "scaleChar": 2}),
        ]
        railAlimPlus = [
            (self.sketcher.drawBlank, 1),
            (self.sketcher.drawChar, 1, {"color": "#ff0000", "text": "+", "deltaY": -0.6, "scaleChar": 2}),
            (self.sketcher.drawredRail, 60),
            (self.sketcher.drawBlank, 1),
            (self.sketcher.drawHalfBlank, 1),
            (self.sketcher.drawChar, 1, {"color": "#ff0000", "text": "+", "deltaY": -0.6, "scaleChar": 2}),
        ]
        lineAlim = [(self.sketcher.drawBlank, 3), (blocAlim, 10, {"direction": HORIZONTAL})]
        bandeAlim = [
            (railAlimMoins, 1, {"direction": VERTICAL}),
            (lineAlim, 2, {"direction": VERTICAL}),
            (railAlimPlus, 1, {"direction": VERTICAL}),
        ]
        bandeDistribution = [(self.line_distribution, 5, {"direction": VERTICAL})]
        numerotation = [
            (self.sketcher.drawBlank, 1),
            (self.sketcher.drawNumIter, 1, {"beginNum": 1, "endNum": 63, "direction": HORIZONTAL, "deltaY": -1.5}),
        ]
        # board600pts = [(self.sketcher.drawBoard,1),(self.sketcher.drawHalfBlank,1,HORIZONTAL),(self.sketcher.drawHalfBlank,1,VERTICAL),(bandeAlim,1,VERTICAL), (self.sketcher.drawBlank,1,VERTICAL), (bandeDistribution,1,VERTICAL), ([(self.sketcher.drawBlank,1)],2,VERTICAL), (bandeDistribution,1,VERTICAL),(self.sketcher.drawBlank,1,VERTICAL),(bandeAlim,1,VERTICAL)]
        board830pts = [
            (self.sketcher.setXYOrigin, 1, {"id_origin": "bboard830"}),
            (self.sketcher.drawBoard, 1),
            (self.sketcher.drawHalfBlank, 1, {"direction": HORIZONTAL}),
            (self.sketcher.drawHalfBlank, 1, {"direction": VERTICAL}),
            (bandeAlim, 1, {"direction": VERTICAL}),
            (numerotation, 1, {"direction": VERTICAL}),
            (self.sketcher.goXY, 1, {"line": 5.5, "column": 0.5, "id_origin": "bboard830"}),
            (self.sketcher.drawCharIter, 1, {"beginChar": "f", "numChars": 5, "anchor": "center", "deltaY": 0.7}),
            (bandeDistribution, 1, {"direction": VERTICAL}),
            (self.sketcher.goXY, 1, {"line": 5.5, "column": 64.5, "id_origin": "bboard830"}),
            (self.sketcher.drawHalfBlank, 1),
            (self.sketcher.drawCharIter, 1, {"beginChar": "f", "numChars": 5, "direction": VERTICAL, "deltaY": 0.7}),
            (self.sketcher.goXY, 1, {"line": 12.5, "column": 0.5, "id_origin": "bboard830"}),
            (self.sketcher.drawCharIter, 1, {"beginChar": "a", "numChars": 5, "deltaY": 0.7}),
            (bandeDistribution, 1, {"direction": VERTICAL}),
            (self.sketcher.goXY, 1, {"line": 12.5, "column": 64.5, "id_origin": "bboard830"}),
            (self.sketcher.drawHalfBlank, 1),
            (self.sketcher.drawCharIter, 1, {"beginChar": "a", "numChars": 5, "direction": VERTICAL, "deltaY": 0.7}),
            (self.sketcher.goXY, 1, {"line": 18.8, "column": 0.5, "id_origin": "bboard830"}),
            (numerotation, 1, {"direction": VERTICAL}),
            (self.sketcher.goXY, 1, {"line": 18.5, "column": 0.5, "id_origin": "bboard830"}),
            (bandeAlim, 1, {"direction": VERTICAL}),
        ]  # ,1,{"direction":VERTICAL})]
        # ,(setFoncTrou,1,{"function":drawRoundHole})
        boardTest = [(self.sketcher.setXYOrigin, 1), (bandeAlim, 1, {"direction": HORIZONTAL})]
        boardTestMinimal = [(self.sketcher.setXYOrigin, 1), (railAlimPlus, 4, {"direction": VERTICAL})]
        board1260pts = [(board830pts, 2, {"direction": PERSO, "dXY": (0, 1.3)})]
        self.circuitTest = [
            (self.sketcher.setXYOrigin, 1, {"id_origin": "circTest"}),
            (board1260pts, 1),
            (self.sketcher.goXY, 1, {"line": 10.1, "column": 1.4, "id_origin": "circTest"}),
            (chip7408, 1, {"direction": HORIZONTAL}),
            (chip7402, 1, {"direction": HORIZONTAL}),
            (chip7404, 1, {"direction": HORIZONTAL}),
            (chip7400, 1, {"direction": HORIZONTAL}),
            (chip7432, 1, {"direction": HORIZONTAL}),
            (self.sketcher.goXY, 1, {"line": 0, "column": 0, "id_origin": "circTest"}),
            (wireTest, 1),
        ]
