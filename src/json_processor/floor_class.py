import logging
import inspect

logger = logging.getLogger(__name__)

# FAIL POLY IS MIGHT BE ROOF


"""
public static Floor Create(
	Document ifc_document,
	IList<CurveLoop> profile,
	ElementId floorTypeId,
	ElementId levelId
)
"""


class Floor:
    """
    Floor in FML might is geometry object
    that consist from points, joined in polyline,
    and extruded with negative value(f.e. -200mm)
    Just ike a flat slab.
    !!!Floor IS NOT Level!!!

    FML file contains "floors" -> "designs" ->"areas" -> "poly"

    Logic:
    1) We parse FML for "floors" -> "level" and get value f.ex. 0
    2) "Name" is context name for floor means Name of the room
    3) Joining points in polyline
    4) Creating New Floor in Revit
    """

    def __init__(self, name, x, y):
        #TODO polyline???
        self.name = name
        self.x = x
        self.y = y
    @classmethod
    def process_config(cls, item_config):
        """Process config item data"""
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Trying to process config Level data in {}'.format(function_name))

        try:
            for x, y in poly in areas:
                name = item_config.get('name', 0)
                x = item_config.get('x', 0)
                y = item_config.get('y', 0)
                # TODO extrusion controll

            print('FML Item parameters processed....')
            return cls(x, y, name)
        except Exception as e:
            logger.error('Error: {}, \n Function: {}'.format(e, function_name))
            print('Error: {}, \n Function: {}'.format(e, function_name))
            return None

    def print_parsed_data(self):
        """Just a test print function"""
        print('Level name: {}'.format(self.poly_x))
        print('Level level: {}'.format(self.poly_y))
        print('Level height: {}'.format(self.height))
