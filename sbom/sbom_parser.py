import json
import requests
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

def format_license(licenses):
    """
    Checks and formats license data and returns a plain text string.
    """
    license_lines = []
    for lic in licenses:
        lic_expr = lic.get("expression", "").strip()
        if lic_expr.lower() == "unknown":
            # Mark "unknown" in uppercase (or use any marker you prefer)
            formatted = lic_expr.upper()
        else:
            formatted = lic_expr
        license_lines.append(formatted)
    # Join multiple license lines with a newline
    license_text = "\n".join(license_lines) if license_lines else ""
    return license_text

def process_component(comp, name_version_dic, licence_dic):
    """
    Processes a component and returns a row as a list of plain text strings.
    """
    name_text = comp.get("name", "")
    # Use plain text for the name
    name_plain = name_text
    
    type_ = comp.get("type", "")
    version = comp.get("version", "")
    licenses = comp.get("licenses", [])

    # Avoid duplicate entries if the same component (name) with the same version exists
    if name_text in name_version_dic and name_version_dic[name_text] == version:
        return None
    name_version_dic[name_text] = version
    
    # Update licence dictionary based on the first license entry (if available)
    if licenses:
        key = list(licenses[0].values())[0]
        licence_dic[key] = licence_dic.get(key, 0) + 1

    license_plain = format_license(licenses)
    
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
                # Highlight if current version is different from the latest (using simple text markup)
                if latest[0] != version:
                    latest_version = latest[0]
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
    
    # Build the row as a list of plain text strings
    row = [name_plain, type_, version, license_plain, latest_version, hasBetaCell]
    return row

def get_table_rows(json_file):
    """
    Reads the SBOM JSON file and returns a list of rows for the table.
    The first row is the header.
    
    :return: List of rows (each row is a list of plain text strings).
    """
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    components = data.get("components", [])
    
    table_data = []
    name_version_dic = {}
    licence_dic = {}
    for comp in components:
        row = process_component(comp, name_version_dic, licence_dic)
        if row:
            table_data.append(row)
    
    write_licence_json(licence_dic)
    
    return table_data

def write_licence_json(licence_dic):
    licence_json = json.dumps(licence_dic, indent=2)
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'licence.json')
    with open(file_path, 'w') as f:
        f.write(licence_json)
