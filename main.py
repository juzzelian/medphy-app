import matplotlib
matplotlib.use('Agg')  # Set the backend to Agg
import streamlit as st
import pylinac as py
from pylinac import CatPhan600
import io
import streamlit as st
from pylinac import Starshot, FieldAnalysis, WinstonLutz
import matplotlib.pyplot as plt  # Import matplotlib
import os
import zipfile
import tempfile
from io import BytesIO
from PIL import Image
import matplotlib.image as mpimg


# Set page configuration
st.set_page_config(
    page_title="Medical Physics QA Tool",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        margin: auto;
    }
    h1, h2, h3 {
        color: #2E86C1;
    }
    .stButton button {
        background-color: #2E86C1;
        color: white;
        font-weight: bold;
    }
    .stFileUploader {
        margin-bottom: 20px;
    }
    .stMarkdown {
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Initialize session state
if 'file_location' not in st.session_state:
    st.session_state.file_location = None
if 'catphan_location' not in st.session_state:
    st.session_state.catphan_location = None
if 'spoke_location' not in st.session_state:
    st.session_state.spoke_location = None
if 'wlt_location' not in st.session_state:
    st.session_state.wlt_location = None
if 'final_field_file_name' not in st.session_state:
    st.session_state.final_field_file_name = "field_analysis.pdf"
if 'final_spoke_file_name' not in st.session_state:
    st.session_state.final_spoke_file_name = "spoke_analysis.pdf"
if 'final_wlt_file_name' not in st.session_state:
    st.session_state.final_wlt_file_name = "wlt_analysis.pdf"
if 'final_catphan_file_name' not in st.session_state:
    st.session_state.final_catphan_file_name = "catphan_analysis.pdf"

# Title
st.title("Medical Physics QA Analysis Tools")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["X-ray Field Analysis", "Spoke Analysis", "WLT Analysis", "CatPhan Analysis", "About"])

# Field Analysis Tab
with tab1:

# Header and example image
    st.header("X-Ray Field Analysis")
    st.image("appimages/field_analyze.png", caption="Field Analysis Example", width=500)  # Add corresponding image


# File uploader
    st.session_state.file_location = st.file_uploader("UPLOAD FIELD DICOM FILE", type=["dcm"], key="field_upload")
    st.session_state.final_field_file_name = st.text_input("Enter Field PDF File Name", value="field_analysis.pdf", key="field_name")

# Analyze button
    if st.button("Analyze Field Congruence", key="field_button"):
        if st.session_state.file_location:
        # Save the uploaded DICOM file to a temporary file
            with open("temp_field.dcm", "wb") as f:
                f.write(st.session_state.file_location.getbuffer())

        # Perform analysis
            my_img = py.FieldAnalysis(path="temp_field.dcm")
            my_img.analyze()

        # Display results
            st.subheader("Results")
            st.subheader("A. Xray Field Size")
            st.write(f"&emsp;&emsp;**Vertical Field Size (cm):** {my_img.results_data().field_size_vertical_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Horizontal Field Size (cm):** {my_img.results_data().field_size_horizontal_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Beam Center to Top Edge (cm):** {my_img.results_data().beam_center_to_top_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Beam Center to Bottom Edge (cm):** {my_img.results_data().beam_center_to_bottom_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Beam Center to Left Edge (cm):** {my_img.results_data().beam_center_to_left_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Beam Center to Right Edge (cm):** {my_img.results_data().beam_center_to_right_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Central Axis to Top Edge (cm):** {my_img.results_data().cax_to_top_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Central Axis to Bottom Edge (cm):** {my_img.results_data().cax_to_bottom_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Central Axis to Left Edge (cm):** {my_img.results_data().cax_to_left_mm / 10.0:.2f}")
            st.write(f"&emsp;&emsp;**Distance from Central Axis to Right Edge (cm):** {my_img.results_data().cax_to_right_mm / 10.0:.2f}")
            st.subheader("B. Flatness and Symmetry")
            st.write(f"&emsp;&emsp;**Horizontal Symmetry (%):** {my_img.results_data().protocol_results['symmetry_horizontal']:.2f}")
            st.write(f"&emsp;&emsp;**Vertical Symmetry (%):** {my_img.results_data().protocol_results['symmetry_vertical']:.2f}")
            st.write(f"&emsp;&emsp;**Horizontal Flatness (%):** {my_img.results_data().protocol_results['flatness_horizontal']:.2f}")
            st.write(f"&emsp;&emsp;**Vertical Flatness (%):** {my_img.results_data().protocol_results['flatness_vertical']:.2f}")

        # Save the analyzed image to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_image_file:
                temp_image_path = temp_image_file.name
                my_img.save_analyzed_image(filename=temp_image_path)

            # Display the saved image using st.image()
                st.image(temp_image_path, caption="Field Size Analysis Image", use_container_width=False)

            # Generate PDF report
            pdf_buffer = io.BytesIO()
            my_img.publish_pdf(pdf_buffer)
            st.session_state.field_pdf = pdf_buffer.getvalue()

        # Clean up temporary files
            os.remove("temp_field.dcm")
            os.remove(temp_image_path)

            st.success("Field analysis completed.")
        else:
            st.error("Error: No field file uploaded.")

