import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
import inspect
import logging
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementParameterFilter, ParameterValueProvider, \
    FilterStringBeginsWith, FilterStringRule, BuiltInParameter, ElementId

logger = logging.getLogger(__name__)


def get_selected_doors(document, family_name_prefix):
    try:
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Selecting doors with name prefix -> {}'.format(family_name_prefix))
        print('Selecting doors with name prefix -> {}'.format(family_name_prefix))

        # Define filter for door symbols with specific name prefix
        selected_ifc_doors = FilteredElementCollector(document).OfCategory(
            BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
        all_ifc_doors = list(selected_ifc_doors)

        return all_ifc_doors

    except Exception as e:
        logger.error("Error occurred: {}".format(e))
        print("Error occurred: {}".format(e))
        return None


def get_selected_windows(document, family_name_prefix):
    try:
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Selecting windows with name prefix -> {}'.format(family_name_prefix))
        print('Selecting windows with name prefix -> {}'.format(family_name_prefix))

        selected_ifc_windows = FilteredElementCollector(document).OfCategory(
            BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
        all_ifc_windows = list(selected_ifc_windows)
        print('All Selected windows : -> {}'.format(all_ifc_windows))
        # we can select windows only with specific name construction
        # but try first to reload family_symbol and 2nd way - select host wall and place a window in empty IFC model by parsing FML for data

        return all_ifc_windows

    except Exception as e:
        logger.error("Error occurred: {}".format(e))
        print("Error occurred: {}".format(e))
        return None

# ####################### TEST CASE ##################################### Example usage:
# ifc_document = __revit__.ActiveUIDocument.Document
# ifc_window_name_prefix = "Window_"  # Update this prefix according to your naming convention
# ifc_doors_name_prefix = "Door_"  # Update this prefix according to your naming convention
#
# selected_ifc_windows = get_selected_windows(ifc_document, ifc_window_name_prefix)


## Show you selection name
# # Print selected_level window names
# if selected_ifc_windows:
#     print("Selected Windows:")
#     for window in selected_ifc_windows:
#         print(window.Name)
# else:
#     print("No windows selected_level.")
#
#
# selected_ifc_doors = get_selected_doors(ifc_document, ifc_doors_name_prefix)
#
# # Print selected_level window names
# if selected_ifc_doors:
#     print("Selected Doors:")
#     for door in selected_ifc_doors:
#         print(door.Name)
# else:
#     print("No Doors selected_level.")
