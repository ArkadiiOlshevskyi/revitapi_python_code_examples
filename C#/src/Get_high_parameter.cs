using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;



public class get_high_parameter_modul
{

    public List<double> Get_high_parameter()
    {
        List<double> doubles = new List<double>();
        try
        {
            Face face = null;
            List<Line> list_of_lines = new List<Line>();
            Line vertical_line_of_planar_face = null;

            foreach (var lines in face.GetEdgesAsCurveLoops())
            {
                foreach (var curve in lines)
                {
                    if (curve is Line)
                    {
                        list_of_lines.Add(curve as Line);
                    }

                }

                vertical_line_of_planar_face = list_of_lines[1];
                double width_parameter = vertical_line_of_planar_face.Length;
                TaskDialog.Show("Get_High_Parameter", width_parameter.ToString());
                doubles.Add(width_parameter);
            }


        }
        catch (Exception e)
        {
            TaskDialog.Show("Get_high_Parameter", $"Error in get_high_parameter: {e.ToString()}");

        }

        return doubles;
    }