# Download PDF button
    if 'field_pdf' in st.session_state:
        st.download_button(
            label="Download Field Analysis Report",
            data=st.session_state.field_pdf,
            file_name=st.session_state.final_field_file_name,
            mime="application/pdf",
            key="field_download"
        )

# Spoke Analysis Tab
with tab2:
    st.header("Spokeshot Analysis Test")
    st.image("appimages/spoke_shot.png", caption="Spokeshot Analysis", width=600)  # Add corresponding image
    st.session_state.spoke_location = st.file_uploader("Upload Spoke Image File", type=["png", "jpg", "jpeg"], key="spoke_upload")
    st.session_state.final_spoke_file_name = st.text_input("Enter Spoke Output File Name", value="spoke_analysis.pdf", key="spoke_name")
    if st.button("Spokeshot Analysis", key="spoke_button"):
        if st.session_state.spoke_location:
            with open("temp_spoke.png", "wb") as f:
                f.write(st.session_state.spoke_location.getbuffer())
            mystar = py.Starshot("temp_spoke.png", sid=1000)
            mystar.analyze(radius=0.95, tolerance=2.0)

            st.subheader("Spokeshot Results")
            st.write(f"&emsp;&emsp;**Maximum Diameter of the Circle (mm):** {mystar.results_data().circle_diameter_mm:.2f}")
            st.write(f"&emsp;&emsp;**Tolerance (mm):** {mystar.results_data().tolerance_mm:.2f}")
            if mystar.results_data().circle_diameter_mm <= mystar.results_data().tolerance_mm:
                st.success("**PASS!**")
            else:
                st.error("**FAIL!**")

            #saving the save_analyze_image into a temporary file to be used for showing later
            # Save the analyzed image to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_image_file:
                temp_image_path = temp_image_file.name
                mystar.save_analyzed_image(filename=temp_image_path)

            # Display the saved image using st.image()
                st.image(temp_image_path, caption="Spoke Shot Analysis", use_container_width=False)

            #saving the pdf bytes into pdf_buffer
            pdf_buffer = io.BytesIO()
            mystar.publish_pdf(pdf_buffer)
            st.session_state.spoke_pdf = pdf_buffer.getvalue()

            st.success("Spoke analysis completed.")
            os.remove("temp_spoke.png")
        else:
            st.error("Error: No spoke file uploaded.")
    if 'spoke_pdf' in st.session_state:
        st.download_button(
            label="Download Spoke Analysis PDF",
            data=st.session_state.spoke_pdf,
            file_name=st.session_state.final_spoke_file_name,
            mime="application/pdf",
            key="spoke_download"
        )

