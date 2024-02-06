import ifcopenshell
import uuid

def add_new_wall(ifc_file, coordinates, x_dim, y_dim, depth):
    # Access necessary instances for wall creation
    owner_history = ifc_file.by_type("IfcOwnerHistory")[0]

    # Create a default placement for the profile
    axis2placement = ifc_file.createIfcAxis2Placement3D(
        Location=ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
        Axis=ifc_file.createIfcDirection((0.0, 0.0, 1.0)),
        RefDirection=ifc_file.createIfcDirection((1.0, 0.0, 0.0))
    )

    # Define a basic rectangular profile for the wall using input dimensions
    wall_profile = ifc_file.createIfcRectangleProfileDef(
        ProfileType="AREA",
        ProfileName="WallProfile",
        Position=ifc_file.createIfcAxis2Placement2D(ifc_file.createIfcCartesianPoint((0.0, 0.0))),
        XDim=x_dim,  # Wall length in meters, user input
        YDim=y_dim   # Wall thickness in meters, user input
    )

    # Extrude the profile to create a solid shape representing the wall geometry
    wall_solid = ifc_file.createIfcExtrudedAreaSolid(
        SweptArea=wall_profile,
        Position=axis2placement,
        ExtrudedDirection=ifc_file.createIfcDirection((0.0, 0.0, 1.0)),
        Depth=depth  # Wall height in meters, user input
    )

    # Create a product definition shape to hold the geometry
    product_definition_shape = ifc_file.createIfcProductDefinitionShape(
        Representations=[ifc_file.createIfcShapeRepresentation(
            ContextOfItems=ifc_file.by_type("IfcGeometricRepresentationContext")[0],
            RepresentationIdentifier="Body",
            RepresentationType="SweptSolid",
            Items=[wall_solid]
        )]
    )

    # Specify the wall's location using IfcLocalPlacement
    local_placement = ifc_file.createIfcLocalPlacement(
        RelativePlacement=ifc_file.createIfcAxis2Placement3D(
            Location=ifc_file.createIfcCartesianPoint(coordinates)
        )
    )

    # Generate a GlobalId for IFC
    global_id = ifcopenshell.guid.compress(uuid.uuid1().hex)

    # Create the wall instance with geometry and placement
    new_wall = ifc_file.createIfcWallStandardCase(
        GlobalId=global_id,
        OwnerHistory=owner_history,
        Name="New Wall",
        Description="A new wall with specified dimensions and location",
        ObjectType="Wall",
        ObjectPlacement=local_placement,
        Representation=product_definition_shape,
        Tag="WallTag"
    )
    return new_wall


def find_wall_orientation_by_name(model, wall_name):
    """
    Finds and prints the orientation vectors of a wall specified by its name.

    Parameters:
    - model: The IFC model loaded with ifcopenshell.
    - wall_name: The name of the wall to find.
    """
    walls = model.by_type("IfcWall")
    for wall in walls:
        if wall.Name == wall_name:
            # Get the local placement matrix for the specified wall
            matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)

            # Extract orientation vectors
            x_direction = matrix[:3, 0]  # Local X-axis direction
            y_direction = matrix[:3, 1]  # Local Y-axis direction
            z_direction = matrix[:3, 2]  # Local Z-axis direction

            print(f"Wall '{wall_name}' Orientation Vectors:")
            print("X-axis direction:", x_direction)
            print("Y-axis direction:", y_direction)
            print("Z-axis direction:", z_direction)
            print("XYZ coordinates:", matrix[:, 3][:3])
            return

    print(f"Wall named '{wall_name}' not found.")


# Find and print the orientation vectors of the specified wall

import ifcopenshell
import uuid

def add_new_wall(ifc_file, coordinates, x_dim, y_dim, depth):
    # Access necessary instances for wall creation
    owner_history = ifc_file.by_type("IfcOwnerHistory")[0]

    # Create a default placement for the profile
    axis2placement = ifc_file.createIfcAxis2Placement3D(
        Location=ifc_file.createIfcCartesianPoint((0.0, 0.0, 0.0)),
        Axis=ifc_file.createIfcDirection((0.0, 0.0, 1.0)),
        RefDirection=ifc_file.createIfcDirection((1.0, 0.0, 0.0))
    )

    # Define a basic rectangular profile for the wall using input dimensions
    wall_profile = ifc_file.createIfcRectangleProfileDef(
        ProfileType="AREA",
        ProfileName="WallProfile",
        Position=ifc_file.createIfcAxis2Placement2D(ifc_file.createIfcCartesianPoint((0.0, 0.0))),
        XDim=x_dim,  # Wall length in meters, user input
        YDim=y_dim   # Wall thickness in meters, user input
    )

    # Extrude the profile to create a solid shape representing the wall geometry
    wall_solid = ifc_file.createIfcExtrudedAreaSolid(
        SweptArea=wall_profile,
        Position=axis2placement,
        ExtrudedDirection=ifc_file.createIfcDirection((0.0, 0.0, 1.0)),
        Depth=depth  # Wall height in meters, user input
    )

    # Create a product definition shape to hold the geometry
    product_definition_shape = ifc_file.createIfcProductDefinitionShape(
        Representations=[ifc_file.createIfcShapeRepresentation(
            ContextOfItems=ifc_file.by_type("IfcGeometricRepresentationContext")[0],
            RepresentationIdentifier="Body",
            RepresentationType="SweptSolid",
            Items=[wall_solid]
        )]
    )

    # Specify the wall's location using IfcLocalPlacement
    local_placement = ifc_file.createIfcLocalPlacement(
        RelativePlacement=ifc_file.createIfcAxis2Placement3D(
            Location=ifc_file.createIfcCartesianPoint(coordinates)
        )
    )

    # Generate a GlobalId for IFC
    global_id = ifcopenshell.guid.compress(uuid.uuid1().hex)

    # Create the wall instance with geometry and placement
    new_wall = ifc_file.createIfcWallStandardCase(
        GlobalId=global_id,
        OwnerHistory=owner_history,
        Name="New Wall",
        Description="A new wall with specified dimensions and location",
        ObjectType="Wall",
        ObjectPlacement=local_placement,
        Representation=product_definition_shape,
        Tag="WallTag"
    )
    return new_wall


def find_wall_orientation_by_name(model, wall_name):
    """
    Finds and prints the orientation vectors of a wall specified by its name.

    Parameters:
    - model: The IFC model loaded with ifcopenshell.
    - wall_name: The name of the wall to find.
    """
    walls = model.by_type("IfcWall")
    for wall in walls:
        if wall.Name == wall_name:
            # Get the local placement matrix for the specified wall
            matrix = ifcopenshell.util.placement.get_local_placement(wall.ObjectPlacement)

            # Extract orientation vectors
            x_direction = matrix[:3, 0]  # Local X-axis direction
            y_direction = matrix[:3, 1]  # Local Y-axis direction
            z_direction = matrix[:3, 2]  # Local Z-axis direction

            print(f"Wall '{wall_name}' Orientation Vectors:")
            print("X-axis direction:", x_direction)
            print("Y-axis direction:", y_direction)
            print("Z-axis direction:", z_direction)
            print("XYZ coordinates:", matrix[:, 3][:3])
            return

    print(f"Wall named '{wall_name}' not found.")


# Find and print the orientation vectors of the specified wall

