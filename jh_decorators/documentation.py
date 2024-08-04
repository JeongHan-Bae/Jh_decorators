# jh_decorators/documentation.py

import inspect
import ast
import os
import sys
from typing import Callable, Any, List, Tuple, Union, Type
from collections import OrderedDict

from jh_decorators.interface import _inner_items
from jh_decorators.reflection import dictized_classes, jsonized_classes, xmlized_classes, yamlized_classes

annotated_callables: 'OrderedDict[str, Union[Callable[..., Any], Type[Any]]]' = OrderedDict()


def Annotation(*decorator_args: Callable[..., Any],
               **decorator_kwargs: Union[List[Tuple[str, str]], str, List[str]]) -> Callable[..., Any]:
    """
    Decorator to add documentation to a function or class. It can be used with or without parameters.

    Args:
        *decorator_args: Arguments passed to the decorator.
        **decorator_kwargs: Keyword arguments passed to the decorator.

            *args*: List of tuples representing parameter documentation in the form of (name, description).
            *return_doc*: Description of the return value.
            *raises_doc*: List of exceptions that the function or class may raise.

    Returns:
        Callable[..., Any]: The decorated function or class with added documentation.
    """

    def actual_decorator(item: Callable[..., Any]) -> Callable[..., Any]:
        param_docs: List[str] = []
        args: List[Tuple[str, str]] = decorator_kwargs.get('args', [])
        return_doc: str = decorator_kwargs.get('return_doc', '')
        raises_doc: List[str] = decorator_kwargs.get('raises_doc', [])

        if isinstance(args, (list, tuple)):
            for arg in args:
                if isinstance(arg, tuple) and len(arg) == 2:
                    param_docs.append(f"{arg[0]} : {arg[1]}")

        docstring = item.__doc__ or ""
        indent = " " * 4
        double_indent = indent * 2
        if param_docs:
            docstring += f"\n{indent}Args:\n{double_indent}" + f"\n{double_indent}".join(param_docs) + "\n"
        if return_doc:
            docstring += f"\n{indent}Returns:\n{double_indent}{return_doc}\n"
        if raises_doc:
            docstring += f"\n{indent}Raises:\n{double_indent}" + f"\n{double_indent}".join(raises_doc) + "\n"
        docstring = f"\n{indent}" + docstring.strip() + f"\n{indent}"

        item.__doc__ = docstring

        # Add to annotated callables
        if inspect.isclass(item):
            if item.__name__ not in annotated_callables:
                annotated_callables[item.__name__] = item
        elif inspect.isfunction(item):
            sig = inspect.signature(item)
            params = list(sig.parameters.values())
            if params and params[0].name == 'self':
                pass
            else:
                annotated_callables[item.__name__] = item

        # Dynamically add Documented decorator
        item = Documented(item)

        return item

    # If the decorator is used without parameters
    if len(decorator_args) == 1 and callable(decorator_args[0]):
        return actual_decorator(decorator_args[0])

    return actual_decorator


