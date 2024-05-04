import logging
import inspect

import clr

clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *


logger = logging.getLogger(__name__)


def delete_host_model_level(document, host_models_level_name):
    """
    We are using HOST MODEL level in revit template where all models and walls, doors are placed.
    After all models were created we need to delete this models level
    And all models templates will be deleted too.
    This is function to fix the problem with activating and preloading revit families Symbols

    Business logic:
        1) Selecting all levels in Revit Document
        2) Finding a level with 'MODELS HOST LEVEL' name and deleting it with all geometry and models on it

    Parameters:
        - ifc_document (type): Active Revit Document.
        - host_models_level_name (str): Name of the level to be deleted.

    Returns:
        None

    Raises:
        Exception: Transaction errors or mistakes in Input.
    """

    function_name = inspect.currentframe().f_code.co_name
    logger.info('Deleting HOST MODELS LEVEL {}'.format(host_models_level_name))
    print('Deleting HOST MODELS LEVEL {}'.format(host_models_level_name))

    try:
        t = Transaction(document, 'Deleting HOST MODELS LEVEL')

        t.Start()

        levels = FilteredElementCollector(document).OfCategory(BuiltInCategory.OST_Levels).WhereElementIsNotElementType().ToElements()

        selectedLevel = None
        for level in levels:
            if level.Name == host_models_level_name:
                selectedLevel = level
                break

        if selectedLevel:
            document.Delete(selectedLevel.Id)
            t.Commit()
            logger.info('Successfully DELETED HOST MODEL LEVEL -> {}'.format(host_models_level_name))
            print('Successfully DELETED HOST MODEL LEVEL -> {}'.format(host_models_level_name))
        else:
            logger.info('No level found with name: {}'.format(host_models_level_name))
            print('No level found with name: {}'.format(host_models_level_name))

    except Exception as e:
        logger.error('Error while deleting level -> {}'.format(e))
        print('Error while deleting level -> {}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            logger.error('Transaction rollback due to error: {}'.format(e))
            print('Transaction rollback due to error: {}'.format(e))


document = __revit__.ActiveUIDocument.Document
host_models_level_name = "MODELS HOST LEVEL"

delete_host_model_level(document, host_models_level_name)
