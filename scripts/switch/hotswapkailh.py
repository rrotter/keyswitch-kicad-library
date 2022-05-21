from os import path

from KicadModTree.nodes.base import Pad, Line, Arc
from KicadModTree.nodes.specialized import RectLine, PolygoneLine

from keycap import Keycap
import util

from switch import Switch


class SwitchHotswapKailh(Switch):

    switch_w = 14
    switch_h = 14

    def __init__(self,
                 plated_th: bool = False,
                 cutout: str = 'relief',
                 **kwargs):

        if cutout not in ['simple', 'relief', None]:
            raise ValueError(f'Cutout type {cutout} not supported.')

        self.cutout = cutout
        self.plated_th = plated_th

        _name='SW_Hotswap_Kailh_MX'
        _tags='Kailh Keyboard Keyswitch Switch Hotswap Socket'
        _description='Kailh keyswitch Hotswap Socket'

        if self.plated_th is True:
            _name += '_plated'
            _tags += ' plated'
            _description += ' plated holes'

        super().__init__(
            name=_name,
            description=_description,
            tags=_tags,
            cutout=True if cutout is not None else False,
            model3d='SW_Hotswap_Kailh_MX.wrl',
            **kwargs
        )

        self._init_switch()

        if cutout is not None:
            if cutout == 'simple':
                self._init_cutout_simple()
            elif cutout == 'relief':
                self._init_cutout_relief()

        self._init_keycap()

    def _init_switch(self):

        # set attributes
        self.setAttribute('smd')

        # create fab outline (keyswitch)
        self._fab_outline()

        # create fab outline (socket)
        self.append(Line(start=[-4, -6.8], end=[4.8, -6.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[4.8, -6.8], end=[4.8, -2.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[-0.3, -2.8], end=[4.8, -2.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[-6, -0.8], end=[-2.3, -0.8],
                    layer='B.Fab', width=0.12))
        self.append(Line(start=[-6, -0.8], end=[-6, -4.8],
                    layer='B.Fab', width=0.12))
        self.append(Arc(center=[-4, -4.8], start=[-4, -6.8],
                    angle=-90, layer='B.Fab', width=0.12))
        self.append(Arc(center=[-0.3, -0.8], start=[-0.3, -2.8],
                    angle=-90, layer='B.Fab', width=0.12))

        # create silkscreen (keyswitch)
        self._silkscreen()

        # create silkscreen (socket)
        self.append(Line(start=[-4.1, -6.9], end=[1, -6.9],
                         layer='B.SilkS', width=0.12))
        self.append(Line(start=[-0.2, -2.7], end=[4.9, -2.7],
                         layer='B.SilkS', width=0.12))
        self.append(Arc(center=[-4.1, -4.9], start=[-4.1, -6.9],
                        angle=-90, layer='B.SilkS', width=0.12))
        self.append(Arc(center=[-0.2, -0.7], start=[-0.2, -2.7],
                        angle=-90, layer='B.SilkS', width=0.12))

        # create courtyard (keyswitch)
        self._courtyard()

        # create courtyard (socket)
        # !TODO: add KLC correct offset (0.25)
        self.append(Line(start=[-4, -6.8], end=[4.8, -6.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[4.8, -6.8], end=[4.8, -2.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[-0.3, -2.8], end=[4.8, -2.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[-6, -0.8], end=[-2.3, -0.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Line(start=[-6, -0.8], end=[-6, -4.8],
                    layer='B.CrtYd', width=0.05))
        self.append(Arc(center=[-4, -4.8], start=[-4, -6.8],
                    angle=-90, layer='B.CrtYd', width=0.05))
        self.append(Arc(center=[-0.3, -0.8], start=[-0.3, -2.8],
                    angle=-90, layer='B.CrtYd', width=0.05))

        # create pads
        if self.plated_th is True:
            self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[-3.81, -2.54], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))
            self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                            at=[2.54, -5.08], size=[3.6, 3.6], drill=3.05,
                            layers=['*.Cu', 'B.Mask']))

            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-6.585, -2.54], size=[3.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[5.32, -5.08], size=[3.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Cu']))

            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[-7.085, -2.54], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
            self.append(Pad(type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                            at=[5.842, -5.08], size=[2.55, 2.5],
                            round_radius_exact=0.25, layers=['B.Mask', 'B.Paste']))
        else:
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[-3.81, -2.54], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))
            self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                            at=[2.54, -5.08], size=[3.05, 3.05], drill=3.05,
                            layers=['*.Cu', '*.Mask']))

            self.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[-7.085, -2.54], size=[2.55, 2.5],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))
            self.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_ROUNDRECT,
                        at=[5.842, -5.08], size=[2.55, 2.5],
                        round_radius_exact=0.25, layers=['B.Cu', 'B.Mask', 'B.Paste']))

        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[0, 0], size=[4, 4], drill=4,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[-5.08, 0], size=[1.75, 1.75], drill=1.75,
                        layers=['*.Cu', '*.Mask']))
        self.append(Pad(type=Pad.TYPE_NPTH, shape=Pad.SHAPE_CIRCLE,
                        at=[5.08, 0], size=[1.75, 1.75], drill=1.75,
                        layers=['*.Cu', '*.Mask']))
