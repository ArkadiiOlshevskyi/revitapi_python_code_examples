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
def open_powershell_shell():
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
        pyrevit_version_command = 'pyrevit run "C:\\Program Files\\IronPython 3.4\\Lib\\site-packages\\wescan_main_IFC_to_DWG_2.py" "C:\\Users\\3duni\\Desktop\\Arkadii\\2_projects_tasks\\8_revit_api_converter_3\\input\\init_project_revit.rvt" --debug'
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
        ifc_loaded = False
        fml_filename = None
        ifc_filename = None

        while True:
            time.sleep(1)
            files_after = set(os.listdir(folder_path))
            new_files = files_after - files_before

            for filename in new_files:
                if filename.endswith('.ifc'):
                    ifc_loaded = True
                    ifc_filename = filename
                elif filename.endswith('.fml'):
                    fml_loaded = True
                    fml_filename = filename

                print('New file detected: {}'.format(filename))
                logging.info('New file detected: {}'.format(filename))

            files_before = files_after

            if ifc_loaded and fml_loaded:
                if ifc_filename[:-4] == fml_filename[:-4]:  # Check if filenames match without extensions
                    print("Both IFC and FML files are loaded with matching names. Starting automation...")
                    logging.info("Both IFC and FML files are loaded with matching names. Starting automation...")
                    # Start automation script here
                    ifc_loaded = False
                    fml_loaded = False
                    open_powershell_shell()  # Open PowerShell shell and execute pyRevit command
                    # activate_revit_document()
                else:
                    print("IFC and FML files loaded, but their names don't match. Automation aborted.")
                    logging.warning("IFC and FML files loaded, but their names don't match. Automation aborted.")
                    # Reset variables
                    ifc_loaded = False
                    fml_loaded = False

            elif ifc_loaded:
                print("IFC file loaded, waiting for FML file to start name check.")
                logging.info("IFC file loaded, waiting for FML file to start name check.")
            elif fml_loaded:
                print("FML file loaded, waiting for IFC file to start name check.")
                logging.info("FML file loaded, waiting for IFC file to start name check.")

    except Exception as e:
        logging.error(e)
        return None


if __name__ == '__main__':
    print('Folder listener runs...')
    print('Waiting for project files to convert...')
    monitor_folder(input_path)
