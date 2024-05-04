import logging
import inspect

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector, ViewFamilyType


logger = logging.getLogger(__name__)


def level_create(document, level_name, project_height):
    """
    Creating Revit level from FML data.

    Business logic:
        1) check if level exists in revit(usually two levels, first in point wall), chose it as first floor
        2) select it and store it in to variable and hst level

    Parameters:
        - ifc_document (type): Active Revit Document.
        - level_name (type): Name parsed from FML.
        - project_height (type): Commutative parameter extracted from FML
                                Pay ATTENTION that FML has Centimeters needed to be converted
                                to Revit foots.

    Returns:
        # type: Creating of new level.

    Raises:
        # ExceptionType: Transaction errors or mistakes in Input.

    Examples:
        # >>> level_create(ifc_document, Level.name, Level.project_height)
    """

    function_name = inspect.currentframe().f_code.co_name
    logger.info('Creating Level {}'.format(function_name))
    print('Creating Level {}'.format(function_name))

    try:
        t = Transaction(document, 'Creating new level')

        t.Start()

        new_level = Level.Create(document, project_height)  # Change this to processor CM from FML
        new_level_name = new_level.get_Parameter(BuiltInParameter.DATUM_TEXT)
        new_level_name.Set(level_name)
        scope_box_param = new_level.get_Parameter(BuiltInParameter.LEVEL_PARAM)
        print('===> scope box parameter'.format(scope_box_param))
        print(type(scope_box_param))
        print(dir(scope_box_param))

        t.Commit()

        logger.info('Successfully created new level -> {}'.format(new_level.Name))
        print('Successfully created new level -> {}'.format(new_level.Name))

    except Exception as e:
        logger.error('Error while creating level -> {}'.format(e))
        print('Error while creating level -> {}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            logger.error(t.GetStatus())
            print(t.GetStatus())


# ############### TEST CASE ############################# Example usage
# ifc_document = __revit__.ActiveUIDocument.Document
# level_name = "NEW TEST LEVEL"
# REVIT_UNITS = 50.55
# 
# selected_level = level_create(ifc_document, level_name, REVIT_UNITS)
# #
# # if selected_level:
# #     print('Selected level Name: {}'.format(selected_level.Name))
# #     print('Selected level ID: {}'.format(selected_level.Id))
# #     print(type(selected_level))
# #     print(dir(selected_level))
# # else:
# #     print('Failed to select level.')
