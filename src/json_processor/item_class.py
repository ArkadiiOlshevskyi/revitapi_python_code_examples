import os
import sys

sys.path.append('C:\Program Files\IronPython 3.4\Lib\site-packages')

import json
import logging
import inspect

logger = logging.getLogger(__name__)


class Item:
    """
    Item in FML is usually furniture or equipment objects.
    1) We are parsing Item from Items in FML json file.
    2) Then we are mapping Item REFID with FamilySymbol name in ModelsName Json.
    3) Creating Revit NewFamilyInstance with FamilySymbol and other data.
    """

    def __init__(self, refid, x, y, z, length, width, height, rotation):
        self.refid = refid
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.width = width
        self.height = height
        self.rotation = rotation

    @classmethod
    def process_config(cls, item_config):
        """Process config item data"""
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Trying to process config item data in {}'.format(function_name))

        try:
            refid = item_config.get('refid', '')
            x = item_config.get('x', 0)
            y = item_config.get('y', 0)
            z = item_config.get('z', 0)
            length = item_config.get('height', 0)
            width = item_config.get('width', 0)
            height = item_config.get('z_height', 0)
            rotation = item_config.get('rotation', 0)

            print('FML Item parameters processed....')
            return cls(refid, x, y, z, width, length, height, rotation)
        except Exception as e:
            logger.error('Error: {}, \n Function: {}'.format(e, function_name))
            print('Error: {}, \n Function: {}'.format(e, function_name))
            return None

    def print_parsed_data(self):
        """Just a test print function"""
        print('refid: {}'.format(self.refid))
        print('x: {}'.format(self.x))
        print('y: {}'.format(self.y))
        print('z: {}'.format(self.z))
        print('width: {}'.format(self.length))
        print('width: {}'.format(self.width))
        print('height: {}'.format(self.height))
        print('rotation: {}'.format(self.rotation))


def item_list_from_fml(input_path, project_name):     # Works Tested - not used anymore
    """
    Extracts items from an FML file for a given project.

    input_path -> FML file of the project that contains all needed data
                   FML can be with extensions like '.fml' or '.json.fml'
    This list later used to create new models in revit
    by accessing items attributes
    """

    function_name = inspect.currentframe().f_code.co_name
    logger.info('Extracting Items to List from FML -> {}'.format(function_name))
    print('Extracting Items to List from FML -> {}'.format(function_name))

    items_list = []

    try:
        for file_name in os.listdir(input_path):
            if file_name.endswith('.fml') and file_name.startswith(project_name):
                fml_to_open_path = os.path.join(input_path, file_name)

        # print('fml path!!! -> {}'.format(fml_to_open_path))   # to check the path

        with open(fml_to_open_path, 'r') as fml_file:
            fml_data = json.load(fml_file)

        for categories in fml_data['floors']:
            for designs in categories['designs']:
                for items in designs['items']:
                    new_item = Item.process_config(items)
                    items_list.append(new_item)

        return items_list  # Return the complete list of items after processing all files

    except Exception as e:
        logger.error('Error: {}'.format(e))
        print('Error: {}'.format(e))
        return None


# # TEST CASE => WORKS ###########################################################################
# fml_file = r"C:\Users\3duni\Desktop\Arkadii\2_projects_tasks\8_revit_api_converter_3\input\test_4_march"
# name = 'test_IFC_FML_0'
# # name = 'Blinqlab ITEM collection'
# items_list = item_list_from_fml(fml_file, name)
# # print('Done  ' + '=' * 50)
# print('Items list -> {}'.format(items_list))
# print('Total Items list -> {}'.format(len(items_list)))
# #
# for item_obj in items_list:
#     print('Items refid is => {}'.format(item_obj.refid))
