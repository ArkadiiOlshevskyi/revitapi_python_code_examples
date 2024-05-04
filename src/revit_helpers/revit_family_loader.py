import os
import logging
import inspect
import sys

sys.path.append('C:\Program Files\IronPython 3.4\Lib\site-packages')

import clr  # Imports to works with Revit API .NET implementation via python
from System.Collections.Generic import List
from collections import OrderedDict
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.DB.IFC import *
from Autodesk.Revit.DB import Transaction, FilteredElementCollector, View3D, DWGExportOptions, ElementId
from Autodesk.Revit.ApplicationServices import *
from Autodesk.Revit.DB import Document, IFCExportOptions, Transaction
from Autodesk.Revit.UI.Events import DialogBoxShowingEventArgs
from Autodesk.Revit.UI.Events import DisplayingOptionsDialogEventArgs

from Autodesk.Revit.UI import TaskDialog, TaskDialogResult, TaskDialogCommandLinkId, TaskDialogCommonButtons
from Autodesk.Revit.DB import FailureProcessingResult, IFailuresPreprocessor
from Autodesk.Revit.DB import Transaction, FailureHandlingOptions

logger = logging.getLogger(__name__)


class RevitFamiliesLoader:
    """
    Processor that loads Revit families(models) to IFC Revit model (ifc_document)
    and returns ifc_document with models.
    All models have the same {filename} as REFID items in FML.

    Input:
    :ifc_document - revit active ifc_document. Can be previously openet IFC model in Revit.
    :revit_models_path - path to revit models
    :item_list - list of objects(Item class) with data attributes like REFID, x,y,z.....

    Logic:
    1) Checking if directory with revit models is exists
    2) Getting all the filenames inside this directory
    3) Mapping filenames in directory to item list REFIDS
        -> if model found - load it (to get FamilySymbol in Revit later)
        -> if model not found - load default Default_XYZ_box.rfa model (simple box)
        -> if Default_XYZ_box.rfa not found - pass
    """

    print('RevitFamilyLoader class is loaded')
    logger.info('RevitFamilyLoader class is loaded')

    def __init__(self, document, revit_models_paths, item_list):
        self.document = document
        self.revit_models_paths = revit_models_paths
        self.item_list = item_list


    def check_path_is_exist(self, revit_models_path):
        """Checking if directory with revit models is exists"""
        function_name = inspect.currentframe().f_code.co_name
        print('RevitFamilyLoader -> Checking directory is exist...')
        logger.info('RevitFamilyLoader -> Checking directory is exist...{}'.format(function_name))

        try:
            if os.path.exists(revit_models_path):
                print('Path Exists: {}'.format(revit_models_path))
                return revit_models_path
            else:
                print('RevitFamilyLoader -> Directory NOT EXISTS...')
                logger.error('RevitFamilyLoader -> Directory NOT EXISTS...')
                return None
        except Exception as e:
            print('RevitFamilyLoader -> Failed to Check directory is exist...{}'.format(e))
            logger.error('RevitFamilyLoader -> Failed to Check directory is exist...{}'.format(e))
            pass


    def get_revit_models_list(self, existing_revit_models_path):
        """Getting list of revit models that exist in directory"""
        function_name = inspect.currentframe().f_code.co_name
        print('RevitFamilyLoader -> Getting Revit models from directory...')
        logger.info('RevitFamilyLoader -> Getting Revit models from directory...{}'.format(function_name))

        revit_models_list = []

        try:
            revit_models_list = os.listdir(existing_revit_models_path)
            print(revit_models_list)
            logger.info('revit models stored in list -> {}'.format(revit_models_list))
            print('revit models stored in list -> {}'.format(revit_models_list))
            print(revit_models_list)
            return revit_models_list

        except Exception as e:
            print('RevitFamilyLoader -> Failed Getting Revit models from directory...{}'.format(e))
            logger.error('RevitFamilyLoader -> Failed Getting Revit models from directory...{}'.format(e))
            pass


    def mapp_and_load_revit_family_name_to_refid(self, document, revit_models_path, items_list):
        """Loads models to Revit ifc_document, returns ifc_document"""
        t = Transaction(document, "Loading revit family_symbol")
        
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Trying to mapp and load revit models according to REFID -> {}'.format(function_name))

        try:
            for item_object in items_list:
                if item_object.refid in os.listdir(revit_models_path):
                    if item_object.refid.endswith(".rfa"):
                        family_path = os.path.join(revit_models_path, item_object.refid)
                    else:
                        family_path = os.path.join(revit_models_path, item_object.refid + ".rfa")       # ?

                    if os.path.exists(family_path):
                        t.Start()
                        document.LoadFamily(family_path)
                        t.Commit()
                        print('Loaded Revit family_symbol for REFID {}'.format(item_object.refid))
                        logger.info('Loaded Revit family_symbol for REFID {}'.format(item_object.refid))
                    else:
                        default_revit_model_name = "Default_XYZ_box"
                        default_family_path = os.path.join(revit_models_path, default_revit_model_name + ".rfa")
                        t.Start()
                        document.LoadFamily(default_family_path)
                        t.Commit()
                        print('Default family_symbol not found for REFID {} -> Using Default_XYZ_box'.format(item_object.refid))
                        logger.info('Default family_symbol not found for REFID {} -> Using Default_XYZ_box'.format(item_object.refid))
                else:
                    print('No Revit family_symbol and no Default family_symbol found for REFID {}. Skipping.'.format(item_object.refid))
                    logger.info('No Revit family_symbol and no Default family_symbol found for REFID {}. Skipping.'.format(item_object.refid))
                    pass

            return document

        except Exception as e:
            print('RevitFamilyLoader -> Failed to load Revit families...{}'.format(e))
            logger.error('RevitFamilyLoader -> Failed to load Revit families...{}'.format(e))
            if t.HasStarted() and not t.HasEnded():
                t.RollBack()
                print('Error -> {} {}'.format(e, t.GetStatus()))
                logger.error('Error -> {} {}'.format(e, t.GetStatus()))

