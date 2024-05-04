import logging
import inspect
from Autodesk.Revit.DB import *

logging.getLogger(__name__)


def get_position_point(face):
    """
    Getting orientation point for Revit model.
    By receiving on input face of element.
    """

    function_name = inspect.currentframe().f_code.co_name   # testing Get current function name
    logging.info('Trying to get position point')

    try:
        for lines in face.GetEdgesAsCurveLoops():
            list_of_lines = list(lines)
            vertical_line_of_face_for_orientation_point = list_of_lines[1]
            horizontal_line_of_planar_face = list_of_lines[2]

            point_1 = vertical_line_of_face_for_orientation_point.GetEndPoint(0)
            print('Point 1: {}'.format(point_1))
            point_2 = horizontal_line_of_planar_face.GetEndPoint(1)
            print('Point 2: {}'.format(point_2))
            position_point = (point_1 + point_2) / 2
            print('Position point: {}'.format(position_point))  # returns line
            return position_point

    except Exception as e:
        print('Error in get_position_point: {}'.format(e))
        logging.error('Error: {}, \n Function: {}'.format(e, function_name))
        return None
