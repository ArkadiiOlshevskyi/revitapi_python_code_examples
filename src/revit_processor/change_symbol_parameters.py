import re
import logging
import inspect

from Autodesk.Revit.DB import *

logger = logging.getLogger(__name__)


def get_default_window_symbol(document):
    """
    Retrieves the default window symbol from the given document.

    Args:
        document: The Revit document to search.

    Returns:
        The name of the default window symbol if found, otherwise None.
    """

    function_name = inspect.currentframe().f_code.co_name
    logging.info('Trying to get default window symbol in function: {}'.format(function_name))
    print('Trying to get default window symbol in function: {}'.format(function_name))

    try:
        all_preloaded_windows_symbols = FilteredElementCollector(document). \
            OfCategory(BuiltInCategory.OST_Windows). \
            WhereElementIsElementType().ToElements()

        pattern_default = re.compile(r'^window_default$', re.IGNORECASE)

        for preloaded_window_symbol in all_preloaded_windows_symbols:
            preloaded_symbol_name = preloaded_window_symbol.Name
            if pattern_default.match(preloaded_symbol_name):
                logging.info('Found default window symbol: {}'.format(preloaded_symbol_name))
                print('Found default window symbol: {}'.format(preloaded_symbol_name))
                return preloaded_window_symbol

        return None
    except Exception as e:
        logging.error('Error occurred while trying to get default window symbol: {}'.format(e))
        print('Error occurred while trying to get default window symbol: {}'.format(e))
        return None


def get_default_door_symbol(document):
    """
    Retrieves the default door symbol from the given document.

    Args:
        document: The Revit document to search.

    Returns:
        The default door symbol Element if found, otherwise None.
    """

    function_name = inspect.currentframe().f_code.co_name
    logging.info('Trying to get default door symbol in function: {}'.format(function_name))
    print('Trying to get default door symbol in function: {}'.format(function_name))

    try:
        all_preloaded_doors_symbols = FilteredElementCollector(document). \
            OfCategory(BuiltInCategory.OST_Doors). \
            WhereElementIsElementType().ToElements()

        pattern_default = re.compile(r'^door_default$', re.IGNORECASE)

        for preloaded_door_symbol in all_preloaded_doors_symbols:
            preloaded_symbol_name = preloaded_door_symbol.Name
            if pattern_default.match(preloaded_symbol_name):
                logging.info('Found default door symbol: {}'.format(preloaded_symbol_name))
                print('Found default door symbol: {}'.format(preloaded_symbol_name))
                return preloaded_door_symbol

        return None
    except Exception as e:
        logging.error('Error occurred while trying to get default door symbol: {}'.format(e))
        print('Error occurred while trying to get default door symbol: {}'.format(e))
        return None


def sort_only_windows_refid_symbols(document):
    """
    Retrieves a list of window symbols with the format 'window_XXX' from the given document.

    Args:
        document: The Revit document to search.

    Returns:
        A sorted list of window symbols with the format 'window_XXX'.
    """

    function_name = inspect.currentframe().f_code.co_name
    logging.info('Trying to get sorted list of window symbols in function: {}'.format(function_name))
    print('Trying to get sorted list of window symbols in function: {}'.format(function_name))

    try:
        all_preloaded_windows_symbols = FilteredElementCollector(document). \
            OfCategory(BuiltInCategory.OST_Windows). \
            WhereElementIsElementType().ToElements()

        sorted_window_symbols = []
        pattern_window_numbers = re.compile(r'^window_(\d+)$', re.IGNORECASE)

        for preloaded_window_symbol in all_preloaded_windows_symbols:
            preloaded_symbol_name = preloaded_window_symbol.Name
            match = pattern_window_numbers.match(preloaded_symbol_name)
            if match:
                sorted_window_symbols.append(preloaded_window_symbol)

        sorted_window_symbols.sort(key=lambda x: int(re.search(r'\d+', x.Name).group()))
        logging.info('Sorted window symbols: {}'.format(sorted_window_symbols))
        print('Sorted window symbols: {}'.format(sorted_window_symbols))
        return sorted_window_symbols

    except Exception as e:
        logging.error('Error occurred while trying to sort window symbols: {}'.format(e))
        print('Error occurred while trying to sort window symbols: {}'.format(e))
        return []


