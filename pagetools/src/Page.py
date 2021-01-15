from pagetools.src.utils.page_processing import string_to_coords

from typing import Dict, List
from pathlib import Path

from lxml import etree


# TODO: Replace by using PAGEPy library
class Page:
    def __init__(self, xml: Path):
        self.filename = xml
        self.tree = self.get_tree(xml)
        self.ns = self.autoextract_namespace(self.tree)

    def get_filename(self) -> Path:
        return self.filename

    @staticmethod
    def autoextract_namespace(tree: etree.Element) -> Dict[str, str]:
        """

        :param tree:
        :return:
        """
        extracted_ns = tree.xpath('namespace-uri(.)')

        if extracted_ns.startswith("http://schema.primaresearch.org/PAGE/gts/pagecontent/"):
            return {"page": extracted_ns}
        else:
            return {}

    @staticmethod
    def get_tree(file: Path) -> etree.Element:
        """

        :param file:
        :return:
        """
        try:
            return etree.parse(str(file))
        except etree.ParseError as e:
            raise e

    def get_text_lines_data(self) -> List[Dict]:
        """

        :return:
        """
        text_lines_data = []

        text_regions = self.tree.getroot().findall(".//page:TextRegion", namespaces=self.ns)

        for text_region in text_regions:
            orientation = float(text_region.attrib.get("orientation", 0))

            text_lines = self.tree.getroot().findall(".//page:TextLine", namespaces=self.ns)
            for idx, text_line in enumerate(text_lines):
                coords = text_line.find("./page:Coords", namespaces=self.ns).attrib["points"]

                text_line_data = {"id": text_line.attrib.get("id"),
                                  "orientation": orientation,
                                  "coords": string_to_coords(coords),
                                  "text_equivs": []
                                  }

                for text_equiv in text_line.findall("./page:TextEquiv", namespaces=self.ns):
                    _idx = text_equiv.attrib.get("index")
                    _content = "".join(text_equiv.find("./page:Unicode", namespaces=self.ns).itertext())
                    text_line_data["text_equivs"].append({"index": int(_idx), "content": _content})

                text_lines_data.append(text_line_data)

            return text_lines_data
