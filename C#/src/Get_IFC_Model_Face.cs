using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace revitapi_python_code_examples
{
    public class Get_ifc_model_face
    {

        public List<Face> Get_IFC_Model_Face(Element element)
        {
            try
            {
                Options options = new Options();
                options.ComputeReferences = true;
                options.IncludeNonVisibleObjects = false;

                GeometryElement geometry_element = element.get_Geometry(options);
                GeometryElement geometry_instance = null;
                foreach (var geometry_instances in geometry_element)
                {
                    if (geometry_instances is GeometryInstance)
                    {
                        GeometryInstance geometryInstance = geometry_instances as GeometryInstance;

                        GeometryElement instance_geometry = geometryInstance.GetInstanceGeometry();
                        geometry_instance = instance_geometry;
                    }
                }
                List<Face> faces_list = new List<Face>();
                foreach (Solid solid in geometry_instance)
                {
                    var get_type = solid.GetType();

                    foreach (Face face in solid.Faces)
                    {
                        faces_list.Add(face);
                    }
                }

                double avg_face_area = faces_list.Select(x => x.Area).Average();
                List<Face> biggest_face = new List<Face>();
                foreach (Face face in faces_list)
                {
                    if (face.Area > avg_face_area)
                    {
                        biggest_face.Add(face);
                    }
                }
                return biggest_face;
            }
            catch (Exception e)
            {
                TaskDialog.Show("Get_IFC_Model_Face", e.Message.ToString());
                return null;
            }

        }

    }
}