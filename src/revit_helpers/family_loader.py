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


def load_family(document, item_refid, revit_models_path, default_revit_model_name):  # Works Tested
    """
    Loads SINGLE model to Revit ifc_document according REFID on input, returns RevitFamilySYMBOL
    Used for iterating over Json parsing Items position
    That is used on next stage of revit model creation
    as reference what model revit need

    !!! ATTENTION !!! -> This function works only inside or wrapped in revit Transaction

    input:
    -> ifc_document - usually ifc_document, but it must be the ifc_document that you want a make record IN
    -> item_refid - we get from item.refid when parsing items directly from FML file
    -> revit_models_path - folder, storage of revit models with REFID names
    -> default_revit_model_name - usually we have Default model it revit models catalog
    to use it if model for this REFID is not found
    """

    t = Transaction(document, "Loading revit family_symbol")

    function_name = inspect.currentframe().f_code.co_name
    logger.info('Trying to load Revit Family to Items.refid -> {}'.format(function_name))
    print('Trying to load Revit Family to Items.refid -> {}'.format(function_name))

    try:
        revit_model_list = os.listdir(revit_models_path)
        # print('Revit models list -> {}'.format(revit_model_list))
        print('Item REFID -> {}'.format(item_refid))

        found = False

        for model in revit_model_list:
            if model.endswith('.rfa'):
                model_name = os.path.splitext(model)[0]
                if item_refid == model_name:
                    revit_model_load_path = os.path.join(revit_models_path, model)
                    print('Found! Revit model path -> {}'.format(revit_model_load_path))
                    logger.info('Found! Revit model path -> {}'.format(revit_model_load_path))

                    t.Start()
                    document.LoadFamily(revit_model_load_path)
                    t.Commit()

                    found = True
                    logger.info('Refid Model Loaded Transaction -> {}'.format(t.GetStatus()))
                    print('Refid Model Loaded Transaction -> {}'.format(t.GetStatus()))

                    break

        if not found:
            revit_model_load_path = os.path.join(revit_models_path, default_revit_model_name + '.rfa')
            print('Not found -> revit model for this refid {}, using Default BOX, path -> {}'.format(item_refid,
                                                                                                     revit_model_load_path))
            t.Start()
            document.LoadFamily(revit_model_load_path)
            t.Commit()

            logger.info('Default Model Loaded Transaction -> {}'.format(t.GetStatus()))
            print('Default Model Loaded Transaction -> {}'.format(t.GetStatus()))

    except Exception as e:
        print('RevitFamilyLoader -> Failed to load Revit families...{}'.format(e))
        logger.error('RevitFamilyLoader -> Failed to load Revit families...{}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            print('Error -> {} Transaction -> {}'.format(e, t.GetStatus()))
            logger.error('Error -> {} Transaction -> {}'.format(e, t.GetStatus()))
            pass


def select_symbol(document, family_name, default_family_symbol):        # VERS 2 18-04-2024
    """
    Function to select Loaded families in Revit document and activate them
    Returns selected family_symbol symbol or default
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Selecting previously loaded family_symbol symbol -> {}'.format(function_name))
    print('Selecting previously loaded family_symbol symbol -> {}'.format(function_name))

    t = Transaction(document, "Selecting and Activating a Symbol")

    param_id = BuiltInParameter.SYMBOL_NAME_PARAM  # Use the parameter for symbol name
    f_param = ParameterValueProvider(ElementId(param_id))
    f_evaluator = FilterStringEquals()
    f_rule = FilterStringRule(f_param, f_evaluator, family_name)
    filter_symbol_name = ElementParameterFilter(f_rule)

    try:
        selected_family_symbol = FilteredElementCollector(document) \
            .OfCategory(BuiltInCategory.OST_GenericModel) \
            .WherePasses(filter_symbol_name) \
            .WhereElementIsElementType() \
            .FirstElement()

        if selected_family_symbol:
            print('Family Symbol Activating.... -> {}'.format(selected_family_symbol.Name))

            t.Start()
            selected_family_symbol.Activate()
            t.Commit()
            print('Success -> Family name -> {}'.format(selected_family_symbol.Name))
            print('Success -> Family Is Active Status ? -> {}'.format(selected_family_symbol.IsActive))

            return selected_family_symbol

        print("Symbol '{}' not found.".format(family_name))
        print("Using Default Symbol -> '{}'".format(default_family_symbol))
        logger.info("Using Default Symbol -> '{}'".format(default_family_symbol))

        param_id = BuiltInParameter.SYMBOL_NAME_PARAM  # Use the parameter for symbol name
        f_param = ParameterValueProvider(ElementId(param_id))
        f_evaluator = FilterStringEquals()
        f_rule = FilterStringRule(f_param, f_evaluator, default_family_symbol)
        filter_symbol_name = ElementParameterFilter(f_rule)

        default_selection = FilteredElementCollector(document) \
            .OfCategory(BuiltInCategory.OST_GenericModel) \
            .WherePasses(filter_symbol_name) \
            .WhereElementIsElementType() \
            .FirstElement()

        if default_selection:
            print('Family Symbol Activating.... -> {}'.format(default_selection.Name))

            t.Start()
            default_selection.Activate()
            t.Commit()
            print('Success -> Family name -> {}'.format(default_selection.Name))
            print('Success -> Family Is Active Status ? -> {}'.format(default_selection.IsActive))

            return default_selection

        else:
            print("Default Symbol '{}' not found.".format(default_family_symbol))
            logger.info("Default Symbol '{}' not found.".format(default_family_symbol))
            return None

    except Exception as e:
        print('Error while selecting preloaded family_symbol symbol-> {}'.format(e))
        logger.error('Error while selecting preloaded family_symbol symbol-> {}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
        return None


# def select_symbol(document, family_name, default_family_symbol):    # prev working version
#     """
#     Function to select Loaded families in Revit ifc_document
#     And Activate them, so we can use them Symbols to Family Creation
#     RETURNS Family
#     """
#     function_name = inspect.currentframe().f_code.co_name
#     logger.info('Selecting prev Loaded Family Symbol -> {}'.format(function_name))
#     print('Selecting prev Loaded Family Symbol -> {}'.format(function_name))
#
#     param_id = ElementId(BuiltInParameter.SYMBOL_NAME_PARAM)  # Use the parameter for symbol name
#     f_param = ParameterValueProvider(param_id)
#     f_evaluator = FilterStringEquals()
#     f_rule = FilterStringRule(f_param, f_evaluator, family_name)
#     filter_symbol_name = ElementParameterFilter(f_rule)
#
#     try:
#         selected_family_symbols = FilteredElementCollector(document) \
#             .OfCategory(BuiltInCategory.OST_GenericModel) \
#             .WherePasses(filter_symbol_name) \
#             .WhereElementIsElementType() \
#             .FirstElement()
#
#         if selected_family_symbols is not None:
#             return selected_family_symbols
#
#         print("Symbol '{}' not found.".format(family_name))
#         print("Using Default Symbol -> '{}'".format(default_family_symbol))
#         logger.info("Using Default Symbol -> '{}'".format(default_family_symbol))
#
#         param_id = ElementId(BuiltInParameter.SYMBOL_NAME_PARAM)  # Use the parameter for symbol name
#         f_param = ParameterValueProvider(param_id)
#         f_evaluator = FilterStringEquals()
#         f_rule = FilterStringRule(f_param, f_evaluator, default_family_symbol)
#         filter_symbol_name = ElementParameterFilter(f_rule)
#
#         default_selection = FilteredElementCollector(document) \
#             .OfCategory(BuiltInCategory.OST_GenericModel) \
#             .WherePasses(filter_symbol_name) \
#             .WhereElementIsElementType() \
#             .FirstElement()
#
#         return default_selection
#
#     except Exception as e:
#         print('Error while selecting preloaded family_symbol symbol-> {}'.format(e))
#         logger.error('Error while selecting preloaded family_symbol symbol-> {}'.format(e))
#
#         return None


def activate_family(document, selected_loaded_family):
    """
    INPUT   -> previously loaded & selected_level family_symbol
            -> active revit ifc_document (like ifc in backend)
    1) Checking status of family_symbol by calling the method - family_symbol.IsActivated (False/True)
    2) Applying Activation -> Family.Activate() wrapped in Transaction
    3) Checking / printing activation status -> should return True
    RETURN -> Activated FamilySymbol
    """

    function_name = inspect.currentframe().f_code.co_name
    logger.info('Activating pre Selected and pre Loaded FamilySymbol -> {}'.format(function_name))
    print ('Activating pre Selected and pre Loaded FamilySymbol -> {}'.format(function_name))

    t = Transaction(document, "Activation selected_level Family")

    try:
        print('Family Symbol Activating.... -> {}'.format(selected_loaded_family.Name))

        t.Start()
        selected_loaded_family.Activate()

        document.Regenerate()


        t.Commit()
        print('Success -> Family name -> {}'.format(selected_loaded_family.Name))
        print('Success -> Family Is Active Status -> {}'.format(selected_loaded_family.IsActive))

        return selected_loaded_family

    except Exception as e:
        print('ERROR trying to ACTIVATE FamilySymbol -> {}'.format(e))
        if t.HasStarted():
            t.RollBack()
            print('ERROR trying to ACTIVATE FamilySymbol -> {} Transaction Status -> {}'.format(e, t.GetStatus()))


def load_select_activate_family_symbol(document, item_refid, revit_models_path, default_revit_model_name):
    """
    Function includes all steps together by functions listed above:
    Load, select, activate
    RETURN -> ready to use FamilySymbol for NewFamilyInstance
    """
    load_family(document, item_refid, revit_models_path, default_revit_model_name)

    new_selected_symbol = select_symbol(document, item_refid, default_revit_model_name)
    # print('Object is        -> {}'.format(new_selected_symbol))  # Print the names of selected_level symbols for verification
    # print('Object TYPE is   -> {}'.format(type(new_selected_symbol)))  # Print the names of selected_level symbols for verification
    # print('Object PROPS is  -> {}'.format(dir(new_selected_symbol)))  # Print the names of selected_level symbols for verification
    # print('Object NAME is   -> {}'.format(new_selected_symbol.Name))  # Print the names of selected_level symbols for verification

    activated_family = activate_family(document, new_selected_symbol)
    # print('Activated Object is        -> {}'.format(activated_family))  # Print the names of selected_level symbols for verification
    # print('Activated Object TYPE is   -> {}'.format(type(activated_family)))  # Print the names of selected_level symbols for verification
    # print('Activated Object PROPS is  -> {}'.format(dir(activated_family)))  # Print the names of selected_level symbols for verification
    # print('Activated Object NAME is   -> {}'.format(activated_family.Name))

    return activated_family
