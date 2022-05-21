from os import path

from KicadModTree.nodes.Footprint import Footprint
from KicadModTree.nodes.base import Text, Model, Pad, Line, Arc
from KicadModTree.nodes.specialized import RectLine, PolygoneLine

from keycap import Keycap
import util


class Switch(Footprint):
    def __init__(self, name: str, description: str, tags: str,
                 cutout: bool = False, keycap: Keycap = None,
                 path3d: str = None, model3d: str = None,
                 text_offset: float = 8):

        Footprint.__init__(self, None)

        self.name = name
        self.description = description
        self.tags = tags
        self.text_offset = text_offset
        self.path3d = None

        if model3d is not None:
            self.path3d = model3d
            if path3d is not None:
                self.path3d = path.join(path3d, self.path3d)

        if cutout is True:
            self.tags += ' Cutout'

        if keycap is not None:
            self.name += '_' + keycap.name
            self.description += f' with {keycap.tags} keycap'
            self.tags += ' ' + keycap.tags

        self.name.replace(' ', '_')

        self._init_generic_nodes()

    def _init_generic_nodes(self):
        # add general values
        self.append(Text(type='reference', text='REF**',
                         at=[0, -self.text_offset], layer='F.SilkS'))
        self.append(Text(type='value', text=self.name,
                         at=[0, self.text_offset], layer='F.Fab'))
        self.append(Text(type='user', text='%R',
                         at=[0, 0], layer='F.Fab'))

        # add model if available
        if self.path3d is not None:
            self.append(Model(filename=self.path3d,
                        at=[0, 0, 0], scale=[1, 1, 1], rotate=[0, 0, 0]))

# http://www.kailh.com/en/Products/Ks/CS/
class SwitchKailhChocV1(Switch):

    choc_w = 15
    choc_h = 15

    choc_cut_w = 14.5
    choc_cut_h = 14.5

    def __init__(self,
                 name: str = 'SW_Kailh_Choc_V1',
                 description: str = 'Kailh Choc V1 (CPG1350) keyswitch',
                 tags: str = 'Kailh Choc V1 CPG1350 Keyswitch Switch',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Kailh_Choc_V1.wrl'):

        Switch.__init__(self,
                        name=name,
                        description=description,
                        tags=tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d,
                        text_offset=9)

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # create fab outline
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.Fab', width=0.1))

        # create silkscreen
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create courtyard
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 5.9], size=[2.2, 2.2], drill=1.2,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-5, 3.8], size=[2.2, 2.2], drill=1.2,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[3.2, 3.2], drill=3.2,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.5, 0], size=[1.8, 1.8], drill=1.8,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[5.5, 0], size=[1.8, 1.8], drill=1.8,
                        layers=['*.Cu', '*.Mask']))

    def _init_cutout(self):

        # create cutout
        self.append(RectLine(start=[-self.choc_cut_w/2, -self.choc_cut_h/2],
                             end=[self.choc_cut_w/2, self.choc_cut_h/2],
                             layer='Eco1.User', width=0.1))


class SwitchHotswapKailhChocV1(Switch):

    choc_w = 15
    choc_h = 15

    choc_cut_w = 14.5
    choc_cut_h = 14.5

    def __init__(self,
                 name: str = 'SW_Hotswap_Kailh_Choc_V1',
                 description: str = 'Kailh keyswitch Hotswap Socket',
                 tags: str = 'Kailh Keyboard Choc V1 keyswitch Keyswitch Switch Hotswap Socket',
                 cutout: bool = True, keycap: Keycap = None,
                 path3d: str = None, model3d: str = 'SW_Hotswap_Kailh_Choc_v1.stp'):

        _name=name
        _tags=tags
        _description=description

        Switch.__init__(self,
                        name=_name,
                        description=_description,
                        tags=_tags,
                        cutout=cutout,
                        keycap=keycap,
                        path3d=path3d,
                        model3d=model3d,
                        text_offset=9)

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        if keycap is not None:
            self.append(keycap)

    def _init_switch(self):

        # set attributes
        self.setAttribute('smd')

        # socket outline
        polyline_base = [
            [-7.275, 5.265],
            [-7.064, 5.831],
            [-6.458, 6.075],
            [-3.433, 6.075],
            [-2.850, 6.350],
            [-2.500, 6.950],
            [-2.500, 7.475],
            [-1.700, 8.275],
            [1.475, 8.275],
            [2.275, 7.475],
        ]

        polyline_base2 = [
            [2.275, 4.425],
            [1.475, 3.625],
            [-0.500, 3.625],
            [-1.162, 3.534],
            [-1.565, 3.318],
            [-2.150, 2.709],
            [-2.400, 2.050],
            [-2.700, 1.650],
            [-3.300, 1.425],
            [-6.475, 1.425],
            [-7.020, 1.688],
            [-7.275, 2.225],
        ]

        # create fab outline (keyswitch)
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.Fab', width=0.1))

        # create fab outline (socket)
        self.append(PolygoneLine(polygone=polyline_base,
                                 layer='B.Fab', width=0.1))
        self.append(PolygoneLine(polygone=polyline_base2,
                                 layer='B.Fab', width=0.1))

        # create silkscreen (keyswitch)
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.SilkS', width=0.12, offset=0.1))

        # create silkscreen (socket)
        # TODO: offset 0.1
        self.append(PolygoneLine(polygone=polyline_base,
                                 layer='B.SilkS', width=0.12))
        self.append(PolygoneLine(polygone=polyline_base2,
                                 layer='B.SilkS', width=0.12))

        # create courtyard (keyswitch)
        self.append(RectLine(start=[-self.choc_w/2, -self.choc_h/2],
                             end=[self.choc_w/2, self.choc_h/2],
                             layer='F.CrtYd', width=0.05, offset=0.25))

        # create courtyard (socket)
        # TODO: offset 0.25
        polyline = polyline_base + polyline_base2
        polyline.append(polyline_base[0])
        self.append(PolygoneLine(polygone=polyline,
                                 layer='B.CrtYd', width=0.05))

        # create pads
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 5.95], size=[3, 3], drill=3,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5, 3.75], size=[3, 3], drill=3,
                        layers=['*.Cu', '*.Mask']))

        self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[3.275, 5.95], size=[2.6, 2.6],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))
        self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[-8.275, 3.75], size=[2.6, 2.6],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))

        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[3.4, 3.4], drill=3.4,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.5, 0], size=[1.9, 1.9], drill=1.9,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[5.5, 0], size=[1.9, 1.9], drill=1.9,
                        layers=['*.Cu', '*.Mask']))

    def _init_cutout(self):

        # create cutout
        self.append(RectLine(start=[-self.choc_cut_w/2, -self.choc_cut_h/2],
                             end=[self.choc_cut_w/2, self.choc_cut_h/2],
                             layer='Eco1.User', width=0.1))