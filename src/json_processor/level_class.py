import logging
import inspect
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import *

logger = logging.getLogger(__name__)

"""
"project_id":150357990,
"name":"Begane grond",
"level":0,
"created_at":"2023-12-07T21:13:49.000Z",
"updated_at":"2024-01-08T20:00:06.000Z",
"height":280.0,
"""

"""
Level level N: 0
Level Name: Begane grond
Level Height in cm: 280.0
Level Project Height in cm: 280.0
"""

"""
public static Level Create(
	Document ifc_document,
	double elevation
)
"""


class Level:
    """
    Level in FML might be single in most of the cases
    and can be multimple levels in one FML file.
    !!!Level IS NOT Floor(Slab)!!!
    FML file contains "floors":
    -> where "level"(s) represented with number 0, 1, 2, 3, 4...etc.
    Then we need "level", "name", "height" values.
    Level is Host for Walls, Floors in Revit.

    Logic:
    1) We parse FML for "floors" -> "level" and get value f.ex. 0
    2) Then by separate function we check if in Revit project
    we are already have "level" with the same value 0 (in 100% cases we have it)
    3) We assign this existing Revit level as 0 level
    4) We might change "name" (like "Begane grond")
    5) We might change "height" (like "280.0" -> divide value for 25...)

    Else:
    1) If value of "level" is else than 0 (like 1,2,3.. or -1?)
    We create new Revit level and store it into variable.
    2) Than all Walls for this level will be hosted in this level
    """

    def __init__(self, name, level, height):
        self.name = name  # "Begane grond"
        self.level = level  # -1? 0,2,3,4
        self.level_full_name = level + '' + name
        self.height = height  # Accumulative height with += total_height

    @classmethod
    def process_config(cls, item_config):
        """Process config item data"""
        function_name = inspect.currentframe().f_code.co_name
        logger.info('Trying to process config Level data in {}'.format(function_name))

        try:
            name = item_config.get('name', 0)
            level = item_config.get('level', 0)
            height = item_config.get('height', 0)

            print('FML Item parameters processed....')
            return cls(name, level, height)
        except Exception as e:
            logger.error('Error: {}, \n Function: {}'.format(e, function_name))
            print('Error: {}, \n Function: {}'.format(e, function_name))
            return None

    def print_parsed_data(self):
        """Just a test print function"""
        print('Level name: {}'.format(self.name))
        print('Level level: {}'.format(self.level))
        print('Level height: {}'.format(self.height))


def create_new_level(document, level_name, level_project_height):
    """
    Creating new level from FML data
    and using Revit transaction

    Parameters:
    - ifc_document (revit ifc_document): opened Revit Active UI Document like init_template.rvt.
    - level_name (str): Level name from FML.
    - level_project_height (float): converted to feet height,
                                    if level is <0 accumulated with Total_height variable in parser.

    Returns:
    # type: Level stored in variable. Ready to use as host for Walls in this level

    Raises:
    # ExceptionType: If problems with Revit Transaction.

    Examples:
    # >>> example_function(2, 3)

    """

    function_name = inspect.currentframe().f_code.co_name
    logger.info('Creating new Level in Revit -> {}'.format(function_name))
    print('Creating new Level in Revit -> {}'.format(function_name))

    t = Transaction(document, "Creating New Level")

    try:
        t.Start()

        new_level = Level.Create(document, level_project_height / 304.8)    # FIX with processor
        new_level.Name = level_name

        t.Commit()

        return new_level

    except Exception as e:
        logger.error('Error while trying to create new level -> {}'.format(e))
        print('Error while trying to create new level -> {}'.format(e))
        if t.HasStarted() and not t.HasEnded():
            t.RollBack()
            print(t.GetStatus())


## TEST CASE -> WORKS 8-3-2024 #######################################################################
# import wescan_paths  # Remote after testing
#
document = __revit__.ActiveUIDocument.Document
level_name = 'new_test_level'
level_height = 6000

new_host_level = create_new_level(document, level_name, level_height)

print('Done  ' + '=' * 100)
