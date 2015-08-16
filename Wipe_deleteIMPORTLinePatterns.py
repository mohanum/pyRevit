from Autodesk.Revit.DB import FilteredElementCollector
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import LinePatternElement
from Autodesk.Revit.UI import TaskDialog

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

cl = FilteredElementCollector(doc).OfClass(LinePatternElement).ToElements()

t = Transaction(doc,"Remove Pattern")
t.Start()

for lp in cl:
	if 'import' in lp.Name.lower():
		print('\nIMPORTED LINETYPE FOUND:\n{0}'.format( lp.Name ))
		doc.Delete( lp.Id )
		print('--- DELETED ---')

t.Commit()