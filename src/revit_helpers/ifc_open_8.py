import sys
import logging
import inspect

# inputted pyrevit init
from pyrevit import HOST_APP  # for pyrevit script to open active ifc_document

# WORKS - opens IFC and remove windows and save revit IFC

init_revit_file = r"C:\Program Files\IronPython 3.4\Lib\site-packages\wescan_revit_helpers\init_project_revit.rvt"
model = init_revit_file
uidoc = HOST_APP.uiapp.OpenAndActivateDocument(model)
doc_pyrevit_init = uidoc.Document
print(doc_pyrevit_init)
print(doc_pyrevit_init.Title)

logger = logging.getLogger(__name__)

sys.path.append('C:\Program Files\IronPython 3.4\Lib\site-packages')

import clr
clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")
from System.Collections.Generic import List

import Autodesk.Revit.DB as DB
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.IFC import *
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI.Events import DisplayingOptionsDialogEventArgs

from Autodesk.Revit.UI import TaskDialog, TaskDialogResult, TaskDialogCommandLinkId, TaskDialogCommonButtons
from Autodesk.Revit.DB import FailureProcessingResult, IFailuresPreprocessor
from Autodesk.Revit.DB import Transaction, FailureHandlingOptions


def export_to_IFC(output_folder, file_name):
    """
    Saving project(revit active ifc_document) in IFC format + options
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Saving in IFC by -> {}'.format(function_name))
    doc = __revit__.ActiveUIDocument.Document  # type: Document #can be problems here with open ifc ifc_document
    t = Transaction(doc, 'Exporting to IFC ifc_document')

    try:
        logging.info('Trying to save in IFC format')
        print('Trying to save in IFC format')
        t.Start()

        options = IFCExportOptions()
        doc.Export(output_folder, file_name, options)

        t.Commit()
        logging.info('Exported ifc_document in IFC format Successfully -> {}'.format(t.GetStatus()))
        print('Exported ifc_document in IFC format Successfully -> {}'.format(t.GetStatus()))

    except Exception as e:
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            logger.error('Error exporting ifc_document to IFC: {}'.format(e))
            print('Error exporting ifc_document to IFC:', e)


class WarningSkipper(IFailuresPreprocessor):
    def PreprocessFailures(self, failuresAccessor):
        # get list of failure messages
        failures = failuresAccessor.GetFailureMessages()

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
    @staticmethod
    def SetWarningSkipper(transaction):
        fail_options = transaction.GetFailureHandlingOptions()
        fail_options.SetFailuresPreprocessor(WarningSkipper())
        transaction.SetFailureHandlingOptions(fail_options)


doc = __revit__.ActiveUIDocument.Document
app = doc.Application

#########################
logging.info('Wrapping transaction on warning skipper')
t = Transaction(doc, 'Opening IFC with Warnings...')
TransactionHandler.SetWarningSkipper(t)
t.Start()

input_path = r"C:\\Users\\3duni\\Desktop\\Arkadii\\2_projects_tasks\\8_revit_api_converter_3\\input\\"
# project_name = r"MollukenStraat_66" # USED THIS FILE IN PREV WORK VERSION
name_file = r"Admiraalsgroet4_bundel_0"
dd = app.OpenIFCDocument(input_path + name_file + '.ifc')

t.Commit()
print('Opening IFC with Warning Done -> {}'.format(t.GetStatus()))
logging.info('Opening IFC with Warning Done -> {}'.format(t.GetStatus()))
########################


# Deleting windows if IFC
def delete_element_or_list_by_id(document):
    t = Transaction(document, "Delete element by ID")
    collector_filter = FilteredElementCollector(document).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElements()
    element_ids_to_delete = [model.Id for model in collector_filter]
    element_ids_to_delete_collection = List[DB.ElementId](element_ids_to_delete)


    try:
        t.Start()
        print('Deleting NEW started...!')
        document.Delete(element_ids_to_delete_collection)        # works! Deletes all OST_Walls|OST_Windows|OST_Doors in the project
        t.Commit()
        print('Deleting NEW finished...!' + '_' * 100)
    except Exception as e:
        print('Deleting elements...failed: {}'.format(str(e)))
        if t is not None and t.HasStarted():
            t.RollBack()
            pass
# ----------------------------------------------------------------------

delete_element_or_list_by_id(dd)  # Windows deleting
print('Script executed' + "_" * 70 + "\n")



########################
print('Trying to save IFC from revit')
logging.info('Trying to save IFC from revit')
path = r"C:\Users\3duni\Desktop\Arkadii\2_projects_tasks\8_revit_api_converter_3\test_output"
name = 'test_IFC file 777'
t = Transaction(dd, 'Exporting to IFC ifc_document')


print('Trying to save in IFC format')
t.Start()

options = IFCExportOptions()
dd.Export(path, name, options)

t.Commit()

print('Exported ifc_document in IFC format Successfully -> {}'.format(t.GetStatus()))
logging.info('Exported ifc_document in IFC format Successfully -> {}'.format(t.GetStatus()))

print('Done')
