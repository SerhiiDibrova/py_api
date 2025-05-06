import json
import logging
from enum import Enum
from typing import Any, Dict, Optional, Union, Mapping, Sequence, TypeAlias

from lxml import etree
from lxml.etree import _Element, parse, fromstring

from src.config.annotations import JSONType  # consider replacing with local TypeAlias

logger = logging.getLogger(__name__)


# (1) Define your JSONType if you want clarity here:
JSONType: TypeAlias = Union[
    None,
    bool,
    int,
    float,
    str,
    Mapping[str, "JSONType"],
    Sequence["JSONType"],
]


class XMLParseError(Exception):
    """Raised when XML schema or types are invalid."""
    pass


class XMLElementType(str, Enum):
    FLOAT   = "float"
    INTEGER = "integer"
    STRING  = "string"
    BOOLEAN = "boolean"
    OBJECT  = "object"
    LIST    = "list"
    NULL    = "null"

    @staticmethod
    def from_value(value: Any) -> "XMLElementType":
        if isinstance(value, str):
            return XMLElementType.STRING
        elif isinstance(value, bool):
            return XMLElementType.BOOLEAN
        elif isinstance(value, int):
            return XMLElementType.INTEGER
        elif isinstance(value, float):
            return XMLElementType.FLOAT
        elif isinstance(value, dict):
            return XMLElementType.OBJECT
        elif isinstance(value, list):
            return XMLElementType.LIST
        elif value is None:
            return XMLElementType.NULL
        else:
            raise XMLParseError(f"Unsupported type: {type(value)}")

    def parse_element_value(self, value: Optional[str]) -> Any:
        # NULL or empty tag
        if value is None:
            if self is XMLElementType.NULL:
                return None
            if self is XMLElementType.OBJECT:
                return {}
            raise XMLParseError("Invalid XML schema for non-leaf node")

        # parse based on type
        if self is XMLElementType.STRING:
            return value
        if self is XMLElementType.INTEGER:
            return int(value)
        if self is XMLElementType.FLOAT:
            return float(value)
        if self is XMLElementType.BOOLEAN:
            val = value.strip().lower()
            if val in ("true", "1", "yes"):
                return True
            if val in ("false", "0", "no"):
                return False
            raise XMLParseError(f"Invalid boolean value: {value}")
        raise XMLParseError(f"Unsupported leaf type: {self.value}")


class XMLParser:
    """Robust XML↔JSONType parser with error handling and logging."""

    @staticmethod
    def _parse_etree_node_leaf(element: _Element) -> Any:
        etype = XMLElementType(element.get("type"))
        raw = element.get("value")
        try:
            return etype.parse_element_value(raw)
        except Exception as e:
            logger.exception("Leaf parse failed: %r type=%s", element, etype)
            raise

    @staticmethod
    def _parse_etree_to_json_type(node: _Element) -> JSONType:
        children = list(node)
        key = node.get("key")

        # Leaf node
        if not children:
            val = XMLParser._parse_etree_node_leaf(node)
            return {key: val} if key else val

        # List vs Object
        if all(child.get("key") is None for child in children):
            return [XMLParser._parse_etree_to_json_type(c) for c in children]

        obj: Dict[str, JSONType] = {}
        for c in children:
            ckey = c.get("key")
            if not ckey:
                raise XMLParseError("Expected 'key' on object child")
            obj[ckey] = (
                XMLParser._parse_etree_to_json_type(c)
                if c.get("type") in ("object", "list")
                else XMLParser._parse_etree_node_leaf(c)
            )
        return obj

    @staticmethod
    def _parse_json_data_to_etree(data: JSONType) -> _Element:
        etype = XMLElementType.from_value(data)
        element = etree.Element("ITEM", type=etype.value)

        if etype is XMLElementType.OBJECT:
            for k, v in data.items():  # type: ignore
                child = XMLParser._parse_json_data_to_etree(v)
                child.set("key", k)
                element.append(child)

        elif etype is XMLElementType.LIST:
            for v in data:  # type: ignore
                element.append(XMLParser._parse_json_data_to_etree(v))

        elif etype in (XMLElementType.STRING, XMLElementType.INTEGER,
                       XMLElementType.FLOAT, XMLElementType.BOOLEAN):
            # JSON-encode non-string leaves to preserve type
            element.set("value", json.dumps(data) if etype is not XMLElementType.STRING else data)  # type: ignore

        # NULL: no value attribute

        return element

    @staticmethod
    def parse_xml_from_file(file: Any) -> JSONType:
        """
        Parse XML file to JSONType object.
        """
        tree = parse(file)
        return XMLParser._parse_etree_to_json_type(tree.getroot())

    @staticmethod
    def parse_xml_from_string(xml_str: str) -> JSONType:
        """
        Parse XML string to JSONType object.
        """
        root = fromstring(xml_str.encode())
        return XMLParser._parse_etree_to_json_type(root)

    @staticmethod
    def parse_json_to_element(data: JSONType) -> _Element:
        """
        Convert JSONType object to an lxml Element.
        """
        return XMLParser._parse_json_data_to_etree(data)

    @staticmethod
    def to_pretty_xml(element: _Element, encoding: str = "utf-8") -> bytes:
        """
        Return a pretty-printed XML byte string.
        """
        return etree.tostring(
            element,
            pretty_print=True,
            xml_declaration=True,
            encoding=encoding,
        )
