import os
import sys
import inspect
import logging

sys.path.append('C:\Program Files\IronPython 3.4\Lib\site-packages')

import clr

clr.AddReference('RevitAPI')  # Add reference to RevitAPI
clr.AddReference('RevitServices')  # Add reference to RevitServices for DocumentManager
clr.AddReference('RevitNodes')  # Add reference to RevitNodes for Document

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import FamilySymbol
from Autodesk.Revit.DB import Document
from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import Document, FilteredElementCollector, ElementId

logger = logging.getLogger(__name__)

# TODO -> add check if modelSymbol is existing is revit already -> use id don't load it


def load_family_symbol(document, symbol_name, default_model_name, path):  # Works Tested
    """
    Loads SINGLE model to Revit ifc_document according REFID on input, returns RevitFamilySYMBOL
    Used for iterating over Json parsing Items position
    That is used on next stage of revit model creation
    as reference what model revit need

    !!! ATTENTION !!! -> This function works only inside or wrapped in revit Transaction

    input:
    -> ifc_document - usually ifc_document, but it must be the ifc_document that you want a make record IN
    -> symbol_name - symbol name to be loaded
    -> path - folder, storage of revit models with REFID names
    -> default_model_name - usually we have Default model it revit models catalog
    to use it if model for this REFID is not found
    """

    t = Transaction(document, "Loading revit family_symbol")

    function_name = inspect.currentframe().f_code.co_name
    logger.info('Trying to load Revit Family to Items.refid -> {}'.format(function_name))
    print('Trying to load Revit Family to Items.refid -> {}'.format(function_name))

    try:
        revit_model_list = os.listdir(path)
        # print('Revit models list -> {}'.format(revit_model_list))
        print('Symbol Name -> {}'.format(symbol_name))

        found = False

        for model in revit_model_list:
            if model.endswith('.rfa'):
                model_name = os.path.splitext(model)[0]
                if symbol_name == model_name:
                    revit_model_load_path = os.path.join(path, model)
                    print('Found! Revit model path -> {}'.format(revit_model_load_path))
                    logger.info('Found! Revit model path -> {}'.format(revit_model_load_path))

                    t.Start()
                    loaded_symbol = document.LoadFamilySymbol(revit_model_load_path, symbol_name)
                    t.Commit()

                    found = True
                    logger.info('Symbol Loaded Transaction -> {}'.format(t.GetStatus()))
                    print('Symbol Loaded Transaction -> {}'.format(t.GetStatus()))

                    return loaded_symbol

        if not found:
            revit_model_load_path = os.path.join(path, default_model_name + '.rfa')
            print('Not found -> revit model for this symbol {}, using Default, path -> {}'.format(symbol_name, revit_model_load_path))
            t.Start()
            loaded_symbol = document.LoadFamilySymbol(revit_model_load_path, symbol_name)
            t.Commit()

            logger.info('Default Model Loaded Transaction -> {}'.format(t.GetStatus()))
            print('Default Model Loaded Transaction -> {}'.format(t.GetStatus()))

            return loaded_symbol

    except Exception as e:
        print('RevitFamilyLoader -> Failed to load Revit families...{}'.format(e))
        logger.error('RevitFamilyLoader -> Failed to load Revit families...{}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            print('Error -> {} Transaction -> {}'.format(e, t.GetStatus()))
            logger.error('Error -> {} Transaction -> {}'.format(e, t.GetStatus()))
