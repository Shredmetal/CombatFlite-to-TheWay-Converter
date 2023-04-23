import zipfile
import xml.etree.ElementTree as ET
import xmltodict

class CombatFliteReader:

    def unzipper(self, file_path: str):

        with zipfile.ZipFile(f'CF_File/{file_path}.cf') as zip_ref:
            zip_ref.extractall("Extracted_CF")

    def xml_parser(self):

        tree = ET.parse(f'Extracted_CF/mission.xml')
        myroot = tree.getroot()
        xmlstr = ET.tostring(myroot, encoding='utf-8', method='xml')
        data_dict = dict(xmltodict.parse(xmlstr))
        return data_dict