# WLT Analysis Tab
with tab3:
    st.header("WINSTON-LUTZ TEST")
    
    st.image("appimages/wlt_img.png", caption="Winston-Lutz Analysis", width=500)  # Add corresponding image

    #Select the equipment
    st.write("If using dicom files not acquired from Varian LINACS, ensure that dicom filename indicate acquisition settings")
    machine_type = st.radio("Select the machine type:", ("Varian","Elekta"))


    st.session_state.wlt_location = st.file_uploader("Upload WLT DICOM Folder", type=["dcm","zip"], accept_multiple_files=True, key="wlt_upload")
    
    st.session_state.final_wlt_file_name = st.text_input("Enter WLT Output File Name", value="wlt_analysis.pdf", key="wlt_name")
    if st.button("WLT Analysis", key="wlt_button"):
        if st.session_state.wlt_location:
            os.makedirs("temp_wlt", exist_ok=True)
            for file in st.session_state.wlt_location:
                with open(f"temp_wlt/{file.name}", "wb") as f:
                    f.write(file.getbuffer())
            #Initialize WinstonLutz based on selected machine type

            if machine_type=="Varian":
                wlt = WinstonLutz("temp_wlt")
            elif machine_type=="Elekta":
                wlt = WinstonLutz("temp_wlt",use_filenames=True)
            wlt.analyze()
                
            saved_images = []
            # Generate and save plots
            for i in range(len(st.session_state.wlt_location)):
                # Create a new figure for each plot
                plt.figure()
                wlt.images[i].plot()  # Generate the plot (assuming this method exists)
                plt.title(f"Image {i+1}")  # Optional: Add a title to the plot
                        
                # Save the plot to a buffer
                buf = BytesIO()
                plt.savefig(buf, format='png')  # Save the plot to the buffer
                buf.seek(0)  # Rewind the buffer
                img_test = Image.open(buf)  # Open the buffer as a PIL image
                saved_images.append(img_test)  # Save the image to the list
                        
                plt.close()  # Close the plot to free up memory

                    # Display the saved images in Streamlit
            st.write(f"Total plots generated: {len(saved_images)}")

            # Display the saved images in a grid (5 images per row)
            num_cols = 5  # Number of columns in the grid
            cols = st.columns(num_cols)  # Create columns

            for i, img in enumerate(saved_images):
                with cols[i % num_cols]:  # Cycle through the columns
                    st.image(img, caption=f"Plot {wlt.images[i]}", use_container_width=True)
            
            # Display results
            st.subheader("Results")
            st.markdown(f"&emsp;&emsp;**Maximum 2D CAX-to-BB Distance (mm):** {wlt.results_data(as_dict=True)['max_2d_cax_to_bb_mm']:.2f}")
            st.write(f"&emsp;&emsp;**Gantry 3D Isocenter Deviation (mm):** {wlt.results_data(as_dict=True)['gantry_3d_iso_diameter_mm']:.2f}")
            st.write(f"&emsp;&emsp;**Collimator 2D Isocenter Deviation (mm):** {wlt.results_data(as_dict=True)['coll_2d_iso_diameter_mm']:.2f}")
            st.write(f"&emsp;&emsp;**Couch 2D Isocenter Deviation (mm):** {wlt.results_data(as_dict=True)['couch_2d_iso_diameter_mm']:.2f}")

            pdf_buffer = io.BytesIO()
            wlt.publish_pdf(pdf_buffer)
            st.session_state.wlt_pdf = pdf_buffer.getvalue()
            pdf_buffer.close()
            st.success("WLT analysis completed.")

            for file in os.listdir("temp_wlt"):
                os.remove(f"temp_wlt/{file}")
            os.rmdir("temp_wlt")
        else:
            st.error("Error: No WLT files uploaded.")
    if 'wlt_pdf' in st.session_state:
        st.download_button(
            label="Download WLT Analysis PDF",
            data=st.session_state.wlt_pdf,
            file_name=st.session_state.final_wlt_file_name,
            mime="application/pdf",
            key="wlt_download"
        )

