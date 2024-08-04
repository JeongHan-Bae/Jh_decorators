# jh_decorators/reflection.py

import json
import yaml
import xmltodict
from functools import wraps
from typing import Type, Any, Callable, cast, Dict, List

# Global dictionaries to store classes decorated with Jsonize and Dictize
jsonized_classes: Dict[str, List[str]] = {}
dictized_classes: Dict[str, List[str]] = {}
xmlized_classes: Dict[str, List[str]] = {}
yamlized_classes: Dict[str, List[str]] = {}


def Jsonize(cls: Type) -> Type:
    """
    Class decorator to add methods to convert the instance to a JSON string
    and to create an instance from a JSON string.

    Args:
        cls (Type): The class to be decorated.

    Returns:
        Type: The decorated class with to_json and from_json methods.
    """
    original_init = cast(Callable[..., None], cls.__init__)

    @wraps(original_init)
    def new_init(self, *args: Any, **kwargs: Any) -> None:
        original_init(self, *args, **kwargs)

    def to_json(self: Any) -> str:
        return json.dumps({k: v for k, v in self.__dict__.items() if not callable(v)})

    def from_json(__cls: Type, json_str: str) -> Any:
        data = json.loads(json_str)
        return __cls(**data)

    setattr(cls, 'to_json', to_json)
    setattr(cls, 'from_json', classmethod(cast(Callable[..., Any], from_json)))
    cls.__init__ = cast(Callable[..., None], new_init)

    # Record the decorated class
    module_name = cls.__module__
    if module_name not in jsonized_classes:
        jsonized_classes[module_name] = []
    jsonized_classes[module_name].append(cls.__name__)

    return cls


def Dictize(cls: Type) -> Type:
    """
    Class decorator to add methods to convert the instance to a dictionary
    and to create an instance from a dictionary.

    Args:
        cls (Type): The class to be decorated.

    Returns:
        Type: The decorated class with to_dict and from_dict methods.
    """
    original_init = cast(Callable[..., None], cls.__init__)

    @wraps(original_init)
    def new_init(self, *args: Any, **kwargs: Any) -> None:
        original_init(self, *args, **kwargs)

    def to_dict(self: Any) -> dict:
        return {k: v for k, v in self.__dict__.items() if not callable(v)}

    def from_dict(__cls: Type, data: dict) -> Any:
        return __cls(**data)

    setattr(cls, 'to_dict', to_dict)
    setattr(cls, 'from_dict', classmethod(cast(Callable[..., Any], from_dict)))
    cls.__init__ = cast(Callable[..., None], new_init)

    # Record the decorated class
    module_name = cls.__module__
    if module_name not in dictized_classes:
        dictized_classes[module_name] = []
    dictized_classes[module_name].append(cls.__name__)

    return cls

def XMLize(cls: Type) -> Type:
    """
    Class decorator to add methods to convert the instance to an XML string
    and to create an instance from an XML string.

    Args:
        cls (Type): The class to be decorated.

    Returns:
        Type: The decorated class with to_xml and from_xml methods.
    """
    original_init = cast(Callable[..., None], cls.__init__)

    @wraps(original_init)
    def new_init(self, *args: Any, **kwargs: Any) -> None:
        original_init(self, *args, **kwargs)

    def to_xml(self: Any) -> str:
        return xmltodict.unparse({cls.__name__: self.__dict__}, pretty=True)

    def from_xml(__cls: Type, xml_str: str) -> Any:
        data = xmltodict.parse(xml_str)[cls.__name__]
        return __cls(**data)

    setattr(cls, 'to_xml', to_xml)
    setattr(cls, 'from_xml', classmethod(cast(Callable[..., Any], from_xml)))
    cls.__init__ = cast(Callable[..., None], new_init)

    # Record the decorated class
    module_name = cls.__module__
    if module_name not in xmlized_classes:
        xmlized_classes[module_name] = []
    xmlized_classes[module_name].append(cls.__name__)

    return cls


def YAMLize(cls: Type) -> Type:
    """
    Class decorator to add methods to convert the instance to a YAML string
    and to create an instance from a YAML string.

    Args:
        cls (Type): The class to be decorated.

    Returns:
        Type: The decorated class with to_yaml and from_yaml methods.
    """
    original_init = cast(Callable[..., None], cls.__init__)

    @wraps(original_init)
    def new_init(self, *args: Any, **kwargs: Any) -> None:
        original_init(self, *args, **kwargs)

    def to_yaml(self: Any) -> str:
        return yaml.dump(self.__dict__)

    def from_yaml(__cls: Type, yaml_str: str) -> Any:
        data = yaml.safe_load(yaml_str)
        return __cls(**data)

    setattr(cls, 'to_yaml', to_yaml)
    setattr(cls, 'from_yaml', classmethod(cast(Callable[..., Any], from_yaml)))
    cls.__init__ = cast(Callable[..., None], new_init)

    # Record the decorated class
    module_name = cls.__module__
    if module_name not in yamlized_classes:
        yamlized_classes[module_name] = []
    yamlized_classes[module_name].append(cls.__name__)

    return cls
