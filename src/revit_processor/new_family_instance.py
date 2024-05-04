import logging
import inspect

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralType  # THIS IN CRUCIAL FOR WINDOW OR NEW FAMILY INSTANCE CREATION

logger = logging.getLogger(__name__)


def create_new_revit_model_instance_on_XYZ(document,
                                           revit_family_symbol,
                                           revit_model_XYZ_location_point,
                                           revit_model_length,
                                           revit_model_width,
                                           revit_model_height,
                                           revit_model_rotation_value,
                                           rotation_axis):
    '''
    constructor for new family_symbol instance creation
    input:
    >- XYZ point
    >- revit_family_symbol

    return:
    -> new Revit model instance
    '''
    function_name = inspect.currentframe().f_code.co_name  # testing Get current function name
    logging.info('Creating new family_symbol... with {}'.format(function_name))

    try:
        print('Revit Function -> Creating new Revit model instance on XYZ...')
        logging.info('Revit Function -> Creating new Revit model instance on XYZ...'.format(function_name))

        new_model = document.Create.NewFamilyInstance(revit_model_XYZ_location_point,
                                                      revit_family_symbol,
                                                      StructuralType.NonStructural)
        # APPLY PARAMETERS:
        new_model.LookupParameter('Length').Set(revit_model_length)
        new_model.LookupParameter('Width').Set(revit_model_width)
        new_model.LookupParameter('Height').Set(revit_model_height)

        # ROTATION FAMILY INSTANCE:
        print('Rotating Element ...')
        rotation_Z_axis = rotation_axis
        element_rotated = new_model.Location.Rotate(rotation_Z_axis, revit_model_rotation_value)
        print('Element Rotated... {}'.format(element_rotated))

        logging.info('Revit Function -> Creating new Revit model instance on XYZ...'.format(function_name))
        print('Revit Function -> New family_symbol instance created: {}'.format(new_model))

    except Exception as e:
        logger.error('Error: {}, \n Function: {}'.format(e, function_name))
        print('Error: {}, \n Function: {}'.format(e, function_name))
        return None

