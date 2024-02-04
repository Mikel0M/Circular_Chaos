import ifcopenshell
import ifcopenshell.util.element
import streamlit as st
import csv
import pandas as pd
import sortingFunctions as sf
import tempfile
import os
import createWall as CW
from tools import ifchelper
import json
import Homepage
import uuid
##################### STREAMLIT IFC-JS COMPONENT MAGIC ######################
from pathlib import Path  #
from re import L  #
from typing import Optional  #
import streamlit.components.v1 as components  #

def draw_3d_viewer():
    def get_current_ifc_file():
        return session.array_buffer

    session.ifc_js_response = ifc_js_viewer(get_current_ifc_file())
    st.sidebar.success("Visualiser loaded")


def get_psets_from_ifc_js():
    if session.ifc_js_response:
        return json.loads(session.ifc_js_response)


def format_ifc_js_psets(data):
    return ifchelper.format_ifcjs_psets(data)


def initialise_debug_props(force=False):
    if not "BIMDebugProperties" in session:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }
    if force:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }


def get_object_data(fromId=None):
    def add_attribute(prop, key, value):
        if isinstance(value, tuple) and len(value) < 10:
            for i, item in enumerate(value):
                add_attribute(prop, key + f"[{i}]", item)
            return
        elif isinstance(value, tuple) and len(value) >= 10:
            key = key + "({})".format(len(value))

        propy = {
            "name": key,
            "string_value": str(value),
            "int_value": int(value.id()) if isinstance(value, ifcopenshell.entity_instance) else None,
        }
        prop.append(propy)

    if session.BIMDebugProperties:
        initialise_debug_props(force=True)
        step_id = 0
        if fromId:
            step_id = int(fromId)
        else:
            step_id = int(session.object_id) if session.object_id else 0
        debug_props = st.session_state.BIMDebugProperties
        debug_props["active_step_id"] = step_id

        crumb = {"name": str(step_id)}
        debug_props["step_id_breadcrumb"].append(crumb)
        element = session.ifc_file.by_id(step_id)
        debug_props["inverse_attributes"] = []
        debug_props["inverse_references"] = []

        if element:

            for key, value in element.get_info().items():
                add_attribute(debug_props["attributes"], key, value)

            for key in dir(element):
                if (
                        not key[0].isalpha()
                        or key[0] != key[0].upper()
                        or key in element.get_info()
                        or not getattr(element, key)
                ):
                    continue
                add_attribute(debug_props["inverse_attributes"], key, getattr(element, key))

            for inverse in session.ifc_file.get_inverse(element):
                propy = {
                    "string_value": str(inverse),
                    "int_value": inverse.id(),
                }
                debug_props["inverse_references"].append(propy)

            print(debug_props["attributes"])


def edit_object_data(object_id, attribute):
    entity = session.ifc_file.by_id(object_id)
    print(getattr(entity, attribute))


def write_pset_data():
    data = get_psets_from_ifc_js()
    if data:
        st.subheader("Object Name")
        psets = format_ifc_js_psets(data['props'])
        for pset in psets.values():
            st.subheader(pset["Name"])
            st.table(pset["Data"])


