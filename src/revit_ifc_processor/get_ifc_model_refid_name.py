import logging
import inspect
import re

logger = logging.getLogger(__name__)


def ifc_model_refid_name(model_name, prefix):
    """
    Function takes ifc_model name from
    pre-selected_level revit list with IFC models
    For example name like "Window_218 1526 1526"
    Means that "Window_218" is revit models name for
    loading generic revit model
    Input:
    -> models_name - name gotten from IFC model.Name
    -> prefix - hardcode search prefix for all IFC models
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Getting model REFID -> {}'.format(function_name))
    print('Getting model REFID -> {}'.format(function_name))

    try:
        if model_name.startswith(prefix):
            # Split the element name based on the first space
            parts = model_name[len(prefix):].split(' ', 1)

            if len(parts) > 0:
                # Extract the part before the first space
                extracted_name = parts[0]
                print('Refid for loading revit model -> {}'.format(extracted_name))
                return extracted_name
            else:
                logger.error("No space found after prefix in the element name.")
                print("No space found after prefix in the element name.")
                return None
        else:
            logger.error("Prefix not found in the element name.")
            print("Prefix not found in the element name.")
            return None
    except Exception as e:
        logger.error("An error occurred in function {}: {}".format(inspect.stack()[0][3], e))
        print("An error occurred in function {}: {}".format(inspect.stack()[0][3], e))
        return None


def extract_type_refid(input_string):
    """
    Used for updated IFC version from 12-04-2024
    with died walls, windows and doors
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Trying to get ifc model name -> {}'.format(function_name))
    print('Trying to get ifc model name -> {}'.format(function_name))

    try:
        # Regular expression pattern to match the name part
        pattern = r'^([A-Za-z_]+_\d+)'

        # Search for the pattern in the input string
        match = re.search(pattern, input_string)

        # If a match is found, return the matched name part
        if match:
            selected_name = match.group(1)
            selected_name_lower = selected_name.lower()
            print('Selected name is ->', selected_name_lower)
            return selected_name_lower
        else:
            return None
    except Exception as e:
        logging.error("An error occurred while extracting name part: %s", e)
        print("An error occurred while extracting name part:", e)
        return None

# ############## TEST CASE 1 ######################################
# import wescan_paths  # Remote after testing
#
# ifc_document = __revit__.ActiveUIDocument.Document
# element_name = "Door_233222 1526 1526"
# prefix = "Door_"
# extracted_name = ifc_model_refid_name(element_name, prefix)

# ############## TEST CASE 2 ######################################
# input_string = "Window_218 1734"      # Usual IFC window door name Window_218
# name_part = extract_type_refid(input_string)
# print(name_part)  # Output: Window_218
