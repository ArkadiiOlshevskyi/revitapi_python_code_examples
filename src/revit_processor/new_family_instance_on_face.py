import logging
import inspect

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import StructuralType  # THIS IN CRUCIAL FOR WINDOW OR NEW FAMILY INSTANCE CREATION

logger = logging.getLogger(__name__)


def create_new_revit_model_instance_on_FACE(document,
                                            ifc_face_to_place,
                                            revit_orientation_point,
                                            revit_family_symbol,
                                            revit_model_XYZ_location_point,
                                            revit_model_width,
                                            revit_model_height):

                                            # revit_model_rotation_value,
                                            # rotation_axis
    """
    Inserts a new instance of a family_symbol onto a face of an existing element, using a location, reference direction, and a type/symbol
    constructor for new family_symbol instance creation on FACE on IFC model(box)
    input:
        ifc_document
        ifc_face_to_place
        revit_orientation_point
        revit_family_symbol
        revit_model_XYZ_location_point
        revit_model_length
        revit_model_width
        revit_model_height
        revit_model_rotation_value
        rotation_axis

    return:
    -> new Revit model instance on the FACE
    """
    function_name = inspect.currentframe().f_code.co_name  # testing Get current function name
    logging.info('Creating new family_symbol... with {}'.format(function_name))

    t = Transaction(document, "Creating new family_symbol on FACE")

    try:
        print('Revit Function -> Creating new Revit model instance on XYZ...')
        logging.info('Revit Function -> Creating new Revit model instance on XYZ...'.format(function_name))

        t.Start()

        new_model = document.Create.NewFamilyInstance(ifc_face_to_place, revit_model_XYZ_location_point,
                                                      revit_orientation_point, revit_family_symbol)

        # APPLY PARAMETERS:
        new_model.LookupParameter('Width').Set(revit_model_width)
        new_model.LookupParameter('Height').Set(revit_model_height)


        t.Commit()
        #
        # logging.info('Revit Function -> Creating new Revit model instance on XYZ...'.format(function_name))
        print('Revit Function -> New family_symbol instance created: {}'.format(new_model))

    except Exception as e:
        logger.error('Error: {}, \n Function: {}'.format(e, function_name))
        print('Error: {}, \n Function: {}'.format(e, function_name))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            pass
            print('Skipping Creation New Family on Face...{}'.format(t.GetStatus()))