# CatPhan Analysis Tab
with tab4:
    # Header and example image
    st.header("CatPhan CT/CBCT Analysis")
    st.image("appimages/catphan_logo.png", caption="CatPhan CT/CBCT Analysis", width=800)  # Add corresponding image

    st.session_state.catphan_location = st.file_uploader("Upload CatPhan DICOM Folder", type=["dcm","zip"], accept_multiple_files=True, key="catphan_upload")
    st.session_state.final_catphan_file_name = st.text_input("Enter CatPhan Output File Name", value="catphan_analysis.pdf", key="catphan_name")

    if st.button("CatPhan Analysis", key="catphan_button"):
        if st.session_state.catphan_location:
            os.makedirs("temp_catphan", exist_ok=True)
            for file in st.session_state.catphan_location:
                with open(f"temp_catphan/{file.name}", "wb") as f:
                    f.write(file.getbuffer())
                
            # Perform analysis
            mycbct = CatPhan600("temp_catphan")
            mycbct.analyze()
            results = mycbct.results_data(as_dict=True)
            

            #Catphan600 inserts
            air_roi_data = results['ctp404']['hu_rois']['Air']
            pmp_roi_data = results['ctp404']['hu_rois']['PMP']
            ldpe_roi_data = results['ctp404']['hu_rois']['LDPE']
            poly_roi_data = results['ctp404']['hu_rois']['Poly']
            acrylic_roi_data = results['ctp404']['hu_rois']['Acrylic']
            delrin_roi_data = results['ctp404']['hu_rois']['Delrin']
            teflon_roi_data = results['ctp404']['hu_rois']['Teflon']
            water_roi_data = results['ctp404']['hu_rois']['Vial']

            #Air Data
            air_mean_hu = air_roi_data['value']
            air_std = air_roi_data['stdev']
            air_nom_value = air_roi_data['nominal_value']
            air_pass_fail = air_roi_data['passed']

            #pmp
            pmp_mean_hu = pmp_roi_data['value']
            pmp_std = pmp_roi_data['stdev']
            pmp_nom_value = pmp_roi_data['nominal_value']
            pmp_pass_fail = pmp_roi_data['passed']

            #LDPE
            ldpe_mean_hu = ldpe_roi_data['value']
            ldpe_std = ldpe_roi_data['stdev']
            ldpe_nom_value = ldpe_roi_data['nominal_value']
            ldpe_pass_fail = ldpe_roi_data['passed']

            #Delrin
            delrin_mean_hu = delrin_roi_data['value']
            delrin_std = delrin_roi_data['stdev']
            delrin_nom_value = delrin_roi_data['nominal_value']
            delrin_pass_fail = delrin_roi_data['passed']

            #teflon
            teflon_mean_hu = teflon_roi_data['value']
            teflon_std = teflon_roi_data['stdev']
            teflon_nom_value = teflon_roi_data['nominal_value']
            teflon_pass_fail = teflon_roi_data['passed']

            #polystyrene
            poly_mean_hu = poly_roi_data['value']
            poly_std = poly_roi_data['stdev']
            poly_nom_value = poly_roi_data['nominal_value']
            poly_pass_fail = poly_roi_data['passed']

            #acrylic
            acrylic_mean_hu = acrylic_roi_data['value']
            acrylic_std = acrylic_roi_data['stdev']
            acrylic_nom_value = acrylic_roi_data['nominal_value']
            acrylic_pass_fail = acrylic_roi_data['passed']

            #water
            water_mean_hu = water_roi_data['value']
            water_std = water_roi_data['stdev']
            water_nom_value = water_roi_data['nominal_value']
            water_pass_fail = water_roi_data['passed']

            #Slice Thickness Results
            slice_thickness_results = results['ctp404']['measured_slice_thickness_mm']

            #HU Linearity
            hu_linearity_test = results['ctp404']['hu_linearity_passed']

            #Geometric Accuracy
            geometric_accuracy_test = results['ctp404']['geometry_passed']

            #CT Uniformity
            nps_avg_pwr = results['ctp486']['nps_avg_power']
            nps_max_frequency = results['ctp486']['nps_max_freq']
            uniformity_index = results['ctp486']['uniformity_index']

            top_rois_data = results['ctp486']['rois']['Top']
            right_rois_data = results['ctp486']['rois']['Right']
            left_rois_data = results['ctp486']['rois']['Left']
            center_rois_data = results['ctp486']['rois']['Center']
            bottom_rois_data = results['ctp486']['rois']['Bottom']

            #Uniformity Values
            top_mean_hu = top_rois_data['value']
            top_stdev = top_rois_data['stdev']
            right_mean_hu = right_rois_data['value']
            right_stdev = right_rois_data['stdev']
            bottom_mean_hu = bottom_rois_data['value']
            bottom_stdev = bottom_rois_data['stdev']
            left_mean_hu = left_rois_data['value']
            left_stdev = left_rois_data['stdev']
            center_mean_hu = center_rois_data['value']
            center_stdev = center_rois_data['stdev']

            #Spatial Resolution
            mtf_10 = results['ctp528']['mtf_lp_mm']['10']
            mtf_30 = results['ctp528']['mtf_lp_mm']['30']
            mtf_50 = results['ctp528']['mtf_lp_mm']['50']

            # Save the analyzed image to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_image_file:
                temp_image_path = temp_image_file.name
                mycbct.save_analyzed_image(filename=temp_image_path)

                # Display the saved image using st.image()
                st.image(temp_image_path, caption="CatPhan Analysis Image", use_container_width=False)


            # Display results
            st.subheader("CatPhan Inserts, CT HU Linearity and Constancy")
            st.write(f"&emsp;&emsp;&emsp;**Air Mean (HU):** {air_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**PMP Mean (HU):** {pmp_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**LDPE Mean (HU):** {ldpe_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Polystyrene Mean (HU):** {poly_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Acrylic Mean (HU):** {acrylic_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Delrin Mean (HU):** {delrin_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Teflon Mean (HU):** {teflon_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Water Mean (HU):** {water_mean_hu:.2f}")
        
            if hu_linearity_test:
                st.write("&emsp;&emsp;&emsp;**HU LINEARITY TEST: PASS**")
            else:
                st.write("&emsp;&emsp;&emsp;**HU LINEARITY TEST: FAIL**")

            
            st.subheader("Slice Thickness and Geometric Accuracy")
            """

            """
            st.write(f"&emsp;&emsp;&emsp;**Measured Slice Thickness:** {slice_thickness_results:.1f}")
            if geometric_accuracy_test:
                st.write("&emsp;&emsp;&emsp;**GEOMETRIC ACCURACY TEST: PASS**")
            else:
                st.write("&emsp;&emsp;&emsp;**GEOMETRIC ACCURACY TEST: FAIL**")

            st.subheader("CT UNIFORMITY")
            """
            """
            st.write(f"&emsp;&emsp;&emsp;**Average Noise Power Spectrum:** {nps_avg_pwr:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Noise Power Spectrum Maximum Frequency:** {nps_max_frequency:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Uniformity Index:** {uniformity_index:.2f}")
            
            st.write(f"&emsp;&emsp;&emsp;**Center Mean HU:** {center_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Center Noise:** {center_stdev:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Top Mean HU:** {top_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Right Mean HU:** {right_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Bottom Mean HU:** {bottom_mean_hu:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**Left Mean HU:** {left_mean_hu:.2f}")

            st.subheader("CT SPATIAL RESOLUTION")
            
            st.write(f"&emsp;&emsp;&emsp;**MTF10 (lp/cm):** {mtf_10*10:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**MTF30 (lp/cm):** {mtf_30*10:.2f}")
            st.write(f"&emsp;&emsp;&emsp;**MTF50 (lp/cm):** {mtf_50*10:.2f}")
            
            # Generate PDF report
            pdf_buffer = io.BytesIO()
            mycbct.publish_pdf(pdf_buffer)
            st.session_state.catphan_pdf = pdf_buffer.getvalue()
            pdf_buffer.close()

            st.success("CatPhan analysis completed.")
            for file in os.listdir("temp_catphan"):
                os.remove(f"temp_catphan/{file}")
            os.rmdir("temp_catphan")

        else:
                st.error("Error: No field file uploaded.")

    # Download PDF button
    if 'catphan_pdf' in st.session_state:
        st.download_button(
            label="Download CatPhan Analysis PDF",
            data=st.session_state.catphan_pdf,
            file_name=st.session_state.final_catphan_file_name,
            mime="application/pdf",
            key="catphan_download"
            )

