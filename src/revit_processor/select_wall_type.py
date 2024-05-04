import inspect
import logging
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

logger = logging.getLogger(__name__)


def select_wall_type(document, wall_type_name):
    """
    Selects a wall type by name.

    Parameters:
        - ifc_document (Document): Active Revit Document.
        - wall_type_name (str): Name of the wall type.

    Returns:
        WallType: Selected wall type if found, None otherwise.

    Raises:
        ValueError: If wall type with the given name is not found.
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Selecting wall type: {}'.format(wall_type_name))
    print('Selecting wall type: {}'.format(wall_type_name))

    try:
        collector = FilteredElementCollector(document).OfCategory(BuiltInCategory.OST_Walls)
        wall_types = collector.WhereElementIsElementType().ToElements()

        for wall_type in wall_types:
            if wall_type.Name == wall_type_name:
                logger.info('Successfully selected wall type: {}'.format(wall_type_name))
                print('Successfully selected wall type: {}'.format(wall_type_name))
                return wall_type

        raise ValueError("Wall type '{}' not found.".format(wall_type_name))

    except Exception as e:
        logger.error('Error selecting wall type: {}'.format(str(e)))
        print('Error selecting wall type: {}'.format(str(e)))
        raise

# ################### test case ##################
# doc = __revit__.ActiveUIDocument.Document
#
# # Get the wall type you want to use
# name = "Default_floorplaner_wall"
#
# pre_selected_wall_type = select_wall_type(doc, name)
#
# print('Select type wall ID -> {}'.format(pre_selected_wall_type.Id))
# print('Select type wall Name -> {}'.format(pre_selected_wall_type.Name))
# # print(dir(pre_selected_wall_type))
