# medphy-app

Medical Physics QA Analysis Tools
Welcome to the Medical Physics QA Analysis Tools, a comprehensive suite designed to streamline and automate quality assurance (QA) processes in medical physics. These tools are built to assist medical physicists, radiation therapists, and QA professionals in performing critical tests to ensure the accuracy, safety, and efficiency of radiation therapy and imaging systems.

Tests Included
The following tests are included in this suite:

Winston-Lutz Test
Spokeshot Test
Field Analysis
Flatness and Symmetry Analysis
Catphan CT Imaging Tests
Test Details
Winston-Lutz Test
The Winston-Lutz Test is used to verify the alignment of the radiation isocenter with the mechanical isocenter of a linear accelerator (linac). This test ensures that the radiation beam is accurately targeted at the intended location, which is critical for precise radiation therapy.

Key Metrics:

Maximum 2D CAX-to-BB distance (mm)

Gantry 3D isocenter deviation (mm)

Collimator 2D isocenter deviation (mm)

Couch 2D isocenter deviation (mm)

Documentation: pylinac Winston-Lutz Documentation

Spokeshot Test
The Spokeshot Test is used to evaluate the alignment of the radiation beam with the gantry rotation axis. This test is particularly useful for checking the consistency of the beam's alignment across different gantry angles.

Key Metrics:

Beam center deviation (mm)

Gantry angle accuracy (degrees)

Documentation: pylinac Spokeshot Documentation

Field Analysis
Field Analysis is performed to assess the congruence of the radiation field with the imaging field. This test ensures that the radiation field matches the imaging field, which is essential for accurate treatment planning and delivery.

Key Metrics:

Vertical field size (cm)

Horizontal field size (cm)

Beam center to edge distances (cm)

Symmetry and flatness (%)

Documentation: pylinac Field Analysis Documentation

Flatness and Symmetry Analysis
The Flatness and Symmetry Analysis evaluates the uniformity of the radiation beam across the field. Flatness measures the uniformity of the dose profile, while symmetry measures the balance of the dose distribution.

Key Metrics:

Flatness (%)

Symmetry (%)

Documentation: pylinac Flatness and Symmetry Documentation

Catphan CT Imaging Tests
The Catphan CT Imaging Tests are used to evaluate the performance of CT imaging systems. These tests assess various aspects of image quality, including spatial resolution, contrast resolution, and uniformity.

Key Metrics:

Spatial resolution (lp/cm)

Contrast-to-noise ratio (CNR)

Uniformity (%)

Documentation: pylinac Catphan Documentation

Features of the QA Analysis Tools
Automated Analysis: The tools automate the analysis process, reducing manual effort and minimizing human error.
Comprehensive Reporting: Detailed reports are generated for each test, including key metrics, plots, and visualizations.
User-Friendly Interface: The tools are designed with a user-friendly interface, making them accessible to both novice and experienced users.
Integration with pylinac: The tools leverage the pylinac module, ensuring accurate and reliable results.
How to Use the Tools
Upload Data: Upload the required DICOM files or images for the specific test.
Run Analysis: Click the "Analyze" button to perform the test.
View Results: Review the results, including key metrics and visualizations.
Download Report: Download a comprehensive PDF report for documentation and further analysis.
Documentation and Support
For detailed documentation on each test and its implementation, refer to the pylinac module documentation:

pylinac Documentation
For support or additional questions, please contact the development team or refer to the official pylinac GitHub repository:

pylinac GitHub Repository

Developed by Juzzel Ian Zerrudo, to provide an easy-to-use application for analyzing common Medical Physics QA tests, using the Python and the pylinac library.

Disclaimer
While every effort has been made to ensure the accuracy and reliability of these tools, no warranty is provided. Users are encouraged to verify the results of their tests independently. The creator and contributors are not liable for any errors, omissions, or consequences arising from the use of these tools.