def sort_only_doors_refid_symbols(document):
    """
    Retrieves a list of doors symbols with the format 'door_XXX' from the given document.

    Args:
        document: The Revit document to search.

    Returns:
        A sorted list of door symbols with the format 'door_XXX'.
    """

    function_name = inspect.currentframe().f_code.co_name
    logging.info('Trying to get sorted list of doors symbols in function: {}'.format(function_name))
    print('Trying to get sorted list of doors symbols in function: {}'.format(function_name))

    try:
        all_preloaded_doors_symbols = FilteredElementCollector(document). \
            OfCategory(BuiltInCategory.OST_Doors). \
            WhereElementIsElementType().ToElements()

        sorted_door_symbols = []
        pattern_door_numbers = re.compile(r'^door_(\d+)$', re.IGNORECASE)

        for preloaded_door_symbol in all_preloaded_doors_symbols:
            preloaded_symbol_name = preloaded_door_symbol.Name
            match = pattern_door_numbers.match(preloaded_symbol_name)
            if match:
                sorted_door_symbols.append(preloaded_door_symbol)

        sorted_door_symbols.sort(key=lambda x: int(re.search(r'\d+', x.Name).group()))
        logging.info('Sorted door symbols: {}'.format(sorted_door_symbols))
        print('Sorted door symbols: {}'.format(sorted_door_symbols))
        return sorted_door_symbols

    except Exception as e:
        logging.error('Error occurred while trying to sort door symbols: {}'.format(e))
        print('Error occurred while trying to sort door symbols: {}'.format(e))
        return []


