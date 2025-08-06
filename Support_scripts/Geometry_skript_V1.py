from ansys.geometry.core import launch_modeler
from ansys.geometry.core.math import (
  Plane,
  Point2D,
  Point3D,
  UNITVECTOR3D_X,
  UNITVECTOR3D_Y,
  UNITVECTOR3D_Z,
)
from ansys.geometry.core.misc import UNITS, Angle
from ansys.geometry.core.sketch import Sketch
from pint import Quantity


def face_identifier(faces, axis):
    """
    Sort a pair of planar faces based on their positions along the specified coordinate axis.

    Args:
        faces : List[IFace, IFace]
        List of planar face pairs.

        axis : (string)
        Axis to sort the face pair on. Options are "x", "y", or "z".

    Returns:
        IFace, IFace
        - IFace: Face with the centroid positioned behind the other face along the specified axis.
        - IFace: Face with the centroid positioned ahead of the other face along the specified axis.

    """
    min_face = ""
    max_face = ""
    if axis == "x":
        position = 0
    elif axis == "y":
        position = 1
    else:
        position = 2
    min_face_cor_val = faces[0].point(0.5, 0.5)[position]
    min_face = faces[0]
    max_face_cor_val = faces[0].point(0.5, 0.5)[position]
    max_face = faces[0]
    for face in faces[1:]:
        if face.point(0.5, 0.5)[position] < min_face_cor_val:
            min_face_cor_val = face.point(0.5, 0.5)[position]
            min_face = face
            continue
        elif face.point(0.5, 0.5)[position] > max_face_cor_val:
            max_face_cor_val = face.point(0.5, 0.5)[position]
            max_face = face
    return min_face, max_face

plane_surface = []
cylindrical_surface = []

m = launch_modeler()
print(m)
design = m.create_design("Tunnel")
middle_radius = 12
tunnel_width = 10
tunnel_height = 7
tunnel_angle = 60
min_z_cooridinate = -0.200

plane_profile = Plane(
    origin=Point3D([0,0, tunnel_height/2+min_z_cooridinate]),
    direction_x=UNITVECTOR3D_Y,
    direction_y=UNITVECTOR3D_Z,
)
profile = Sketch(plane=plane_profile)
'''
(profile.segment(Point2D([-tunnel_width/2, min_z_cooridinate], unit=UNITS.mm), Point2D([tunnel_width/2, min_z_cooridinate], unit=UNITS.mm))
    .segment_to_point(Point2D([tunnel_width/2, tunnel_height+min_z_cooridinate], unit=UNITS.mm))
    .segment_to_point(Point2D([-tunnel_width/2, tunnel_height+min_z_cooridinate], unit=UNITS.mm))
    .segment_to_point(Point2D([-tunnel_width/2, min_z_cooridinate], unit=UNITS.mm))
)
'''
(profile.box(Point2D([0,0], unit=UNITS.m), Quantity(tunnel_width, UNITS.m), Quantity(tunnel_height, UNITS.m)))


component_1 = design.add_component("Component1")
enclosure = component_1.revolve_sketch(
    "tunnel",
    sketch=profile,
    axis=UNITVECTOR3D_Z,
    angle=Angle(tunnel_angle, unit=UNITS.degrees),
    rotation_origin=Point3D([0, middle_radius, 0]),
)

body = component_1.get_all_bodies()[0]
body.rotate(axis_origin=Point3D([0, middle_radius, 0]), 
            axis_direction=UNITVECTOR3D_Z, 
            angle=Angle(-tunnel_angle/2, unit=UNITS.degrees))

for face in enclosure.faces:
    if face.surface_type.name == "SURFACETYPE_PLANE":
        plane_surface.append(face)
    elif face.surface_type.name == "SURFACETYPE_CYLINDER":
        cylindrical_surface.append(face)
        
tunnel_inlet,  tunnel_outlet = face_identifier(faces=plane_surface, axis="x")
tunnel_road , tunnel_top= face_identifier(faces=plane_surface, axis="z")
tunnel_symm1 = cylindrical_surface[0]
tunnel_symm2 = cylindrical_surface[1]


design.create_named_selection("tunnel_xmin", faces=[tunnel_inlet])
design.create_named_selection("tunnel_xmax", faces=[tunnel_outlet])
design.create_named_selection("tunnel_zmax", faces=[tunnel_top])
design.create_named_selection("tunnel_zmin", faces=[tunnel_road])
design.create_named_selection("tunnel_ymin", faces=[tunnel_symm1])
design.create_named_selection("tunnel_ymax", faces=[tunnel_symm2])


file = design.export_to_pmdb()