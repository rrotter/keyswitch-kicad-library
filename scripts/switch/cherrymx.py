from os import path

from KicadModTree.nodes.base import Pad, Line, Arc
from KicadModTree.nodes.specialized import RectLine, PolygoneLine

from keycap import Keycap
import util

from switch import Switch

# https://www.cherrymx.de/en/dev.html
class SwitchCherryMX(Switch):

    cherry_w = 14
    cherry_h = 14

    def __init__(self,
                 switch_type: str = 'PCB',
                 name: str = 'SW_Cherry_MX',
                 description: str = 'Cherry MX keyswitch',
                 tags: str = 'Cherry MX Keyboard Keyswitch Switch',
                 cutout: str = 'simple', keycap: Keycap = None,
                 path3d: str = None, model3d: str = None):

        if switch_type not in ['PCB', 'Plate']:
            raise ValueError(f'Switch type {switch_type} not supported.')

        if cutout not in ['simple', 'relief', None]:
            raise ValueError(f'Cutout type {cutout} not supported.')

        self.switch_type = switch_type
        self.cutout = cutout

        _name = name + '_' + switch_type
        _description = description + ' ' + switch_type + ' Mount'
        _tags = tags + ' ' + switch_type

        Switch.__init__(self,
                        name=_name,
                        description=_description,
                        tags=_tags,
                        cutout=True if cutout is not None else False,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d if model3d is not None
                        else f'{_name}.wrl')

        self._init_switch()

        if cutout is not None:
            if cutout == 'simple':
                self._init_cutout_simple()
            elif cutout == 'relief':
                self._init_cutout_relief()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # create fab outline
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))
        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-3.81, -2.54], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[2.54, -5.08], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[4, 4], drill=4,
                        layers=['*.Cu', '*.Mask']))

        if self.switch_type == 'PCB':
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[-5.08, 0], size=[1.75, 1.75], drill=1.75,
                            layers=['*.Cu', '*.Mask']))
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[5.08, 0], size=[1.75, 1.75], drill=1.75,
                            layers=['*.Cu', '*.Mask']))

    def _init_cutout_simple(self):

        # create cutout
        self.append(RectLine(start=[-self.cherry_w/2, -self.cherry_h/2],
                             end=[self.cherry_w/2, self.cherry_h/2],
                             layer='Eco1.User', width=0.1))

    def _init_cutout_relief(self):

        # create cutout
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
