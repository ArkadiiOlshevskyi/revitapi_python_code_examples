import sys
import math  # for radians in revit rotation parameter
import logging

sys.path.append(r'C:\Users\3duni\Desktop\Arkadii\2_projects_tasks\8_revit_api_converter_3\converter\utils')

logger = logging.getLogger(__name__)
# DIVIDER_REVIT = 25.4
DIVIDER_REVIT = 30.48  # THIS IS FIXED VALUE USED TO CONVERT FML CENTEMITERS TO REVIT FOOTS
"""IF WE CHANGE NUMBERS FOR UNIT CONVERT WE DO IT ONLY HERE!!!!"""


def log_exceptions(func):
    """
    Decorator used to wrap functions in:
    - try / except form
    - logging (info, error)
    - inspecting(to see failed function name in logs).
    """

    def wrapper(*args, **kwargs):
        function_name = func.__name__
        try:
            logging.info('Trying to parse FML file {}'.format(function_name))
            return func(*args, **kwargs)
        except Exception as e:
            logger.error('Error: {}, \n in Function: {}'.format(e, function_name))
            print('Error: {}, \n in Function: {}'.format(e, function_name))
            return None

    return wrapper


@log_exceptions
def x_revit(x_fml):
    if x_fml == 0:
        return 0
    else:
        x = x_fml / float(DIVIDER_REVIT)
        return x


# Sometimes we have problems here like -> unsupported operand type(s) for /: 'dict' and 'float',
# TODO Wall base offset aka balance : 0.016404199475065617 - why revit returns this value???
def y_revit(y_fml):
    if y_fml == 0:
        return 0
    else:
        y = y_fml / float(DIVIDER_REVIT) * -1  # * -1 because of Revit Y axis is opposite to FML Y axis
        return y


@log_exceptions
def z_revit(z_fml):
    if z_fml == 0:
        return 0
    else:
        z = z_fml / DIVIDER_REVIT
    return z


@log_exceptions
def width_revit(width_fml):
    width = width_fml / DIVIDER_REVIT
    return width


@log_exceptions
def height_revit(height_fml):
    height = height_fml / DIVIDER_REVIT
    return height


@log_exceptions
def z_height_revit(z_height_fml):
    if z_height_fml == 0:
        return 0
    else:
        z_height = z_height_fml / DIVIDER_REVIT
    return z_height


@log_exceptions  # Version works 100% success
def rotation_revit(rotation_fml):
    """
    In Floor planer, in FML file are different values for rotation and flipped Y axis, that's why formula is so strange
    """
    print('Original rotation value from fml -> {}'.format(rotation_fml))
    adjusted_rotation_fml = ((rotation_fml - 270) % 360) * (
        -1)  # Adjust rotation by adding 90 degrees and ensure result is within [0, 360) range
    rotation_rad = math.radians(adjusted_rotation_fml)
    return rotation_rad

# # ###### TEST CASE ##########################################################################
# X -> 63.448122087022128
# y -> -2.2970669334404774
# z -> 0.0
# location point -> (1611.582301010, 58.345500109, 0.0)
# ###### TEST CASE ##########################################################################
# Typical ITEM data - Needed to de Converted
# x = 63.44
# # x = 1699.5823010103622        # Previous
# y = -2.29
# # y = 142.54850010938833        # Previous
# z = 0
# name_x = 0
# name_y = 0
# width = 77
# height = 77
# z_height = 0
# rotation = 1
# rotation_x = 0
# rotation_y = 0


# print('X - Original: {}, Converted -> {}'.format(x, x_revit(x)))
# print('Y - Original: {}, Converted -> {}'.format(y, y_revit(y)))
# print('Z - Original: {}, Converted -> {}'.format(z, z_revit(z)))
# print('name_x - Original: {}, Converted -> {}'.format(name_x, x_revit(name_x)))
# print('name_y - Original: {}, Converted -> {}'.format(name_y, y_revit(name_y)))
# print('width - Original: {}, Converted -> {}'.format(width, width_revit(width)))
# print('height - Original: {}, Converted -> {}'.format(height, height_revit(height)))
# print('z_height - Original: {}, Converted -> {}'.format(z_height, z_height_revit(z_height)))
# print('rotation - Original: {}, Converted -> {}'.format(rotation, rotation_revit(rotation)))
# print('rotation_x - Original: {}, Converted -> {}'.format(rotation_x, rotation_revit(rotation_x)))
# print('rotation_y - Original: {}, Converted -> {}'.format(rotation_y, rotation_revit(rotation_y)))
