import clr
import math
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
# IMPORTANT => fml files made in cm, Revit works in mm!!! Attention to the numbers
# All imports needet to acccess to RevitAPI
# THIS SCRIPT WORKS FINE!
# http://wiki.theprovingground.org/revit-api-py-setup
# http://wiki.theprovingground.org/revit-api

# Creating application and ifc_document to work with
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document


def create_axis_grid(p_1, p_2):
    # creating simple grid axis with letters in the ends
    # p_1 = XYZ(0,0,0)
    # p_2 = XYZ(5000,0,0)
    line_1 = Line.CreateBound(p_1, p_2)

    t = Transaction(doc, 'Axis Grid')
    t.Start()
    axis_1 = Grid.Create(doc, line_1)
    name = axis_1.get_Parameter(BuiltInParameter.DATUM_TEXT)    # DATUM_TEXT is "name"
    name.Set('X')   # better use UPPERCASE alphabet letters in order and prevern using same letters and numbers



    print(f"Axis element was created...")
    t.Commit()

