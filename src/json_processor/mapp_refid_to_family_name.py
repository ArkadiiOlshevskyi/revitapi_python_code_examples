import logging
import inspect

logger = logging.getLogger(__name__)


def mapp_refid_to_name(data, target_refid):
    """
    Utility function that finds REFID (FML model ID) in data dictionary
    and matches it with FamilySymbol name (needed for NewFamilyInstance creation inside Revit).
    :param data: Dictionary containing REFID to name mappings.
    :param target_refid: The REFID to be mapped to a name.
    :return: The corresponding Revit family_symbol name, or None if not found.
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Trying to map refid to name in {}'.format(function_name))
    try:
        if target_refid in data:
            mapped_name = data[target_refid]
            logger.info('Mapped name is: {}'.format(data[target_refid]))
            return mapped_name
        else:
            logger.warning('No name found for REFID: {}'.format(target_refid))
            return None
    except Exception as e:
        logger.error('Error : {} \n in Function: {}'.format(e, function_name))
        print('Error: {} \n in Function: {}'.format(e, function_name))
        return None
