# SBOM_Visualizer
SBOM Visualizer is a lightweight Python application that parses Software Bill of Materials (SBOM) JSON files and visualizes the data both in a dynamic table and through interactive graphs. The tool displays detailed license usage statistics using bar and pie charts, making it easier for developers and managers to understand software dependencies and license distributions at a glance.


## Description
The project provides an intuitive interface built with Tkinter where users can load an SBOM JSON file. The application then populates a resizable table with parsed data, applying color-coding to highlight discrepancies between current and latest versions. In addition, it automatically generates graphs that display license usage statistics. After the SBOM .json parsing the user has the option to export the data in .pdf fromat. The tool is ideal for software projects that need to keep track of open-source license compliance and dependency management.

## Features
  - **Interactive Table**: Displays SBOM data with alternating row colors and dynamic resizing.
  - **Graph Generation**: Automatically generates bar and pie charts to visualize license usage.
  - **File Chooser**: Easily select SBOM JSON files for processing.
  - **Export PDF**: Export the SBOM data as a Table in .pdf format.

## Built With
- Python 3.13.2

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.
