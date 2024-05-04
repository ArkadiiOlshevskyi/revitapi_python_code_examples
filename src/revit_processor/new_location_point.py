import inspect
import logging

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import XYZ, Transaction

# Configure logging
logger = logging.getLogger(__name__)


def get_t_point_coordinates(document, x_point, y_point, z_point):
    """
    Interpolates a point T between two given points A and B using linear interpolation.

    Args:
        document (revit object): Active Revit Document.
        x_point (float): Coordinates of point A as a tuple (x, y, z).
        y_point (float): Coordinates of point B as a tuple (x, y, z).
        z_point (float): Coordinate adjusted with 'z' value from fml that responsible for lifting the window or door.

    Returns:
        XYZ Revit Point
               Returns None if any error occurs during transaction.

    Raises:
        TypeError: If the input arguments are not of the expected types.
        ValueError: If the value of t is outside the valid range [0, 1].
        Exception: For any other unexpected errors.
    """
    function_name = inspect.currentframe().f_code.co_name
    print('Trying to get correct t coordinate for door and window instance -> {}'.format(function_name))
    logger.info('Trying to get correct t coordinate for door and window instance -> {}'.format(function_name))

    t = Transaction(document, "Creating Location location point")

    try:
        t.Start()
        t_raw_point_xyz = XYZ(x_point, y_point, z_point)
        t.Commit()

        logger.info('Successfully created Raw location point X -> {}'.format(t_raw_point_xyz.X))
        print('Successfully created Raw location point X -> {}'.format(t_raw_point_xyz.X))
        print('Successfully created Raw location point Y -> {}'.format(t_raw_point_xyz.Y))
        print('Successfully created Raw location point Z -> {}'.format(t_raw_point_xyz.Z))

        return t_raw_point_xyz

    except Exception as e:
        print('Error while getting T_point -> {}'.format(e))
        logger.error('Error while getting T_point -> {}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
        # pass



# # ############# TEST CASE ######################:
#
# ifc_document = __revit__.ActiveUIDocument.Document
#
# Point_A = (-11.191413750, -3.465035797, 27.559055118)
# Point_B = (-64.360705088, -23.465035797, 47.559055118)
# #t = 0.4956633272162606
# t_point = 0.0256633272162606
#
#
# t_coordinates = get_t_point_coordinates(ifc_document, Point_A, Point_B, t_point)
