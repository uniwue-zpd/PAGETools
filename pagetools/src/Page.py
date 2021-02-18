from pagetools.src.utils.page_processing import string_to_coords

from typing import Dict, List, Set
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

    def get_ns(self) -> Dict[str, str]:
        return self.ns

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

    def get_element_data(self, element_types: Set[str]) -> List[Dict]:
        element_data = []

        for element_type in element_types:
            element_regions = self.tree.getroot().findall(f".//page:{element_type}", namespaces=self.ns)

            for region in element_regions:
                if element_type == "TextLine":
                    orientation = float(region.getparent().attrib.get("orientation", 0))
                else:
                    orientation = float(region.attrib.get("orientation", 0))

                coords = region.find("./page:Coords", namespaces=self.ns).attrib["points"]

                text_line_data = {"id": region.attrib.get("id"),
                                  "orientation": orientation,
                                  "coords": string_to_coords(coords),
                                  "text_equivs": []
                                  }

                text_equivs = region.findall("./page:TextEquiv", namespaces=self.ns)
                if len(text_equivs) > 0:
                    for text_equiv in text_equivs:
                        idx = text_equiv.attrib.get("index")
                        content = "".join(text_equiv.find("./page:Unicode", namespaces=self.ns).itertext())
                        text_line_data["text_equivs"].append({"index": idx, "content": content})

                element_data.append(text_line_data)

        return element_data

    def get_texts(self) -> List[etree.Element]:
        return [elem for elem in self.tree.xpath(f".//page:Unicode", namespaces=self.ns)]

    def export(self, out: Path, pretty=True, encoding="unicode"):
        with out.open("w") as outfile:
            outfile.write(etree.tostring(self.tree, pretty_print=pretty, encoding=encoding))