def write_health_data():
    st.subheader("🩺 Debugger")
    ## REPLICATE IFC DEBUG PANNEL
    row1_col1, row1_col2 = st.columns([1, 5])
    with row1_col1:
        st.number_input("Object ID", key="object_id")
    with row1_col2:
        st.button("Inspect From Id", key="edit_object_button", on_click=get_object_data,
                  args=(st.session_state.object_id,))
        data = get_psets_from_ifc_js()
        if data:
            st.button("Inspect from Model", key="get_object_button", on_click=get_object_data,
                      args=(data['id'],)) if data else ""

    if "BIMDebugProperties" in session and session.BIMDebugProperties:
        props = session.BIMDebugProperties
        if props["attributes"]:
            st.subheader("Attributes")
            # st.table(props["attributes"])
            for prop in props["attributes"]:
                col2, col3 = st.columns([3, 3])
                if prop["int_value"]:
                    col2.text(f'🔗 {prop["name"]}')
                    col2.info(prop["string_value"])
                    col3.write("🔗")
                    col3.button("Get Object", key=f'get_object_pop_button_{prop["int_value"]}',
                                on_click=get_object_data, args=(prop["int_value"],))
                else:
                    col2.text_input(label=prop["name"], key=prop["name"], value=prop["string_value"])
                    # col3.button("Edit Object", key=f'edit_object_{prop["name"]}', on_click=edit_object_data, args=(props["active_step_id"],prop["name"]))

        if props["inverse_attributes"]:
            st.subheader("Inverse Attributes")
            for inverse in props["inverse_attributes"]:
                col1, col2, col3 = st.columns([3, 5, 8])
                col1.text(inverse["name"])
                col2.text(inverse["string_value"])
                if inverse["int_value"]:
                    col3.button("Get Object", key=f'get_object_pop_button_{inverse["int_value"]}',
                                on_click=get_object_data, args=(inverse["int_value"],))

        ## draw inverse references
        if props["inverse_references"]:
            st.subheader("Inverse References")
            for inverse in props["inverse_references"]:
                col1, col3 = st.columns([3, 3])
                col1.text(inverse["string_value"])
                if inverse["int_value"]:
                    col3.button("Get Object", key=f'get_object_pop_button_inverse_{inverse["int_value"]}',
                                on_click=get_object_data, args=(inverse["int_value"],))
#                                                                           #
#                                                                           #
# Tell streamlit that there is a component called ifc_js_viewer,            #
# and that the code to display that component is in the "frontend" folder   #
frontend_dir = (Path(__file__).parent / "frontend-viewer").absolute()  #
_component_func = components.declare_component(  #
    "ifc_js_viewer", path=str(frontend_dir)  #
)  #


#                                                                           #
# Create the python function that will be called                            #
def ifc_js_viewer(  #
        url: Optional[str] = None,  #
):  #
    component_value = _component_func(  #
        url=url,  #
    )  #
    return component_value  #


#                                                                           #
#############################################################################


def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True

    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input

def callback_upload_csv():
    pass


