from os import path

from KicadModTree.nodes.base import Pad, Line, Arc
from KicadModTree.nodes.specialized import RectLine, PolygoneLine

from keycap import Keycap
import util

from switch import Switch

from shapes import ShapesMX

# https://www.cherrymx.de/en/dev.html
class SwitchCherryMX(Switch, ShapesMX):

    switch_w = 14
    switch_h = 14

    def __init__(self,
                 switch_type: str = 'PCB',
                 cutout: str = 'simple',
                 **kwargs):

        if switch_type not in ['PCB', 'Plate']:
            raise ValueError(f'Switch type {switch_type} not supported.')

        if cutout not in ['simple', 'relief', None]:
            raise ValueError(f'Cutout type {cutout} not supported.')

        self.switch_type = switch_type
        self.cutout = cutout

        _name = f'SW_Cherry_MX_{switch_type}'

        super().__init__(
            name=_name,
            description=f'Cherry MX keyswitch {switch_type} Mount',
            tags=f'Cherry MX Keyboard Keyswitch Switch {switch_type}',
            cutout=True if cutout is not None else False,
            model3d=f'{_name}.wrl',
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
        self._fab_outline()
        self._silkscreen()
        self._courtyard()

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[-3.81, -2.54], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                        at=[2.54, -5.08], size=[2.5, 2.5], drill=1.5,
                        layers=['*.Cu', 'B.Mask']))
        self.centerhole(dia=4)

        if self.switch_type == 'PCB':
            self.pcb_mount_holes(dia=1.75,x=5.08)
