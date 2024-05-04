import sys
import logging
import inspect

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


def open_ifc_file(document, input_path, project_name):
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
        ifc_document = app.OpenIFCDocument(input_path + "\\" + project_name + '.ifc')
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
