import logging
import inspect
from Autodesk.Revit.DB import XYZ

logging.getLogger(__name__)


def get_orientation_point(point):
    """
    Getting orientation point for Revit model.
    """

    function_name = inspect.currentframe().f_code.co_name  # testing Get current function name
    logging.info('Trying to get orientation point...')
    print('Trying to get orientation point...')

    try:
        get_z = point.Z
        orientation_point = point - XYZ(0, 0, get_z)
        print('Orientation point: {}'.format(orientation_point))
        return orientation_point

    except Exception as e:
        print('Error in get_orientation_point: {}'.format(e))
        logging.error('Error: {}, \n Function: {}'.format(e, function_name))
        return None
