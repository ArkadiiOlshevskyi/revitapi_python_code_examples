import logging

logger = logging.getLogger(__name__)


class Wall:
    """
    Wall in FML :
    1) Check floor in FML -> select floor(level) and store it in variable
        fml -> "floors" -> "level": 0,1,2
        height -> 280 cm, meaning
        if level exist in revit - store it in variable, else CreateNewLevel
    2) There are only one type of wall, so we are Selecting WallType Family to use it
    3) Parsing FML wall data (coordinates, parameters, openness)
        3.1) if Opening is exists -> Also extract the data for Window and Door_Window, store data to variable
    4) Create NewWall (A-B)  A________B
    5) Select this wall as Host and store it in variable
    6) If Opening in wall is True, and it's Window/Door_Window => create NewWindowInstance/NewDoorInstance
    Then parce next wall if FML.....
    """

    def __init__(self,
                 a,
                 a_x,
                 a_y,
                 az,
                 az_h,
                 az_z,
                 b,
                 b_x,
                 b_y,
                 bz,
                 bz_h,
                 bz_z,
                 thickness,
                 balance,
                 decor,
                 openings):

        self.a = a
        self.a_x = a_x
        self.a_y = a_y
        self.az = az
        self.az_h = az_h
        self.az_z = az_z
        self.b = b
        self.b_x = b_x
        self.b_y = b_y
        self.bz = bz
        self.bz_h = bz_h
        self.bz_z = bz_z
        self.thickness = thickness
        self.balance = balance
        self.decor = decor
        self.openings = openings

    @classmethod
    def process_config(cls, item_config):
        """
        Process configuration data for a wall.

        Args:
            item_config (dict): Configuration data for the wall.

        Returns:
            Wall: A Wall object if processing is successful, None otherwise.
        """
        try:
            a = item_config.get('a', {"x": 0, "y": 0})
            b = item_config.get('b', {"x": 0, "y": 0})
            az = item_config.get('az', {"z": 0, "h": 0})
            az_h = az.get('h', 0)
            az_z = az.get('z', 0)
            bz = item_config.get('bz', {"z": 0, "h": 0})
            bz_h = bz.get('h', 0)
            bz_z = bz.get('z', 0)
            thickness = item_config.get('thickness', 0)
            balance = item_config.get('balance', 0)
            decor = item_config.get('decor', {})
            openings = item_config.get('openings', {})

            # Extracting x and y values for points a and b
            a_x = a.get('x', 0)
            a_y = a.get('y', 0)
            b_x = b.get('x', 0)
            b_y = b.get('y', 0)

            logger.info('Wall parameters processed successfully.')
            print('Wall parameters processed successfully.')
            return cls(a, a_x, a_y, az, az_h, az_z, b, b_x, b_y, bz, bz_h, bz_z, thickness, balance, decor, openings)

        except KeyError as e:
            logger.error('KeyError: %s', e)
            print('KeyError: %s', e)
            return None

    def print_parsed_data(self):
        """
        Print parsed data of the wall.
        """
        print('a: {}'.format(self.a))
        print('b: {}'.format(self.b))
        print('a_x: {}'.format(self.a_x))
        print('a_y: {}'.format(self.a_y))
        print('b_x: {}'.format(self.b_x))
        print('b_y: {}'.format(self.b_y))
        print('az: {}'.format(self.az))
        print('az_h: {}'.format(self.az_h))
        print('az_z: {}'.format(self.az_z))
        print('bz: {}'.format(self.bz))
        print('bz_h: {}'.format(self.bz_h))
        print('bz_z: {}'.format(self.bz_z))
        print('thickness: {}'.format(self.thickness))
        print('balance: {}'.format(self.balance))
        print('decor: {}'.format(self.decor))
        print('openings: {}'.format(self.openings))
