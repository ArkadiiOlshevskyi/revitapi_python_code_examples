import logging
import inspect

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *

logger = logging.getLogger(__name__)


def select_and_set_default_zero_level(document, level_name_to_set):
    """
    This function selects the level with elevation value 0 and renames it.

    Args:
        document (Document): The Active UI Revit ifc_document.
        level_name_to_set (str): The name to set for the selected level.

    Returns:
        Element: The selected level if found, None otherwise.
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Trying to select Default Zero Level in Revit -> {}'.format(function_name))
    print('Trying to select Default Zero Level in Revit -> {}'.format(function_name))

    t = Transaction(document, 'Setting Default Zero level')

    try:
        # Retrieve all levels from the ifc_document
        levels = FilteredElementCollector(document).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

        # Iterate through levels and check elevation parameter
        for level in levels:
            elevation_param = level.get_Parameter(BuiltInParameter.LEVEL_ELEV)
            if elevation_param and elevation_param.AsDouble() == 0:
                # Change the level name
                t.Start()
                level.Name = level_name_to_set
                t.Commit()

                logger.info('Default level selected and renamed Successfully! {}'.format(t.GetStatus()))
                print('Default level selected and renamed Successfully! {}'.format(t.GetStatus()))

                return level

        # If no level with elevation 0 is found
        print('Default Revit Level {} not found'.format(level_name_to_set))
        logging.info('Default Revit  {} not found'.format(level_name_to_set))
        return None

    except Exception as ex:
        logger.error('Error while selecting level by name {}'.format(ex))
        print('Error while selecting level by name {}'.format(ex))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            print(t.GetStatus())
            return None


# ################################# TEST CASE -> WORKS TESTED #################################
# ifc_document = __revit__.ActiveUIDocument.Document
# selected_level = select_and_set_default_zero_level(ifc_document, "NAME FROM FML")
#
# if selected_level:
#     print('Default Level Name is -> {}'.format(selected_level.Name))
#     print('Default Level ID is -> {}'.format(selected_level.Id))
# else:
#     print("Failed to select level.")
