import csv
import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

import common as cm

COMMON_PATH = f"{cm.PROJECT_PATH}/client"


def generate_xml_for_csv(client_name):
    path = f"{COMMON_PATH}/{client_name}/models"
    csv_files = [file for file in os.listdir(path + "/local") if file.endswith('.csv')]

    for csv_file in csv_files:
        name = csv_file.split('.csv')[0]
        # Read the CSV file
        with open(f"{path}/local/{csv_file}", 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Get the headers of the CSV

        # Create the root element
        root = Element("table", name=f"{client_name}.{name}", dataSource="DS1", handler="import-script.sb")

        # Iterate over the headers and create the XML structure
        for index, header in enumerate(headers):
            # Create column element with attributes
            column = SubElement(root, "column", key="true" if index == 0 else "false", type="primitive")

            # Create source and target elements
            _ = SubElement(column, "source", name=header, type="float32")
            _ = SubElement(column, "target", name=header, type="float32")

        # Convert the XML structure to string
        xml_string = parseString(tostring(root)).toprettyxml(indent="    ")

        # Write the XML content to a file
        with open(f"{COMMON_PATH}/{client_name}/importer/{name}.xml", 'w') as xml_file:
            xml_file.write(xml_string)

        # Also create a log file
        with open(f"{COMMON_PATH}/{client_name}/importer/{name}.log", 'w') as log_file:
            log_file.write("")


if __name__ == "__main__":
    client_number = cm.CLIENT_NUMBER
    client_name = cm.CLIENT_NAME
    generate_xml_for_csv(client_name)
