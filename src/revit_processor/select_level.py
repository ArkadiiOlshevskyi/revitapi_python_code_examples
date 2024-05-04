import logging
import inspect

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *

logger = logging.getLogger(__name__)


def select_level_by_name(document, level_name):
    """
    Selects a level by name.

    Args:
        document (Document): The Revit ifc_document.
        level_name (str): The name of the level to select.

    Returns:
        Element: The selected level element if found, otherwise None.
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Trying to select a level by Name {}'.format(function_name))
    print('Trying to select a level by Name {}'.format(function_name))

    try:
        # Retrieve all levels from the ifc_document
        levels = FilteredElementCollector(document).OfCategory(
            BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()
        print(type(levels))

        # Iterate through levels and find the one with the specified name
        selectedLevel = None
        for level in levels:
            if level.Name == level_name:
                selectedLevel = level
                break

        # Check if the level was found
        if selectedLevel:
            logger.info('Level Selected!')
            print('Level Selected!')
            return selectedLevel
        else:
            print('Level {} not found'.format(level_name))
            logging.info('Level {} not found'.format(level_name))
            return None
    except Exception as ex:
        logger.error('Error while selecting level by name {}'.format(ex))
        print('Error while selecting level by name {}'.format(ex))
        return None


# ############### TEST CASE ############################# Example usage
# ifc_document = __revit__.ActiveUIDocument.Document
# level_name = "L5"
# selected_level = select_level_by_name(ifc_document, level_name)
#
# if selected_level:
#     print('Selected level Name: {}'.format(selected_level.Name))
#     print('Selected level ID: {}'.format(selected_level.Id))
#     print(type(selected_level))
#     print(dir(selected_level))
# else:
#     print('Failed to select level.')
