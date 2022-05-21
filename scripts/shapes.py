from KicadModTree.nodes.specialized import PolygoneLine
from KicadModTree.nodes.base import Pad

class ShapesMX:
    def _init_cutout_relief(self):
        # create mx "relief" cutout
        polyline = [[7, -7],
                    [7, -6],
                    [7.8, -6],
                    [7.8, -2.9],
                    [7, -2.9],
                    [7, 2.9],
                    [7.8, 2.9],
                    [7.8, 6],
                    [7, 6],
                    [7, 7],
                    [-7, 7],
                    [-7, 6],
                    [-7.8, 6],
                    [-7.8, 2.9],
                    [-7, 2.9],
                    [-7, -2.9],
                    [-7.8, -2.9],
                    [-7.8, -6],
                    [-7, -6],
                    [-7, -7],
                    [7, -7]]

        self.append(PolygoneLine(polygone=polyline,
                                 layer='Eco1.User', width=0.1))

class ShapesHotswap:
    def _pads(self):
    
        # create pads
        if self.plated_th is True:
            # hotswap socket mount holes, plated
            self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[-3.81, -2.54], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))
            self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[2.54, -5.08], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))

            # bridge plated holes to pad 
            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-6.585, -2.54], size=[3.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[5.32, -5.08], size=[3.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))

            # hotswap socket pads
            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-7.085, -2.54], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[5.842, -5.08], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
        else:
            # hotswap socket mount holes
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[-3.81, -2.54], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[2.54, -5.08], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))

            # hotswap socket pads
            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[-7.085, -2.54], size=[2.55, 2.5],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[5.842, -5.08], size=[2.55, 2.5],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))
