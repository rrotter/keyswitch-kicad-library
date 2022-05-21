from os import path

from KicadModTree.nodes.base import Pad, Line, Arc
from KicadModTree.nodes.specialized import RectLine, PolygoneLine

from keycap import Keycap
import util

from switch import Switch

# http://www.kailh.com/en/Products/Ks/CS/
class SwitchKailhChoc(Switch):

    switch_w = 15
    switch_h = 15

    choc_cut_w = 14.5
    choc_cut_h = 14.5

    def __init__(self,
                 switch_type: str = 'V1V2',
                 hotswap: bool = False, hotswap_plated: bool = False,
                 name: str = None,
                 cutout: bool = True,
                 model3d: str = None,
                 **kwargs):

        if switch_type not in ['V1', 'V2', 'V1V2']:
            raise ValueError(f'Switch type {switch_type} not supported.')

        if hotswap_plated is True and hotswap is False:
            raise ValueError('Hotswap plated switch must be hotswap.')

        self.hotswap = hotswap
        self.hotswap_plated = hotswap_plated

        self.switch_type = switch_type

        if model3d is None:
            if hotswap is True:
                _model3d = 'SW_Hotswap_Kailh_Choc_v1.wrl'
            else:
                _model3d = 'SW_Kailh_Choc_V1.wrl'
        else:
            _model3d = model3d


        if hotswap is True:
            _name = 'SW_Hotswap_Kailh_Choc'
        else:
            _name = 'SW_Kailh_Choc'

        _name += '_' + switch_type

        if hotswap_plated is True:
            _name += '_Plated'


        _description = 'Kailh Choc keyswitch'
        _tags = 'Kailh Choc Keyswitch Switch'

        if switch_type in ['V1', 'V1V2']:
            _description += ' CPG1350 V1'
            _tags += ' CPG1350 V1'

        if switch_type in ['V2', 'V1V2']:
            _description += ' CPG1353 V2'
            _tags += ' CPG1353 V2'

        if hotswap is True:
            _description += ' Hotswap'
            _tags += ' Hotswap'

        if hotswap_plated is True:
            _description += ' Plated'
            _tags += ' Plated'

        super().__init__(
            name=_name,
            description=_description,
            tags=_tags,
            cutout=cutout,
            model3d=_model3d,
            text_offset=9,
            **kwargs
        )

        self._init_switch()

        if cutout is True:
            self._init_cutout()

        self._init_keycap()

    def _init_switch(self):

        # set attributes
        if self.hotswap is True:
            self.setAttribute('smd')

        self._fab_outline()
        self._silkscreen()
        self._courtyard()

        if self.hotswap is True:
            # socket outline
            polyline_base = [
                [7.275, -2.225],
                [7.575, -2.225],
                [7.575, -1.425],
                [3.567, -1.425],
                [3.276,  -1.48],
                [3.025, -1.636],
                [2.848, -1.873],
                [2.769, -2.158],
                [2.612, -2.729],
                [2.258, -3.203],
                [1.756, -3.516],
                [1.175, -3.625],
                [-1.45, -3.625],
                [-2.275, -4.45],
            ]

            polyline_base2 = [
                [-2.275, -7.45],
                [-1.45, -8.275],
                [1.261, -8.275],
                [1.643, -8.199],
                [1.968, -7.982],
                [2.475, -7.475],
                [2.475, -7.275],
                [2.566, -6.816],
                [2.826, -6.426],
                [3.216, -6.166],
                [3.675, -6.075],
                [6.475, -6.075],
                [6.781, -6.014],
                [7.041, -5.841],
                [7.214, -5.581],
                [7.275, -5.275],
            ]

            # create fab outline (socket)
            self.append(PolygoneLine(polygone=polyline_base,
                                     layer='B.Fab', width=0.1))
            self.append(PolygoneLine(polygone=polyline_base2,
                                     layer='B.Fab', width=0.1))

            # create silkscreen (socket)
            # TODO: offset 0.1
            self.append(PolygoneLine(polygone=polyline_base,
                                     layer='B.SilkS', width=0.12))
            self.append(PolygoneLine(polygone=polyline_base2,
                                     layer='B.SilkS', width=0.12))

            # create courtyard (socket)
            # TODO: offset 0.25
            polyline = polyline_base + polyline_base2
            polyline.append(polyline_base[0])
            self.append(PolygoneLine(polygone=polyline,
                                     layer='B.CrtYd', width=0.05))

        # create pads
        if self.hotswap is True:
            if self.hotswap_plated is True:
                self.append(Pad(number=1, type=Pad.TYPE_THT,
                                shape=Pad.SHAPE_CIRCLE,
                                at=[0, -5.9], size=[3.6, 3.6], drill=3.05,
                                layers=['*.Cu', 'B.Mask']))
                self.append(Pad(number=2, type=Pad.TYPE_THT,
                                shape=Pad.SHAPE_CIRCLE,
                                at=[5, -3.8], size=[3.6, 3.6], drill=3.05,
                                layers=['*.Cu', 'B.Mask']))

                self.append(Pad(number=1, type=Pad.TYPE_SMT,
                                shape=Pad.SHAPE_ROUNDRECT,
                                at=[-2.85, -6], size=[3.85, 2.5],
                                round_radius_exact=0.25, layers=['B.Cu']))
                self.append(Pad(number=2, type=Pad.TYPE_SMT,
                                shape=Pad.SHAPE_ROUNDRECT,
                                at=[7.85, -3.8], size=[3.85, 2.5],
                                round_radius_exact=0.25, layers=['B.Cu']))

                self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                                at=[-3.5, -6], size=[2.55, 2.5],
                                round_radius_exact=0.25,
                                layers=['B.Mask', 'B.Paste']))
                self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                                at=[8.5, -3.8], size=[2.55, 2.5],
                                round_radius_exact=0.25,
                                layers=['B.Mask', 'B.Paste']))

                self.append(Pad(type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                at=[-5, 5.15], size=[2.6, 2.6],
                                drill=1.6, layers=['*.Cu', 'B.Mask']))

            else:
                self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                                at=[0, -5.9], size=[3.05, 3.05], drill=3.05,
                                layers=['*.Cu', '*.Mask']))
                self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                                at=[5, -3.8], size=[3.05, 3.05], drill=3.05,
                                layers=['*.Cu', '*.Mask']))

                self.append(Pad(number=1, type=Pad.TYPE_SMT,
                                shape=Pad.SHAPE_ROUNDRECT,
                                at=[-3.5, -6], size=[2.55, 2.5],
                                round_radius_exact=0.25,
                                layers=['B.Cu', 'B.Mask', 'B.Paste']))
                self.append(Pad(number=2, type=Pad.TYPE_SMT,
                                shape=Pad.SHAPE_ROUNDRECT,
                                at=[8.5, -3.8], size=[2.55, 2.5],
                                round_radius_exact=0.25,
                                layers=['B.Cu', 'B.Mask', 'B.Paste']))

                self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                                at=[-5, 5.15], size=[1.6, 1.6],
                                drill=1.6, layers=['*.Cu', '*.Mask']))
        else:
            self.append(Pad(number=1, type=Pad.TYPE_THT,
                            shape=Pad.SHAPE_CIRCLE,
                            at=[0, -5.9], size=[2.2, 2.2], drill=1.2,
                            layers=['*.Cu', 'B.Mask']))
            self.append(Pad(number=2, type=Pad.TYPE_THT,
                            shape=Pad.SHAPE_CIRCLE,
                            at=[5, -3.8], size=[2.2, 2.2], drill=1.2,
                            layers=['*.Cu', 'B.Mask']))

        if self.switch_type == 'V1':
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[0, 0], size=[3.45, 3.45], drill=3.45,
                            layers=['*.Cu', '*.Mask']))
        else:  # V2 or V1V2
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[0, 0], size=[5.05, 5.05], drill=5.05,
                            layers=['*.Cu', '*.Mask']))

        if self.switch_type in ['V1', 'V1V2']:
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[-5.5, 0], size=[1.9, 1.9], drill=1.9,
                            layers=['*.Cu', '*.Mask']))
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[5.5, 0], size=[1.9, 1.9], drill=1.9,
                            layers=['*.Cu', '*.Mask']))

        if self.switch_type in ['V2', 'V1V2']:
            if self.hotswap is False or self.hotswap_plated is True:
                self.append(Pad(type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                                at=[-5, 5.15], size=[2.6, 2.6], drill=1.6,
                                layers=['*.Cu', 'B.Mask']))
            else:
                self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                                at=[-5, 5.15], size=[1.6, 1.6], drill=1.6,
                                layers=['*.Cu', '*.Mask']))

    def _init_cutout(self):

        # create cutout
        self.append(RectLine(start=[-self.choc_cut_w/2, -self.choc_cut_h/2],
                             end=[self.choc_cut_w/2, self.choc_cut_h/2],
                             layer='Eco1.User', width=0.1))
