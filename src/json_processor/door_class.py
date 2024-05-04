import logging
import inspect

logger = logging.getLogger(__name__)

"""
"frameColor":"#ffffff",
"mirrored":[
0,
0
],
"refid":"208",
"t":0.2897576907219706,
"type":"door",
"width":100,
"z":0,
"z_height":215
"""


class Door_Window:
    """
    Door_Window in FML is "opening" inside "wall" where wall is a host.
    1) We use this class only if Wall has Openings in its data.
    2) Wall can have many Doors.
    3) Door_Window created in Revit as NewFamilyInstance with Host(wall)
    4) Door_Window has various parameters such ad REFID - that identify design.
    So we map REFID with FamilySymbol name in ModelsName Json.
    5) 't' is parameter that representing position of Door_Window in wall according
    placement between wall points A(start) and B(finish) from 0 to 1.
    6) 'type' is parameter that representing type of Door_Window (door, window)
    7) 'width' parameter working together with Width parameter if Revit Family
    8) 'z_height' parameter working together with Height parameter if Revit Family
    9) 'z' ??????
    9) 'mirrored' ??????
    """

    def __init__(self, frameColor, mirrored, refid, t, opening_type, width, height, z, z_height):
        self.frameColor = frameColor
        self.mirrored = mirrored
        self.refid = refid
        self.t = t
        self.opening_type = opening_type
        self.width = width
        self.height = height
        self.z = z
        self.z_height = z_height


    @classmethod
    def process_config(cls, ifc_door_config):
        """Process config Door_Window data"""
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Trying to process config door data in {}'.format(function_name))

        try:
            frameColor = ifc_door_config.get('frameColor', 0)
            mirrored = ifc_door_config.get('mirrored', 0)
            refid = ifc_door_config.get('refid', '')
            t = ifc_door_config.get('t', 0)
            door_type = ifc_door_config.get('type', '')  # "type" is built in name in python
            width = ifc_door_config.get('width', 0)
            height = ifc_door_config.get('height', 0)
            z = ifc_door_config.get('z', 0)
            z_height = ifc_door_config.get('z_height', 0)

            print('FML Door_Window parameters processed....')
            return cls(frameColor, mirrored, refid, t, door_type, width, height, z, z_height)
        except Exception as e:
            logger.error('Error: {}, \n Function: {}'.format(e, function_name))
            print('Error: {}, \n Function: {}'.format(e, function_name))
            return None

    def print_parsed_data(self):
        """Just a test print function"""
        print('Door_Window frameColor: {}'.format(self.frameColor))
        print('Door_Window mirrored: {}'.format(self.mirrored))
        print('Door_Window refid: {}'.format(self.refid))
        print('Door_Window t: {}'.format(self.t))
        print('Door_Window type: {}'.format(self.opening_type))
        print('Door_Window width: {}'.format(self.width))
        print('Door_Window height: {}'.format(self.height))
        print('Door_Window z: {}'.format(self.z))
        print('Door_Window z_height: {}'.format(self.z_height))
