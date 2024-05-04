import inspect
import logging

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import XYZ, Transaction

# Configure logging
logger = logging.getLogger(__name__)


def get_t_point_coordinates(document, a_point, b_point, t_value, correct_z):
    """
    Interpolates a point T between two given points A and B using linear interpolation.

    Args:
        document (revit object): Active Revit Document.
        a_point (tuple): Coordinates of point A as a tuple (x, y, z).
        b_point (tuple): Coordinates of point B as a tuple (x, y, z).
        t_value (float): Value between 0 and 1 representing the position of point T between A and B.
        correct_z (float): Value between 0 and 1 representing the position of point T between A and B.

    Returns:
        tuple: Coordinates of point T as a tuple (x, y, z).
               Returns None if any error occurs during interpolation.

    Raises:
        TypeError: If the input arguments are not of the expected types.
        ValueError: If the value of t is outside the valid range [0, 1].
        Exception: For any other unexpected errors.
    """
    function_name = inspect.currentframe().f_code.co_name
    print('Trying to get correct T coordinate for door and window instance -> {}'.format(function_name))
    logger.info('Trying to get correct t coordinate for door and window instance -> {}'.format(function_name))

    t = Transaction(document, "Creating Raw location point")

    try:
        x_A = a_point[0]
        y_A = a_point[1]
        z_A = a_point[2]

        x_B = b_point[0]
        y_B = b_point[1]
        z_B = b_point[2]

        # Calculate differences between coordinates of A and B
        delta_x = x_B - x_A
        delta_y = y_B - y_A
        delta_z = z_B - z_A

        # Calculate coordinates of point T using linear interpolation
        x_t = x_A + t_value * delta_x
        y_t = y_A + t_value * delta_y
        z_t = z_A + t_value * delta_z
        print('Previous Z coordinate for t_value -> {}'.format(z_t))

        # correcting Z point
        final_z = z_t + correct_z

        # Create a new XYZ object for point T
        t.Start()
        t_raw_point_xyz = XYZ(x_t, y_t, final_z)
        t.Commit()

        logger.info('Successfully created Raw location point X -> {}'.format(t_raw_point_xyz))
        # print('Successfully created Raw location point X -> {}'.format(t_raw_point_xyz.X))
        # print('Successfully created Raw location point Y -> {}'.format(t_raw_point_xyz.Y))
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

#
# # """
# GOOD RESULT
# Trying to get correct t coordinate for door and window instance -> get_t_point_coordinates
# Successfully extracted T coordinates
# X_t -> -12.555914671463785
# Y_t -> -3.9783023413252119
# Z_t -> 28.072321662325212
# Final t_point -> (-12.555914671, -3.978302341, 28.072321662)
# >>>
# Trying to get correct t coordinate for door and window instance -> get_t_point_coordinates
# Successfully extracted T coordinates
# X_t -> -37.545481600323782
# Y_t -> -13.378302341325213
# Z_t -> 37.472321662325214
# Final t_point -> (-37.545481600, -13.378302341, 37.472321662)
# >>>
# Trying to get correct t coordinate for door and window instance -> get_t_point_coordinates
# Successfully extracted T coordinates
# X_t -> -58.813198135523791
# Y_t -> -21.37830234132521
# Z_t -> 45.472321662325214
# Final t_point -> (-58.813198136, -21.378302341, 45.472321662)
# """
