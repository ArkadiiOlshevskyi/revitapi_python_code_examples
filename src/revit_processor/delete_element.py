import logging
import inspect
from Autodesk.Revit.DB import *

import clr

clr.AddReference('RevitAPI')        # Add reference to RevitAPI
clr.AddReference('RevitServices')   # Add reference to RevitServices for DocumentManager
clr.AddReference('RevitNodes')      # Add reference to RevitNodes for Document

logger = logging.getLogger(__name__)


def delete_element(document, element_id):   # WORKING tested 19-3-2024
    """
    Deleting element with Transaction
    Input:
    -> active revit ifc_document of ifc ifc_document on backend
    -> elementID to delete like 123123123 (access by method from selected_level element)
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Deleting Element gy ID -> {}'.format(function_name))
    t = Transaction(document, 'Deleting Element')

    try:
        t.Start()
        document.Delete(element_id)
        t.Commit()

        logger.info('Element was Deleted Successfully -> {}'.format(t.GetStatus()))
        print('Element was Deleted Successfully -> {}'.format(t.GetStatus()))

    except Exception as e:
        logger.error('Error while Deleting element dy ID -> {}'.format(e))
        print('Error while Deleting element dy ID -> {}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            print(t.GetStatus())
