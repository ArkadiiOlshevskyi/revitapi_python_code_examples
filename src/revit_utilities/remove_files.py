import os
import logging
import inspect

logger = logging.getLogger(__name__)


def remove_files(path, name, extensions):
    """
    Delete files in the specified directory with the specified extensions.
    Use Constant REMOVE_EXTENSIONS
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Deleting files from settled directory -> %s' % function_name)

    # Convert name to a list if it's not already one
    if type(name) is not list:
        name = [name]

    # Iterate over each file in the directory
    for file_name in os.listdir(path):
        # Check if the file matches any of the provided names and extensions
        for n in name:
            for ext in extensions:
                if file_name.startswith(n) and file_name.endswith(ext):
                    # Construct the full file path
                    file_path = os.path.join(path, file_name)
                    try:
                        # Attempt to remove the file
                        os.remove(file_path)
                        logging.info('Deleted file: %s' % file_path)
                    except Exception as e:
                        # Log any errors that occur during file removal
                        logging.error('Error deleting file %s: %s' % (file_path, e))