def changing_symbol(document,
                    ifc_model,
                    model_symbols,
                    default_model_symbol):
    """
    Change the symbol of IFC models (doors, windows) in Revit.

    :param document: Revit Document - Active or backend Revit document containing IFC models
    :param ifc_model: Revit element - Selection of visible model in 3D model
    :param model_symbols: list of Revit symbols - Preloaded window symbols in the Revit document
    :param default_model_symbol: Revit Symbol - Default symbol to use if no match is found

    :return: list of changed Revit objects with new or default symbols
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Trying to change IFC model Symbol -> {}'.format(function_name))
    print('Trying to change IFC model Symbol -> {}'.format(function_name))

    t = Transaction(document, "Changing Symbol")

    try:
        t.Start()

        ifc_model_symbol_name = ifc_model.Symbol.Name.lower()
        ifc_model_symbol_name_prefix = ifc_model_symbol_name.split()[0]

        symbol_found = False
        for symbol in model_symbols:
            symbol_name_str = symbol.Name
            if ifc_model_symbol_name_prefix == symbol_name_str:
                ifc_model.Symbol = symbol
                print('IFC Model -> SYMBOL CHANGED!')
                print('NEW SYMBOL -> {}!'.format(ifc_model.Symbol.Name))
                logging.info('IFC Model -> SYMBOL CHANGED! NEW SYMBOL -> {}!'.format(ifc_model.Symbol.Name))
                symbol_found = True
                break

        if not symbol_found:
            print('Symbol not found for {}!'.format(ifc_model_symbol_name_prefix))
            ifc_model.Symbol = default_model_symbol
            print('NEW SYMBOL -> {}!'.format(ifc_model.Symbol.Name))
            logging.warning('Symbol not found for {}. Default symbol used.'.format(ifc_model_symbol_name_prefix))
            logging.info('IFC Model -> SYMBOL CHANGED! NEW SYMBOL -> {}!'.format(ifc_model.Symbol.Name))

        t.Commit()
        print('Successfully changed Symbol in IFC model -> {}'.format(t.GetStatus()))
        logger.info('Successfully changed Symbol in IFC model -> {}'.format(t.GetStatus()))

        return ifc_model

    except Exception as e:
        print('Mapping IFC Windows or Roors from FML...failed: {}'.format(str(e)))
        logger.error('Mapping IFC Windows or Roors from FML...failed: {}'.format(str(e)))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            pass


def changing_parameters(document,
                        ifc_model,
                        width_parameter_value,
                        height_parameter_value):
    """
    Change the parameters of updated (revit Symbol is already changed) (doors, windows) IFC model in Revit.

    :param document: Revit Document - Active or backend Revit document containing IFC models
    :param ifc_model: Revit element - Selection of previously changed and visible model in 3D model
    :param width_parameter_value: Float - numeric value previously extracted from IFC model geometry
    :param height_parameter_value: Float - numeric value previously extracted from IFC model geometry

    :return: changed Revit object with new parameters like Height and Width
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Trying to change IFC model Parameters Height and Width -> {}'.format(function_name))
    print('Trying to change IFC model Parameters Height and Width -> {}'.format(function_name))

    t = Transaction(document, "Changing Parameters Height and Width")

    try:
        t.Start()

        print('APPLYING NEW PARAMETERS...')  # works - use it ON OTHER SCRIPT AND APPLY TRANSFERRED PARAMS
        width_parameter = ifc_model.LookupParameter("Width")
        if width_parameter:
            width_value = width_parameter.AsValueString()
            print("Width LOOKUP parameter of {} is {}".format(ifc_model.Name, width_value))
        else:
            print("Width parameter not found for {}".format(ifc_model.Name))

        height_parameter = ifc_model.LookupParameter("Height")
        if height_parameter:
            width_value = height_parameter.AsValueString()
            print("Height LOOKUP parameter of {} is {}".format(ifc_model.Name, width_value))
        else:
            print("Height parameter not found for {}".format(ifc_model.Name))

        ifc_model.LookupParameter('Width').Set(width_parameter_value)
        ifc_model.LookupParameter('Height').Set(height_parameter_value)

        print('NEW PARAMETERS WAS APPLIED!')

        t.Commit()
        return ifc_model

    except Exception as e:
        print('APPLYING NEW PARAMETERS...failed: {}'.format(str(e)))
        logger.error('APPLYING NEW PARAMETERS...failed: {}'.format(str(e)))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            pass


############################################################### Example usage:  WORKS 17-04-2024
# print('###### TEST CASE' + '#' * 80)
#
# ifc_document = __revit__.ActiveUIDocument.Document
# doors_symbols = sort_only_doors_refid_symbols(ifc_document)
# for door_object in doors_symbols:
#     print(type(door_object))
#     print('Door symbol Name -> {}'.format(door_object.Name))
#
# default_symbol_door = get_default_door_symbol(ifc_document)
# print(type(doors_symbols))
# print("Default Symbol ->", default_symbol_door)
#
# default_symbol_window = get_default_window_symbol(ifc_document)
# print("Default Symbol ->", default_symbol_window)
# print(type(default_symbol_window))
# print(default_symbol_window.Name)
#
# window_symbols = sort_only_windows_refid_symbols(ifc_document)
# for window_object in window_symbols:
#     print(type(window_object))
#     print(window_object.Name)
#
# print('###### SELECTING and MAPPING IFC WINDOWS' + '#' * 20)
# selection_all_ifc_windows = FilteredElementCollector(ifc_document). \
#     OfCategory(BuiltInCategory.OST_Windows). \
#     WhereElementIsNotElementType().ToElements()
#
# for window in selection_all_ifc_windows:
#     # get the parameters from windows geometry
#     width_param_value = 2
#     height_param_value = 2
#
#     window_with_new_symbol = changing_symbol(ifc_document, window, window_symbols, default_symbol_window)
#     window_with_new_parameters = changing_parameters(ifc_document, window, width_param_value, height_param_value)