def main():      
    st.set_page_config(
        layout= "wide",
        page_title="Circular-Chaos",
        #page_icon="✍️",
    )
    st.title("Circular-Chaos")
    st.markdown(
    """ 
    ### Load File in the Side Bar to start
    """
    )
    ## 3d viewer

    initialise_debug_props()

    ## Adds a Logo
    st.sidebar.image('Circular-Chaos.png')


    #st.header("Viewer")
    if "ifc_file" in session and session["ifc_file"]:
        if "ifc_js_response" not in session:
            session["ifc_js_response"] = ""
        draw_3d_viewer()
        tab1 = st.tabs(["Properties"])
        # with tab1:
        test = write_pset_data()
        # with tab2:
        #   write_health_data()

    ## Add File uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    firstIFC = st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file", on_change=callback_upload)
    if firstIFC:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, firstIFC.name)
        with open(path, "wb") as f:
            f.write(firstIFC.getvalue())


    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Project successfuly loaded')
        st.sidebar.write("You can reload a new file  ")

    ## Add File uploader to Side Bar Navigation
    st.sidebar.header('List Loader')
    ListOfObjects = st.sidebar.file_uploader("Choose a file", type=['csv'], key="uploaded_csv", on_change=callback_upload_csv)


    ## Adds a field to write the name of the element to substitute
    st.sidebar.header('Object to Substitute')
    ObjectName = st.sidebar.text_input('Write the name of the object to substitute')

    ## Adds a field to write the path to save the modified IFC file
    st.sidebar.header('Path IFC')
    pathIFC = st.sidebar.text_input('Write the path to save the modified IFC')

    ##Adds a button to run Code:
    runButton = st.sidebar.button(label="RUN", key="RunButton")
    if runButton:
        # print(pd.read_csv('DataList.csv'))
        df = pd.read_csv("Datalist.csv")

        completeListParts = []
        # Create Objects acording to the list using the sortingFunctios
        for n in range(len(df.index)):
            completeListParts.append(
                sf.parts(df.iloc[n]['type'], df.iloc[n]['name'], df.iloc[n]['height'], df.iloc[n]['width'],
                         df.iloc[n]['depth'], df.iloc[n]['material'], df.iloc[n]['number'], 0,
                         df.iloc[n]['number'], 0))

        #Retrieve the Wall Data

        # Step 1: Retrieve the wall by name
        model = ifcopenshell.open(path)
        walls = model.by_type("IfcWall")
        target_wall = next((wall for wall in walls if wall.Name == ObjectName), None)

        if target_wall:
            # Get properties and quantities of the wall
            psets = ifcopenshell.util.element.get_psets(target_wall)

            # Extract Length and Height from BaseQuantities
            base_quantities = psets.get("BaseQuantities", {})
            length = float(base_quantities.get("Length", "Not available"))
            height = float(base_quantities.get("Height", "Not available"))

            print(f"Length: {length}, Height: {height}")
        else:
            print(f"No wall found with name: {ObjectName}")
            length = 0
            height = 0
        length *=100
        height *=100
        st.sidebar.write("the Length of the Wall is: "+ str(length))
        st.sidebar.write("Names of the elements used: ")
        #st.sidebar.write(height)
        #length *= 100
        #height *= 100
        # Now let us find a match for a
        sumLength = 0
        listNewElements = []
        while length > 0:
                result = sf.findMatch(length, height, completeListParts)
                for char in result:
                    length -= char.getWidth()
                    sumLength += char.getWidth()
                    listNewElements.append(char)
        if sumLength < length:
            listNewElements.pop()

        totalLength = 0
        for char in listNewElements:
            totalLength += char.getWidth()
            st.sidebar.write(char.getName())

        st.sidebar.write("The length of the Sum of reused Elements is: "+ str(totalLength))


#Code to create Walls:

        #ifc_file = ifcopenshell.open("AC20-FZK-Haus.ifc")

        wall_name_to_delete = ObjectName

        # Function to delete an existing wall by name
        def delete_existing_wall(ifc_file, wall_name_to_delete):
            for wall in ifc_file.by_type("IfcWall"):
                if wall.Name == wall_name_to_delete:
                    ifc_file.remove(wall)
                    break  # Assuming only one wall matches the criteria

        # Optionally delete an existing wall
        delete_existing_wall(model, wall_name_to_delete)

        coordinates = (0.0, 0.0, 0.0)  # starting wall
        x_dim = 5.0  # Length of the wall in meters
        y_dim = 0.1  # Thickness of the wall in meters
        depth = 2.65  # Height of the wall in meters
        lengthCoordinate = 0.0
        # Add a new wall
        for element in listNewElements:
            #CW.add_new_wall(model, coordinates, x_dim, y_dim, depth)
            totalLength += float(element.getWidth())
            CW.add_new_wall(model, coordinates, element.getWidth()/100, element.getDepth()/100, element.getHeight()/100)

        # Overwrite the IFC file with the new changes
        #model.write('ifcTest.ifc')  # This overwrites the original file
        # Example for Windows, adjust the path as necessary
        desktop_path = str(pathIFC)
        #desktop_path = r'C:\Users\mikel\Desktop\ifcTest.ifc'  # Replace 'YourUsername' with your actual username
        model.write(desktop_path)
        
        #col1, col2 = st.columns([2,1])
        #col1.subheader(f'Start Exploring "{get_project_name()}"')
        #col2.text_input("✏️ Change Project Name", key="project_name_input")
        #col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name())

    st.sidebar.write("""
    --------------
        Credits:
        Brandon Byers
        Katrin Milanzi
        Mikel Martinez
        
    
    Find the repository in: https://github.com/Mikel0M/Circular_Chaos
    
    --------------
    License: MIT
    
    """)
    st.write("")
    st.sidebar.write("")

if __name__ == "__main__":
    session = st.session_state
    main()