# REVITAPI PYTHON CODE EXAMPLES

This repo contains tested code examples for geometry creation in Revit2024 (RevitAPI)
Because in general there are not much python examples in web about working with.
Also, there are a lot of different information you have to pass through before
to understand RevitAPI conception.
So the idea was to collect all best samples and approaches in one place, 
test them, and use them for current task or pipeline.

Code examples split in small snippets(functions), 
so you can easy find-out what is exactly you need and use it in your current case.
Also fill free to comment and contribute.


## Content:

Automation_pyRevit_Launches:
- Python scripts that listen folder for different files and launch revit automation script

data:
- JSON file sample that you can use for testing
- IFC file for test
- Revit file as an output

scr:
- json processor (to extract data from json)
- revit_helpers (to save dwg, ifc, etc.)
- revit_ifc_processor (to work with imported ifc geometry.)
- revit utilities (to extract data from json)
