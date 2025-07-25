import json
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import os

def get_latest_version(package_name):
    """
    Query the NuGet Flat Container API to get the latest version for a package.
    """
    try:
        return_tuple = ()
        hasBeta = "NO"
        url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/index.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            versions = data.get("versions", [])
            if versions:
                # Iterate over the versions in reverse order (latest first)
                for version in reversed(versions):
                    if "alpha" not in version.lower() and "beta" not in version.lower() and "preview" not in version.lower():
                        return_tuple = (version, hasBeta)
                        return return_tuple
                    else:
                        hasBeta = "YES"
                # If all versions contain "alpha", return the last version
                return_tuple = (versions[-1], "YES")
                return return_tuple
    except Exception as e:
        print(f"Error fetching latest version for {package_name}: {e}")
    return None

def generate_pdf_from_sbom(json_file, output_pdf):
    output_pdf += ".pdf"
    
    # Load the SBOM JSON data.
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    components = data.get("components", [])
    
    # Prepare table header and rows.
    table_data = [["Name", "Type", "Version", "License", "Latest Version", "HasBeta"]]
    
    # Get a basic style for Paragraphs.
    styles = getSampleStyleSheet()
    cell_style = styles["BodyText"]
    name_version_dic = {}
    for comp in components:
        # Wrap the Name in a Paragraph to allow text wrapping.
        name_text = comp.get("name", "")
        name_para = Paragraph(name_text, cell_style)
        
        type_ = comp.get("type", "")
        version = comp.get("version", "")
        licenses = comp.get("licenses", [])
        if name_text not in name_version_dic.keys() or name_version_dic[name_text] != version:
            name_version_dic[name_text] = version
            # Build the License cell text.
            license_lines = []
            for lic in licenses:
                lic_expr = lic.get("expression", "").strip()
                if lic_expr.lower() == "unknown":
                    # Display unknown license in bold red.
                    formatted = "<b><font color='red'>{}</font></b>".format(lic_expr)
                else:
                    formatted = lic_expr
                license_lines.append(formatted)
            license_text = "<br/>".join(license_lines) if license_lines else ""
            license_para = Paragraph(license_text, cell_style)
            
            # Get the latest version via purl.
            purl = comp.get("purl", "")
            latest_version = ""
            hasBetaCell = ""
            if purl.startswith("pkg:nuget/"):
                try:
                    # purl format: pkg:nuget/PackageId@version
                    package_info = purl[len("pkg:nuget/"):]
                    package_id, current_version = package_info.split("@")
                    latest = get_latest_version(package_id)
                    if latest:
                        hasBetaCell = latest[1]
                        # If the current version is different from the latest, mark it in bold red.
                        if latest[0] != version:
                            latest_version = "<b><font color='red'>{}</font></b>".format(latest[0])
                        else:
                            latest_version = latest[0]
                    else:
                        latest_version = hasBetaCell ="N/A"
                except Exception as e:
                    print(f"Error processing purl {purl}: {e}")
                    latest_version = hasBetaCell = "N/A"
            else:
                latest_version = hasBetaCell = "N/A"
            latest_version_para = Paragraph(latest_version, cell_style)
            hasBetaCell_para = Paragraph(hasBetaCell, cell_style)
            
            row = [name_para, type_, version, license_para, latest_version_para, hasBetaCell_para]
            table_data.append(row)
    
    # Adjust column widths (widen the first column for text wrapping).
    col_widths = [160, 80, 80, 120, 90,50]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header row background.
        ('GRID', (0, 0), (-1, -1), 1, colors.black),          # Grid lines.
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        license_json_file = os.path.join(script_dir,  "licence.json")
        with open(
            license_json_file,
            "r", 
            encoding="utf-8"
         )as file:
            license_data = json.load(file)
    except Exception as e:
        print(f"Error loading license data: {e}")
        license_data = {}

    # Prepare License Table
    license_table_data = [["License", "Count"]]
    for license_name, count in license_data.items():
        license_table_data.append([license_name, count])

    # Define License Table
    license_table = Table(license_table_data, colWidths=[250, 100], )
    license_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    project_table_title = Paragraph("Project Dependencies", style=styles["Title"]) 
    license_table_title = Paragraph("License Occurancy", style=styles["Title"])
    
    # Build and save the PDF.
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    elements = [
        project_table_title,
        Spacer(1,10),
        table, 
        Spacer(1, 30), 
        license_table_title,
        Spacer(1, 10), 
        license_table]
    doc.build(elements)
    print("PDF generated:", output_pdf)
