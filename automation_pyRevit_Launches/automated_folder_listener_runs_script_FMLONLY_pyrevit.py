import datetime
import os
import sys
import time
import logging
import inspect
import subprocess
from wescan_utilities import timer
import wescan_paths
import wescan_file_extensions

sys.path.append(r'C:\Program Files\IronPython 3.4\Lib\site-packages')
sys.path.append(r'C:\Users\3duni\Desktop\Arkadii\2_projects_tasks\8_revit_api_converter_3\converter')
sys.path.append(r'C:\Users\3duni\Application Data\pyCharmEnvironments\RevitAPI24')

path = wescan_paths.INPUT_PATH
input_path = wescan_paths.INPUT_PATH  # for now using tes_input folder
# output_path = wescan_paths.OUTPUT_PATH
init_revit_file = wescan_paths.INIT_REVIT__FILE  # for now using init_project_revit.rvt
refid_and_model_names = wescan_paths.MODELS_FML_REFID_PATH


@timer
def open_powershell_shell(file_path):
    """
    Function to open PowerShell shell and execute pyRevit command.
    ATTENTION -> THIS SCRIPT WILL WORK EVERYTIME WITH SINGLE FML FILE,
    NEW FILE IN DIRECTORY FOUND == NEW TASK FOR PYREVIT
    In pyRevit command we run wescan_main.py script (model converter).
    TODO: Add to logic many scenarios with filenames, missing file... etc.
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Running function: %s {}'.format(function_name))
    try:
        powershell_process = subprocess.Popen(["powershell.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
        # Add { --debug} to get debug print
        # pyrevit_version_command = 'pyrevit run "C:\\Program Files\\IronPython 3.4\\Lib\\site-packages\\wescan_fml_parse_only_1.py" "C:\\Users\\3duni\\Desktop\\Arkadii\\2_projects_tasks\\8_revit_api_converter_3\\input\\revit_project.rvt" --debug'
        pyrevit_version_command = 'pyrevit run "C:\\Program Files\\IronPython 3.4\\Lib\\site-packages\\wescan_main_IFC_to_DWG_dwi.py" "C:\\Users\\3duni\\Desktop\\Arkadii\\2_projects_tasks\\8_revit_api_converter_3\\input\\revit_project.rvt" --debug'
        output, _ = powershell_process.communicate(pyrevit_version_command.encode('utf-8'))

        print(output.decode('utf-8'))
        logging.info('PowerShell shell opened and pyRevit command executed.')
    except Exception as e:
        print('Error opening PowerShell shell or executing command:', e)
        logging.error('Error opening PowerShell shell or executing command: %s', e)


def monitor_folder(folder_path):
    """
    Script monitoring a folder(input).
    -> If we put new project files in the folder with .fml or .ifc extensions, it will process them
    by executing automation pyRevit script.
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Running function: {}'.format(function_name))

    try:
        files_before = set(os.listdir(folder_path))
        fml_loaded = False
        fml_filename = None

        while True:
            time.sleep(1)
            files_after = set(os.listdir(folder_path))
            new_files = files_after - files_before

            for filename in new_files:
                if filename.endswith('.fml'):
                    fml_loaded = True
                    fml_filename = filename

                    print('New FML file detected: {}'.format(filename))
                    logging.info('New FML file detected: {}'.format(filename))

                    print("Starting automation for FML file...")
                    logging.info("Starting automation for FML file...")
                    open_powershell_shell(os.path.join(folder_path, filename))  # Open PowerShell shell and execute pyRevit command
                    fml_loaded = False  # Reset FML loaded flag

            files_before = files_after

    except Exception as e:
        logging.error(e)
        return None


if __name__ == '__main__':
    print('Folder listener runs...')
    print('Waiting for FML files to convert...')
    monitor_folder(input_path)
    # WORKS 27-3-2024
