from os import path

from KicadModTree.nodes.base import Pad, Line, Arc
from KicadModTree.nodes.specialized import RectLine, PolygoneLine

from keycap import Keycap
import util

from switch import Switch

# https://github.com/keyboardio/keyswitch_documentation/blob/master/datasheets/ALPS/SKCL.pdf
class SwitchAlpsMatias(Switch):

    switch_w = 15.5
    switch_h = 12.8

    def __init__(self, cutout: bool = True, **kwargs):

        super().__init__(
            name='SW_Alps_Matias',
            description='Alps/Matias keyswitch',
            tags='Alps Matias Keyboard Keyswitch Switch Plate',
            cutout=cutout,
            model3d='SW_Alps_Matias.wrl',
            **kwargs
        )

        self._init_switch()

        if cutout is True:
            self._init_cutout_simple()

        self._init_keycap()

    def _init_switch(self):
        self._fab_outline()
        self._silkscreen()
        self._courtyard()

        # create pads
        self.append(Pad(number=1, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                    at=[-2.5, -4], size=[2.5, 2.5], drill=1.5,
                    layers=['*.Cu', 'B.Mask']))
        self.append(Pad(number=2, type=Pad.TYPE_THT, shape=Pad.SHAPE_CIRCLE,
                    at=[2.5, -4.5], size=[2.5, 2.5], drill=1.5,
                    layers=['*.Cu', 'B.Mask']))

