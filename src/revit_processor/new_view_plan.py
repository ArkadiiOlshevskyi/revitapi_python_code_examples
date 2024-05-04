import logging
import inspect

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')

from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector, ViewFamilyType

logger = logging.getLogger(__name__)


def select_view_plan(document, type_of_plan):
    """
    Selection ViewTypeId to create other plans.

    Args:
        document (Document): The Revit ifc_document.
        type_of_plan (str): getting on input preselected from Revit built-in system templates 'Architectural Plan' for creating floor plan 2d view projection

    Returns:
        ViewPlan: The selected template of  ViewPlan (Architectural) object if successful, None otherwise.
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Selecting ViewTypeFamily - Architectural -> {}'.format(function_name))
    print('Selecting ViewTypeFamily - Architectural -> {}'.format(function_name))

    try:
        view_family_types = FilteredElementCollector(document).OfClass(ViewFamilyType).ToElements()
        for view in view_family_types:
            if view.Name == type_of_plan:
                selected_view = view
                print(selected_view.Id)
                print(type(selected_view))
                print(dir(selected_view))

                return selected_view  # Return None if no drafting view family_symbol type is found

    except Exception as e:
        logger.error('Error while trying to select view -> {}'.format(e))
        print('Error while trying to select view -> {}'.format(e))
        return None


def create_view_plan(document, selected_plan, view_name, level_id):
    """
    Create a ViewPlan in Revit.
    ViewPlan can be -> (FloorPlan, Ceiling Plan, StructuralPlan, AreaPlan)

    Args:
        document (Document): The Revit ifc_document.
        selected_plan (id): plan as template, for 90% cases it will be 'Architectural Plan'
        view_name (str): The name of the view plan to create.
        level_id (Level): The Revit level to associate the view plan with.

    Returns:
        ViewPlan: The created ViewPlan object if successful, None otherwise.
    """
    function_name = inspect.currentframe().f_code.co_name
    logger.info('Function "{}" started.'.format(function_name))
    print('Function "{}" started.'.format(function_name))

    try:
        t = Transaction(document, "Create ViewPlan")
        t.Start()

        view_plan = ViewPlan.Create(document, selected_plan.Id, level_id)
        view_plan.Name = view_name      # setting the floor plan name

        t.Commit()

        logger.info('ViewPlan "{}" created successfully.'.format(view_name))
        print('ViewPlan "{}" created successfully.'.format(view_name))
        return view_plan

    except Exception as ex:
        logger.error('Error while creating ViewPlan "{}": {}'.format(view_name, ex))
        print('Error while creating ViewPlan "{}": {}'.format(view_name, ex))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            print(t.GetStatus())
            logger.error(t.GetStatus())
        return None


# ########################## TEST CASE -> WORKS 26-3-2024 ##########################
# ifc_document = __revit__.ActiveUIDocument.Document
# type_of_plan = 'Architectural Plan'
#
# selected_view_plan = select_view_plan(ifc_document, type_of_plan)
# print(selected_view_plan)
# print(type(selected_view_plan))
# print(dir(selected_view_plan))
# print('ID of selected plan: {}'.format(selected_view_plan.Id))
# print('ID of selected plan: {}'.format(selected_view_plan.Name))