def Documented(item: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to mark an item (function or class) as documented.

    Args:
        item (Callable[..., Any]): The item to be marked as documented.

    Returns:
        Callable[..., Any]: The original item marked as documented.
    """
    return item


def generate_api(include_unannotated: bool = False) -> None:
    """
    Generates a .pyi file containing the signatures and docstrings of the annotated functions.

    Args:
        include_unannotated (bool): If True, includes functions without annotations in the generated file.
    """

    def generate_docstring(__obj: Callable[..., Any]) -> str:
        """Generate the docstring for a function or class."""
        docstring: str = __obj.__doc__ or ''
        return f'    """{docstring}"""\n' if docstring else ''

    def write_function(_f: Any, __name: str, __obj: Callable[..., Any], documented: bool) -> None:
        """Write the function signature and docstring to the file."""
        docstring: str = generate_docstring(__obj)
        signature: str = str(inspect.signature(__obj))
        if documented:
            _f.write(f"@Documented\n")
        _f.write(f"def {__name}{signature}:\n")
        if docstring:
            _f.write(docstring)
        _f.write("    ...\n\n")

    def write_class(_f: Any, __name: str, __obj: Any, documented: bool,
                    __has_dictize: bool, __has_jsonize: bool, __has_xmlize: bool, __has_yamlize: bool) -> None:
        """Write the class signature and its methods to the file."""
        docstring: str = generate_docstring(__obj)
        if documented:
            _f.write(f"@Documented\n")
        _f.write(f"class {__name}:\n")
        if docstring:
            _f.write(docstring)
        for method_name, method in inspect.getmembers(__obj, inspect.isfunction):
            signature: str = str(inspect.signature(method))
            # Remove 'self: Any' from the signature
            if 'self' in signature:
                signature = signature.replace('(self: Any', '(self')
            method_doc: str = generate_docstring(method)
            _f.write(f"    def {method_name}{signature}:\n")
            if method_doc:
                method_doc = method_doc.strip().replace("\n", "\n" + " " * 4)
                _f.write(f'        {method_doc}\n')
            _f.write(" " * 8 + "...\n\n")
        if __has_dictize:
            _f.write("    @classmethod\n")
            _f.write("    def from_dict(cls, data: dict):\n")
            _f.write(" " * 8 + "...\n\n")
        if __has_jsonize:
            _f.write("    @classmethod\n")
            _f.write("    def from_json(cls, json_str: str):\n")
            _f.write(" " * 8 + "...\n\n")
        if __has_xmlize:
            _f.write("    @classmethod\n")
            _f.write("    def from_xml(cls, xml_str: str):\n")
            _f.write(" " * 8 + "...\n\n")
        if __has_yamlize:
            _f.write("    @classmethod\n")
            _f.write("    def from_yaml(cls, yaml_str: str):\n")
            _f.write(" " * 8 + "...\n\n")

    def get_reflections():
        # Check if class has Dictize, Jsonize, XMLize, or YAMLize decorators
        _has_dictize = name in dictized_classes.get(obj.__module__, [])
        _has_jsonize = name in jsonized_classes.get(obj.__module__, [])
        _has_xmlize = name in xmlized_classes.get(obj.__module__, [])
        _has_yamlize = name in yamlized_classes.get(obj.__module__, [])

        return _has_dictize, _has_jsonize, _has_xmlize, _has_yamlize

    # Get the current module
    module = sys.modules['__main__']
    module_file = module.__file__
    module_name = os.path.splitext(os.path.basename(module_file))[0]
    output_file = f"{module_name}.pyi"

    # Read the source code of the module to find import statements
    module_source = inspect.getsource(module)
    module_ast = ast.parse(module_source)

    import_statements: List[Union[ast.Import, ast.ImportFrom]] = []
    for node in module_ast.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            match node:
                case ast.ImportFrom(module='jh_decorators.documentation'):
                    # Replace Annotation with Documented and skip generate_api
                    new_names = [alias for alias in node.names if alias.name not in ['generate_api', 'Annotation']]
                    if new_names:
                        node.names = new_names
                        import_statements.append(node)
                case ast.ImportFrom(module='jh_decorators.interface'):
                    # Skip Inner, update_global and get_global
                    new_names = [alias for alias in node.names if alias.name
                                 not in ['Inner', 'update_global', 'get_global']]
                    if new_names:
                        node.names = new_names
                        import_statements.append(node)
                case ast.ImportFrom(module='jh_decorators.reflection'):
                    # Skip Jsonize, Dictize, XMLize and YAMLize
                    new_names = [alias for alias in node.names if alias.name
                                 not in ['Jsonize', 'Dictize', 'XMLize', 'YAMLize']]
                    if new_names:
                        node.names = new_names
                        import_statements.append(node)
                case ast.ImportFrom(module='jh_decorators.performance'):
                    # Skip Timing, Log and ProgressBar
                    new_names = [alias for alias in node.names if
                                 alias.name not in ['Timing', 'Log', 'ProgressBar']]
                    if new_names:
                        node.names = new_names
                        import_statements.append(node)
                case _:
                    import_statements.append(node)

    with open(output_file, 'w') as f:
        f.write("from jh_decorators.documentation import Documented\n")
        # Write import statements
        for stmt in import_statements:
            if isinstance(stmt, ast.Import):
                for alias in stmt.names:
                    f.write(f"import {alias.name}")
                    if alias.asname:
                        f.write(f" as {alias.asname}")
                    f.write("\n")
            elif isinstance(stmt, ast.ImportFrom):
                f.write(f"from {stmt.module} import ")
                names = [f"{alias.name}" if alias.asname is None else f"{alias.name} as {alias.asname}" for alias in
                         stmt.names]
                f.write(", ".join(names))
                f.write("\n")

        f.write("\n")

        # Write documented functions and classes
        for name, obj in annotated_callables.items():
            if inspect.isfunction(obj) and obj.__module__ == module.__name__ and name not in _inner_items.get(
                    module.__name__, []):
                write_function(f, name, obj, True)
            elif inspect.isclass(obj) and obj.__module__ == module.__name__ and name not in _inner_items.get(
                    module.__name__, []):
                write_class(f, name, obj, True, *get_reflections())

        # Optionally write unannotated functions and classes
        if include_unannotated:
            for name, obj in inspect.getmembers(module):
                if inspect.isfunction(
                        obj) and name not in annotated_callables and obj.__module__ == module.__name__ and \
                        name not in _inner_items.get(module.__name__, []):
                    write_function(f, name, obj, False)
                elif inspect.isclass(
                        obj) and name not in annotated_callables and obj.__module__ == module.__name__ and \
                        name not in _inner_items.get(module.__name__, []):
                    write_class(f, name, obj, True, *get_reflections())
