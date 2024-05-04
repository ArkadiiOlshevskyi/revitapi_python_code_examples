import logging
import inspect

logger = logging.getLogger(__name__)

"""
"frameColor":"#ffffff",
"mirrored":[
0,
0
],
"refid":"220",
"t":0.4890816847273642,
"type":"window",
"width":285,
"z":95,
"z_height":160
"""


class Window:
    """
    Window in FML is "opening" inside "wall" where wall is a host.
    1) We use this class only if Wall has Openings in its data.
    2) Wall can have many Window.
    3) Window created in Revit as NewFamilyInstance with Host(wall)
    4) Window has various parameters such ad REFID - that identify design.
    So we map REFID with FamilySymbol name in ModelsName Json.
    5) 't' is parameter that representing position of Window in wall according
    placement between wall points A(start) and B(finish) from 0 to 1.
    6) 'type' is parameter that representing type of Window (Window, window)
    7) 'width' parameter working together with Width parameter if Revit Family
    8) 'z_height' parameter working together with Height parameter if Revit Family
    9) 'z' ??????
    9) 'mirrored' ??????
    """

    def __init__(self, frameColor, mirrored, refid, t, window_type, width, height, z, z_height):
        self.frameColor = frameColor
        self.mirrored = mirrored
        self.refid = refid
        self.t = t
        self.window_type = window_type
        self.width = width
        self.height = height
        self.z = z
        self.z_height = z_height


    @classmethod
    def process_config(cls, ifc_window_config):
        """Process config Window data"""
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Trying to process config Window data in {}'.format(function_name))

        try:
            frameColor = ifc_window_config.get('frameColor', 0)
            mirrored = ifc_window_config.get('mirrored', 0)
            refid = ifc_window_config.get('refid', '')
            t = ifc_window_config.get('t', 0)
            window_type = ifc_window_config.get('type', '')  # "type" is built in name in python
            width = ifc_window_config.get('width', 0)
            height = ifc_window_config.get('height', 0)
            z = ifc_window_config.get('z', 0)
            z_height = ifc_window_config.get('z_height', 0)

            print('FML Window parameters processed....')
            return cls(frameColor, mirrored, refid, t, window_type, width, height, z, z_height)
        except Exception as e:
            logger.error('Error: {}, \n Function: {}'.format(e, function_name))
            print('Error: {}, \n Function: {}'.format(e, function_name))
            return None

    def print_parsed_data(self):
        """Just a test print function"""
        print('Window frameColor: {}'.format(self.frameColor))
        print('Window mirrored: {}'.format(self.mirrored))
        print('Window refid: {}'.format(self.refid))
        print('Window t: {}'.format(self.t))
        print('Window type: {}'.format(self.window_type))
        print('Window width: {}'.format(self.width))
        print('Window height: {}'.format(self.height))
        print('Window z: {}'.format(self.z))
        print('Window z_height: {}'.format(self.z_height))
