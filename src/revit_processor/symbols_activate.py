import clr  # Imports to works with Revit API .NET implementation via python
from System.Collections.Generic import List
from collections import OrderedDict

from Autodesk.Revit.DB import *

document = __revit__.ActiveUIDocument.Document

all_generic_models_preloaded = FilteredElementCollector(document).\
    OfCategory(BuiltInCategory.OST_GenericModel).\
    WhereElementIsElementType().\
    ToElements()

print(type(all_generic_models_preloaded))
print(len(all_generic_models_preloaded))
print(all_generic_models_preloaded)

t = Transaction(document, "Activating Preloaded Symbol")

for family_symbol in all_generic_models_preloaded:
    # print('Selected symbol -> {}'.format(family_symbol))
    # print('Selected symbol DIR -> {}'.format(dir(family_symbol)))
    # print('Selected symbol Active ? -> {}'.format(family_symbol.IsActive))
    print('Selected symbol Name -> {}'.format(family_symbol.Name))

    print('Trying Activating Preloaded Symbol')
    t.Start()
    family_symbol.Activate()
    t.Commit()
    print(t.GetStatus())
    document.Regenerate()

    print('done')
