import logging
import inspect
from Autodesk.Revit.DB import *

logger = logging.getLogger(__name__)


def get_ifc_model_face(element):
    """
    Getting geometrical face and store it into object
    So we can place Revit Family on it(on face instance).
    """
    function_name = inspect.currentframe().f_code.co_name   # testing Get current function name
    logging.info('Trying to get IFC model geometry face...')

    try:
        options = Options()
        options.ComputeReferences = True
        options.IncludeNonVisibleObjects = False

        geometry_element = element.Geometry[options]
        for geometry_instances in geometry_element:
            geometry_instances = geometry_instances.GetInstanceGeometry()
        for solid in geometry_instances:
            get_type = solid.GetType()      # Autodesk.Revit.DB.Solid
        # for faces in solid.Faces:
        #     print('element is: {}'.format(faces))  # Works => returns FACES
        faces_list = []
        for faces in solid.Faces:
            faces_list.append(faces)
        print('Faces list: {}'.format(faces_list))

        avg_face_area = sum(faces.Area for faces in solid.Faces) / len(faces_list)      # 9.4471253757322255 WORKS! calculate average face area
        biggest_face = []
        for big_face in faces_list:
            if big_face.Area >= avg_face_area:
                biggest_face.append(big_face)
        biggest_face_to_list = list(biggest_face)
        ifc_model_face = biggest_face_to_list[1]
        print('Biggest face: {}'.format(ifc_model_face))
        print('Biggest face: {}'.format(ifc_model_face.Area))

        print('IFC model face: {}'.format(ifc_model_face))
        return ifc_model_face

    except Exception as e:
        print('Error in get_ifc_model_face: {}'.format(e))
        logging.error('Error: {}, \n Function: {}'.format(e, function_name))
        return None
