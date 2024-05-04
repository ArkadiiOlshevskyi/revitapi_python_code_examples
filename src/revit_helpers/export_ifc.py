import logging
import inspect

from Autodesk.Revit.ApplicationServices import *
from Autodesk.Revit.DB.IFC import *
from Autodesk.Revit.DB import Document, IFCExportOptions, Transaction

logger = logging.getLogger(__name__)


def export_to_IFC(ifc_document, output_folder, file_name):
    """
    Exporting project (revit active ifc_document) in IFC format + options
    !!!!Attention - IFC file opened on backend is now showing in Revit viewport!!!
    To test any options over IFC run your scripts in Revit python Shell
    To Export from Revit opened IFC(from fml) this function MUST receive
    on input ifc_document(ifc) that opened on backend(ifc).
    """
    function_name = inspect.currentframe().f_code.co_name
    logging.info('Saving in IFC by -> {}'.format(function_name))
    t = Transaction(ifc_document, "Export to IFC from Revit")

    try:
        print('Trying to Exporting IFC...')
        logging.info('Trying to Exporting IFC...')

        t.Start()

        options = IFCExportOptions()
        ifc_document.Export(output_folder, file_name, options)

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
