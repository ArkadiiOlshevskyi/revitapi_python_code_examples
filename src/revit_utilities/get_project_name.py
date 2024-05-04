import os
import logging
import inspect

logger = logging.getLogger(__name__)


def get_project_name(path, extensions):
    """
    Get project name from the given path with file name and JSON extension.
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Running function: {}'.format(function_name))

    try:
        file_names = []
        for file_name in os.listdir(path):
            if file_name.endswith(tuple(extensions)):
                file_name = os.path.splitext(file_name)[0]
                file_names.append(file_name)

        if file_names:
            return file_names[0]  # Returning the first file name found
        else:
            logger.warning("No files with given extensions found in the path.")
            return None

    except Exception as e:
        logger.error('Error: {}, \n in Function: {}'.format(e, function_name))
        return None
