import inspect
import logging
import clr  # Imports to works with Revit API .NET implementation via python
from System.Collections.Generic import List
from collections import OrderedDict
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.IFC import *
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, View3D, DWGExportOptions, ElementId
from Autodesk.Revit.DB import *

import wescan_paths

clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
clr.AddReference("System")

logger = logging.getLogger(__name__)


input_path = wescan_paths.INPUT_PATH  # for now using tes_input folder
output_path = wescan_paths.OUTPUT_PATH
project_name = "MollukenStraat_66"


class RoomWarningSwallower(IFailuresPreprocessor):
    def FailureHandler(self, failuresAccessor):
        fail_list = List[FailureMessageAccessor]()
        fail_acc_list = failuresAccessor.GetFailureMessages().GetEnumerator()
        for failure in fail_acc_list:
            failure_severity = failure.GetSeverity()
            if (failure_severity == FailureSeverty.Warning):
                failuresAccessor.DeleteWarning(failure)
            else:
                failuresAccessor.ResolveFailure(failure)
                return FailureProcessingResult.ProceedWithCommit
        return FailureProcessingResult.Continue


def export_project_to_dwg(document, output_folder_path, name):
    """
    Export file in revit to DWG
    It's better to export dwg in 2007 or 2013 format
    TODO: set dwg format to 2007 year
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Function {} started....'.format(function_name))

    try:
        logger.info('Exporting ifc_document to DWG vers.2007....')
        print('Exporting ifc_document to DWG vers.2007....')

        t = Transaction(document, "Exporting ifc_document to DWG vers.2007....")
        t.Start()

        options = t.GetFailureHandlingOptions()
        options.SetFailuresPreprocessor(RoomWarningSwallower())
        t.SetFailureHandlingOptions(options)

        views = list(FilteredElementCollector(document).OfClass(View3D))[2]
        viewsWrap = []
        viewsWrap.Add(views.Id)
        collection = List[ElementId](viewsWrap)

        options = DWGExportOptions()
        options.FileVersion = ACADVersion.R2007
        # os.makedirs(output_folder_path, exist_ok=True)
        out_name_dwg = name.split(".")[0] + ".dwg"
        document.Export(output_folder_path, out_name_dwg, collection, options)

        t.Commit()
        # print(t.GetStatus())
        logger.info('Document exported to DWG vers.2007 successfully {} \n {}'.format(out_name_dwg, t.GetStatus()))
        # ifc_document.Close()       # add it if you want to close the ifc_document after exporting
    except Exception as e:
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            logger.error('Error exporting ifc_document to DWG vers.2007: {}'.format(e))
            print('Error exporting ifc_document to DWG:', e)

