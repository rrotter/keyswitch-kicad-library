import argparse
import os

from KicadModTree.KicadFileHandler import KicadFileHandler

from keycap import Keycap

from switch import SwitchKailhChocV1, \
                   SwitchHotswapKailhChocV1

# SPACING = 19.05 # Standard 0.75 Inches
SPACING = 19 # Round (in metric) 19mm common on Preonic and other OLKBs

# CHOC_SPACING_X = 18
# CHOC_SPACING_Y = 17
CHOC_SPACING_X = 19
CHOC_SPACING_Y = 18.5

path3d = '${KICAD6_3RD_PARTY}/3dmodels/' \
         'com_github_perigoso_keyswitch-kicad-library/' \
         '3d-library.3dshapes/'

keycaps = {
    '1u': {'keycap_type': 'regular', 'width': 1},
    '1.25u': {'keycap_type': 'regular', 'width': 1.25},
    '1.25u90': {'keycap_type': 'regular', 'width': 1.25, 'rotation': 90},
    '1.5u': {'keycap_type': 'regular', 'width': 1.5},
    '1.5u90': {'keycap_type': 'regular', 'width': 1.5, 'rotation': 90},
    '1.75u': {'keycap_type': 'regular', 'width': 1.75},
    '1.75u90': {'keycap_type': 'regular', 'width': 1.75, 'rotation': 90},
    '2u': {'keycap_type': 'regular', 'width': 2},
    '2u90': {'keycap_type': 'regular', 'width': 2, 'rotation': 90},
}

def generate_switch_kailh_choc_v1(output_path):
    x_spacing = CHOC_SPACING_X
    y_spacing = CHOC_SPACING_Y
    # group = 'Switch_Keyboard_Kailh'
    group = 'Keyswitch_Choc'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.5u', '2u']

    switches = []

    switches.append(SwitchKailhChocV1(path3d=path3d))

    for key in keys:
        switches.append(SwitchKailhChocV1(path3d=path3d,
                                          keycap=Keycap(x_spacing=x_spacing,
                                                        y_spacing=y_spacing,
                                                        **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


def generate_switch_hotswap_kailh_choc_v1(output_path):
    x_spacing = CHOC_SPACING_X
    y_spacing = CHOC_SPACING_Y
    # group = 'Switch_Keyboard_Hotswap_Kailh'
    group = 'Keyswitch_Choc_Socket'
    out_path = os.path.join(output_path, f'{group}.pretty')
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    keys = ['1u', '1.25u', '1.5u', '2u']

    switches = []

    switches.append(SwitchHotswapKailhChocV1(path3d=path3d))

    for key in keys:
        switches.append(SwitchHotswapKailhChocV1(path3d=path3d,
                                                 keycap=Keycap(x_spacing=x_spacing,
                                                               y_spacing=y_spacing,
                                                               **keycaps[key])))

    for switch in switches:
        file_handler = KicadFileHandler(switch)
        file_handler.writeFile(os.path.join(out_path, f'{switch.name}.kicad_mod'), timestamp=0)


if __name__ == '__main__':
    # --------------------- Parser ---------------------
    parser = argparse.ArgumentParser(
        description='Generate keyswitch kicad library.',
        usage='%(prog)s [options]')

    parser.add_argument('-o', '--output',
                        type=str, default='./output',
                        help='output path '
                             '(default: %(default)s)')

    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    generate_switch_kailh_choc_v1(args.output)
    generate_switch_hotswap_kailh_choc_v1(args.output)
