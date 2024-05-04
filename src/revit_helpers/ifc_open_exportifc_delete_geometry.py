import sys
import logging
import inspect

######### DELETE WHEN IT WAS TESTED ##################
## TEST case -> run from CLI pyrevit run...--debug
from pyrevit import HOST_APP  # for pyrevit script to open active ifc_document

init_revit_file = r"C:\Program Files\IronPython 3.4\Lib\site-packages\wescan_revit_helpers\init_project_revit.rvt"
model = init_revit_file
uidoc = HOST_APP.uiapp.OpenAndActivateDocument(model)
doc_pyrevit_init = uidoc.Document
print(doc_pyrevit_init)
print(doc_pyrevit_init.Title)
######### DELETE WHEN IT WAS TESTED ##################

logger = logging.getLogger(__name__)
sys.path.append('C:\Program Files\IronPython 3.4\Lib\site-packages')

import clr

clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from System.Collections.Generic import List


import Autodesk.Revit.DB as DB  # used for List in delete function
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.IFC import *
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI.Events import DisplayingOptionsDialogEventArgs

from Autodesk.Revit.UI import TaskDialog, TaskDialogResult, TaskDialogCommandLinkId, TaskDialogCommonButtons
from Autodesk.Revit.DB import FailureProcessingResult, IFailuresPreprocessor
from Autodesk.Revit.DB import Transaction, FailureHandlingOptions


class WarningSwallower(IFailuresPreprocessor):
    """
    Class to handle dialog box when opening IFC file (that was generated from fml)
    This solution WORKS on backend
    But NOT WORKS while running in RevitPythonShell!
    So you can apply this WarningSwallower for script running by pyRevit in CLI
    """

    def PreprocessFailures(self, failuresAccessor):
        # get list of failure messages
        failures = failuresAccessor.GetFailureMessages()
        logging.info('WarningSwallower working...')

        # Iterate through each failure message
        for failureMessageAccessor in failures:
            # Get failure severity
            failureSeverity = failureMessageAccessor.GetSeverity()

            # Check if failure is a warning
            if failureSeverity == FailureSeverity.Warning:
                print('Failure Severity -> {}'.format(failureSeverity))
                failuresAccessor.DeleteWarning(failureMessageAccessor)
            else:
                return FailureProcessingResult.Continue

        # Continue processing other failures
        return FailureProcessingResult.Continue


class TransactionHandler(object):
    """
    Class to implement WarningSwallower to Revit Transaction
    Later we wrapp our IFC open transaction in this staticmethod
    """

    @staticmethod
    def SetWarningSkipper(transaction):
        logging.info('WarningSwallower attaching options to Revit Transaction')
        fail_options = transaction.GetFailureHandlingOptions()
        fail_options.SetFailuresPreprocessor(WarningSwallower())
        transaction.SetFailureHandlingOptions(fail_options)


def open_ifc_file(document, input_path, name_file):
    """
    Function to open IFC file in active ifc_document inside Revit
    Then we have click OK on the dialog box
    This function MUST RETURN ifc_document that contains IFC geometry
    Input:
    ifc_document -> usual 'ifc_document' value like ifc_document that used in RevitApi
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Trying to open IFC from fml: {}'.format(function_name))

    try:
        app = document.Application
        logging.info('Wrapping IFC open transaction on warning skipper')
        t = Transaction(document, 'Opening IFC with Warnings...')
        TransactionHandler.SetWarningSkipper(t)

        t.Start()
        ifc_document = app.OpenIFCDocument(input_path + name_file + '.ifc')
        t.Commit()

        print('Opening IFC with Warning Done -> {}'.format(t.GetStatus()))
        logging.info('Opening IFC with Warning Done -> {}'.format(t.GetStatus()))
        # We are returning ifc_document with IFC geometry inside for future use in mapping etc.
        return ifc_document

    except Exception as e:
        logging.error('Error while opening IFC from fml -> {}'.format(e))
        print('Error while opening IFC from fml -> {}'.format(e))
        if t is not None and t.HasStarted():
            t.RollBack()
            logging.info('IFC Opening Transaction Rolled Back... ->{}'.format(t.GetStatus()))
            print('IFC Opening Transaction Rolled Back... ->{}'.format(t.GetStatus()))
            return None


## TEST case -> revit python shell copy paste -> WORKS
## TEST case -> automation CLI pyrevit launch -> WORKS
#
doc = __revit__.ActiveUIDocument.Document  # using opened empty init pyrevit file
name_file = r"Admiraalsgroet4_bundel_0"  # using some IFC from fml for test (in main this name we get from project_name function)

input_path = r"C:\\Users\\3duni\\Desktop\\Arkadii\\2_projects_tasks\\8_revit_api_converter_3\\input\\"
ifc = open_ifc_file(doc, input_path, name_file)  # return IFC ifc_document


##### Test option to delete IFC windows, so we can sure that actions in opened IFC can be performe

def delete_element_or_list_by_id(document):
    """
    Function delete IFC windows (boxes) from
    loaded IFC model (we get in by input ifc ifc_document to this function)
    import Autodesk.Revit.DB as DB  # used for List in delete function
    """
    t = Transaction(document, "Delete element by ID")
    collector_filter = FilteredElementCollector(document).OfCategory(
        BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
    element_ids_to_delete = [model.Id for model in collector_filter]
    element_ids_to_delete_collection = List[DB.ElementId](element_ids_to_delete)
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Delete IFC windows from loaded IFC model')

    try:
        t.Start()
        logging.info('Trying to delete IFC windows from model...')
        print('Trying to delete IFC windows from model...')

        document.Delete(
            element_ids_to_delete_collection)  # works! Deletes all OST_Walls|OST_Windows|OST_Doors in the project

        t.Commit()
        print('IFC windows was deleted successfully -> {}'.format(t.GetStatus()))
        logging.info('IFC windows was deleted successfully -> {}'.format(t.GetStatus()))

    except Exception as e:
        print('Deleting IFC windows ...failed: {}'.format(str(e)))
        logging.error('Deleting IFC windows ...failed: {}'.format(t.GetStatus()))
        if t is not None and t.HasStarted():
            t.RollBack()
            logging.info('{}'.format(t.GetStatus()))
            print('{}'.format(t.GetStatus()))
            pass


# ----------------------------------------------------------------------
delete_element_or_list_by_id(ifc)  # IFCWindows deleting
print('Script executed' + "_" * 70 + "\n")
# ----------------------------------------------------------------------


print('Trying to save in IFC format')
path = r"C:\Users\3duni\Desktop\Arkadii\2_projects_tasks\8_revit_api_converter_3\test_output"
name = 'test_IFC file 777'
t = Transaction(ifc, "Export to IFC from Revit")

try:
    print('Trying to Exporting IFC...')
    logging.info('Trying to Exporting IFC...')

    t.Start()

    options = IFCExportOptions()
    ifc.Export(path, name, options)

    t.Commit()
    print('DONE Exporting IFC...')
    logging.info('DONE Exporting IFC...')

except Exception as e:
    print('Exporting IFC ...failed: {}'.format(str(e)))
    logging.error('Exporting IFC ...failed: {}'.format(t.GetStatus()))
    if t is not None and t.HasStarted():
        t.RollBack()
        logging.info('{}'.format(t.GetStatus()))
        print('{}'.format(t.GetStatus()))
        pass

print('Exported ifc_document in IFC format Successfully -> {}'.format(t.GetStatus()))
logging.info('Exported ifc_document in IFC format Successfully -> {}'.format(t.GetStatus()))

print('Done' + '#' * 50)
