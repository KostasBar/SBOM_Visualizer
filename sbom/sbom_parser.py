import json
import requests
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from collections import Counter
import os

def get_latest_version(package_name):
    """
    Returns a tuple (latest_version, hasBeta) for the NuGet Package.
    """
    try:
        hasBeta = "NO"
        url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/index.json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            versions = data.get("versions", [])
            if versions:
                # Check versions from the last to the first.
                for version in reversed(versions):
                    if ("alpha" not in version.lower() and
                        "beta" not in version.lower() and
                        "preview" not in version.lower()):
                        return (version, hasBeta)
                    else:
                        hasBeta = "YES"
                # If all versions contain "alpha"/"beta"/"preview", return the last one.
                return (versions[-1], "YES")
    except Exception as e:
        print(f"Error fetching latest version for {package_name}: {e}")
    return None

def format_license(licenses, cell_style):
    """
    Checks and formats license. Then returns a Paragraph for the cell.
    """
    license_lines = []
    for lic in licenses:
        lic_expr = lic.get("expression", "").strip()
        if lic_expr.lower() == "unknown":
            formatted = "<b><font color='red'>{}</font></b>".format(lic_expr)
        else:
            formatted = lic_expr
        license_lines.append(formatted)
    license_text = "<br/>".join(license_lines) if license_lines else ""
    return Paragraph(license_text, cell_style)

def process_component(comp, name_version_dic, cell_style, licence_dic):
    """
    Processes a component and returns a row.
    """
    name_text = comp.get("name", "")
    # Create Paragraph for text wrapping.
    name_para = Paragraph(name_text, cell_style)
    
    type_ = comp.get("type", "")
    version = comp.get("version", "")
    licenses = comp.get("licenses", [])

    if name_text in name_version_dic and name_version_dic[name_text] == version:
        return None
    name_version_dic[name_text] = version
    
    if len(licenses) > 0:
        key = list(licenses[0].values())[0]
        licence_dic[key] = licence_dic.get(key, 0) + 1

    license_para = format_license(licenses, cell_style)
    
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
                # Highlight if current version is different from the latest
                if latest[0] != version:
                    latest_version = "<b><font color='red'>{}</font></b>".format(latest[0])
                else:
                    latest_version = latest[0]
            else:
                latest_version = "N/A"
                hasBetaCell = "N/A"
        except Exception as e:
            print(f"Error processing purl {purl}: {e}")
            latest_version = "N/A"
            hasBetaCell = "N/A"
    else:
        latest_version = "N/A"
        hasBetaCell = "N/A"
    
    latest_version_para = Paragraph(latest_version, cell_style)
    hasBetaCell_para = Paragraph(hasBetaCell, cell_style)
    
    row = [name_para, type_, version, license_para, latest_version_para, hasBetaCell_para]
    return row

def get_table_rows(json_file):
    """
    Reads the SBOM JSON file and returns a list of rows for the table.
    The first row is the header.
    
    :return: List of rows (each row is a list of cell objects).
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    components = data.get("components", [])
    
    table_data = []
    styles = getSampleStyleSheet()
    cell_style = styles["BodyText"]
    
    name_version_dic = {}
    licence_dic = {}
    for comp in components:
        row = process_component(comp, name_version_dic, cell_style, licence_dic)
        if row:
            table_data.append(row)
    
    # Optionally, write the license dictionary to a file.
    write_licence_json(licence_dic)
    
    return table_data

def write_licence_json(licence_dic):
    licence_json = json.dumps(licence_dic, indent=2)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'licence.json')
    with open(file_path, 'w') as f:
        f.write(licence_json)