# About Tab
with tab5:
        

    # Title and Introduction
    st.title("Medical Physics QA Analysis Tools")
    st.markdown("""
    Welcome to the **Medical Physics QA Analysis Tools**, a comprehensive suite designed to streamline and automate quality assurance (QA) processes in medical physics. 
    These tools are built to assist medical physicists, radiation therapists, and QA professionals in performing critical tests to ensure the accuracy, safety, and efficiency of radiation therapy and imaging systems.
    """)

    # Tests Overview
    st.header("Tests Included")
    st.markdown("""
    The following tests are included in this suite:
    1. **Winston-Lutz Test**
    2. **Spokeshot Test**
    3. **Field Analysis**
    4. **Flatness and Symmetry Analysis**
    5. **Catphan CT Imaging Tests**
    """)

    # Test Details
    st.header("Test Details")

    ### Winston-Lutz Test
    st.markdown("""
    #### **Winston-Lutz Test**
    The **Winston-Lutz Test** is used to verify the alignment of the radiation isocenter with the mechanical isocenter of a linear accelerator (linac). This test ensures that the radiation beam is accurately targeted at the intended location, which is critical for precise radiation therapy.

    - **Key Metrics**:
    - Maximum 2D CAX-to-BB distance (mm)
    - Gantry 3D isocenter deviation (mm)
    - Collimator 2D isocenter deviation (mm)
    - Couch 2D isocenter deviation (mm)

    - **Documentation**: [pylinac Winston-Lutz Documentation](https://pylinac.readthedocs.io/en/latest/winston_lutz.html)
    """)

    ### Spokeshot Test
    st.markdown("""
    #### **Spokeshot Test**
    The **Spokeshot Test** is used to evaluate the alignment of the radiation beam with the gantry rotation axis. This test is particularly useful for checking the consistency of the beam's alignment across different gantry angles.

    - **Key Metrics**:
    - Beam center deviation (mm)
    - Gantry angle accuracy (degrees)

    - **Documentation**: [pylinac Spokeshot Documentation](https://pylinac.readthedocs.io/en/latest/spokeshot.html)
    """)

    ### Field Analysis
    st.markdown("""
    #### **Field Analysis**
    **Field Analysis** is performed to assess the congruence of the radiation field with the imaging field. This test ensures that the radiation field matches the imaging field, which is essential for accurate treatment planning and delivery.

    - **Key Metrics**:
    - Vertical field size (cm)
    - Horizontal field size (cm)
    - Beam center to edge distances (cm)
    - Symmetry and flatness (%)

    - **Documentation**: [pylinac Field Analysis Documentation](https://pylinac.readthedocs.io/en/latest/field_analysis.html)
    """)

    ### Flatness and Symmetry Analysis
    st.markdown("""
    #### **Flatness and Symmetry Analysis**
    The **Flatness and Symmetry Analysis** evaluates the uniformity of the radiation beam across the field. Flatness measures the uniformity of the dose profile, while symmetry measures the balance of the dose distribution.

    - **Key Metrics**:
    - Flatness (%)
    - Symmetry (%)

    - **Documentation**: [pylinac Flatness and Symmetry Documentation](https://pylinac.readthedocs.io/en/latest/flatness_symmetry.html)
    """)

    ### Catphan CT Imaging Tests
    st.markdown("""
    #### **Catphan CT Imaging Tests**
    The **Catphan CT Imaging Tests** are used to evaluate the performance of CT imaging systems. These tests assess various aspects of image quality, including spatial resolution, contrast resolution, and uniformity.

    - **Key Metrics**:
    - Spatial resolution (lp/cm)
    - Contrast-to-noise ratio (CNR)
    - Uniformity (%)

    - **Documentation**: [pylinac Catphan Documentation](https://pylinac.readthedocs.io/en/latest/catphan.html)
    """)

    # Features
    st.header("Features of the QA Analysis Tools")
    st.markdown("""
    - **Automated Analysis**: The tools automate the analysis process, reducing manual effort and minimizing human error.
    - **Comprehensive Reporting**: Detailed reports are generated for each test, including key metrics, plots, and visualizations.
    - **User-Friendly Interface**: The tools are designed with a user-friendly interface, making them accessible to both novice and experienced users.
    - **Integration with pylinac**: The tools leverage the **pylinac** module, ensuring accurate and reliable results.
    """)

    # How to Use
    st.header("How to Use the Tools")
    st.markdown("""
    1. **Upload Data**: Upload the required DICOM files or images for the specific test.
    2. **Run Analysis**: Click the "Analyze" button to perform the test.
    3. **View Results**: Review the results, including key metrics and visualizations.
    4. **Download Report**: Download a comprehensive PDF report for documentation and further analysis.
    """)

    # Documentation and Support
    st.header("Documentation and Support")
    st.markdown("""
    For detailed documentation on each test and its implementation, refer to the **pylinac module documentation**:
    - [pylinac Documentation](https://pylinac.readthedocs.io/en/latest/)

    For support or additional questions, please contact the development team or refer to the official pylinac GitHub repository:
    - [pylinac GitHub Repository](https://github.com/jrkerns/pylinac)
    """)

    # About the Creator
    st.header("About the Creator")
    st.image("appimages/jibz_img.png", caption="Juzzel Ian B. Zerrudo, MSc, CMP-ROMP", width=300)  # Add corresponding image
    st.markdown("""
    Developed by **Juzzel Ian Zerrudo**, to provide an easy-to-use application for analyzing common Medical Physics QA tests, using the **Python** and the **pylinac library**.
    """)

    # Disclaimer
    st.header("Disclaimer")
    st.markdown("""
    While every effort has been made to ensure the accuracy and reliability of these tools, **no warranty** is provided. 
    Users are encouraged to verify the results of their tests independently. The creator and contributors are not liable for any errors, omissions, or consequences arising from the use of these tools.
    """)


# Footer
st.markdown("---")
st.write("developed by: jibzerrudo")