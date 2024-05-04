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
    logging.info('Running function: %s' % function_name)
    print('Running function: %s' % function_name)
    try:

        powershell_process = subprocess.Popen(["powershell.exe"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
        # Add { --debug} to get debug print
        # pyrevit_version_command = 'pyrevit run "C:\\Program Files\\IronPython 3.4\\Lib\\site-packages\\wescan_main_IFC_to_DWG.py" "C:\\Users\\3duni\\Desktop\\Arkadii\\2_projects_tasks\\8_revit_api_converter_3\\input\\init_project_revit.rvt" --debug'
        pyrevit_version_command = 'pyrevit run "C:\\Program Files\\IronPython 3.4\\Lib\\site-packages\\wescan_main_IFC_to_DWG_2.py" "C:\\Users\\3duni\\Desktop\\Arkadii\\2_projects_tasks\\8_revit_api_converter_3\\input\\init_project_revit.rvt" --debug'
        output, _ = powershell_process.communicate(pyrevit_version_command.encode('utf-8'))

        print(output.decode('utf-8'))
        logging.info('PowerShell shell opened and pyRevit command executed.')
        print('PowerShell shell opened and pyRevit command executed.')
    except Exception as e:
        logging.error('Error opening PowerShell shell or executing command: %s', e)
        print('Error opening PowerShell shell or executing command:', e)


def monitor_folder(folder_path):
    """
    Script monitoring a folder(input).
    -> If we put new project files in the folder with .ifc extensions, it will process them
    by executing automation pyRevit script.
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Running function: {}'.format(function_name))
    print('Running function: {}'.format(function_name))

    try:
        files_before = set(os.listdir(folder_path))
        ifc_loaded = False
        ifc_filename = None

        while True:
            time.sleep(1)
            files_after = set(os.listdir(folder_path))
            new_files = files_after - files_before

            for filename in new_files:
                if filename.endswith('.ifc'):
                    ifc_loaded = True
                    ifc_filename = filename
                    print('New IFC file detected: {}'.format(filename))
                    logging.info('New IFC file detected: {}'.format(filename))

            files_before = files_after

            if ifc_loaded:
                print("IFC file loaded, starting automation...")
                logging.info("IFC file loaded, starting automation...")
                # Start automation script here
                open_powershell_shell()  # Open PowerShell shell and execute pyRevit command
                ifc_loaded = False  # Reset the flag after processing
            else:
                print("Waiting for IFC file...")
                logging.info("Waiting for IFC file...")

    except Exception as e:
        logging.error(e)
        return None


if __name__ == '__main__':
    print('Folder listener runs...')
    print('Waiting for project files to convert...')
    monitor_folder(input_path)
