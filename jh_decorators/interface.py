# jh_decorators/interface.py

import sys
import functools
from typing import Callable, Any, Dict, List, cast

# Record all internal items in all modules
_inner_items: Dict[str, List[str]] = {}


def Inner(item: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to mark a function or a class as internal.
    Internal items will be inaccessible in user modules.

    Args:
        item (Callable): The callable to be marked as internal.

    Returns:
        Any: The original item marked as internal.
    """

    item_class = cast(type, getattr(item, '__class__'))

    module_name: str = item.__module__ if hasattr(item, '__module__') else item_class.__module__
    item_name: str = item.__name__ if hasattr(item, '__name__') else item_class.__name__

    # Mark the item as internal
    item.__is_inner = True

    if module_name not in _inner_items:
        _inner_items[module_name] = []

    _inner_items[module_name].append(item_name)

    def wrap_function(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # Check the call stack for the calling module
            frame_getter = cast(Callable[[int], Any], getattr(sys, '_getframe'))
            calling_frame = frame_getter(1)
            calling_module = calling_frame.f_globals['__name__']

            if calling_module != module_name:
                # Check the entire call stack for the defining module
                current_frame = calling_frame
                while current_frame:
                    if current_frame.f_globals['__name__'] == module_name:
                        break
                    current_frame = current_frame.f_back
                else:
                    raise RuntimeError(
                        f"{item_name} is an internal function and cannot be called outside its defining module.")

            return func(*args, **kwargs)

        return wrapped

    if isinstance(item, type):
        # Handle classes
        for attr_name, attr_value in item.__dict__.items():
            if callable(attr_value):
                if isinstance(attr_value, (staticmethod, classmethod)):
                    # Unwrap staticmethod and classmethod to get the actual function
                    original_func = attr_value.__func__
                    wrapped_func = wrap_function(original_func)
                    setattr(item, attr_name, type(attr_value)(wrapped_func))
                else:
                    setattr(item, attr_name, wrap_function(attr_value))
        # Ensure the class itself is also marked
        item = wrap_function(item)
    else:
        # Handle functions and other callables
        item = wrap_function(item)

    # Replace the original item with the wrapped version in the module's dictionary
    sys.modules[module_name].__dict__[item_name] = item

    return item


class OverrideError(Exception):
    """
    Exception raised when a method decorated with @Override does not override any method in the superclass.

    Args:
        message (str): Explanation of the error.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


def Override(method: Callable[..., Any]) -> Callable[..., Any]:
    """
    A decorator to indicate that a method is intended to override a method in the superclass.
    Raises an OverrideError if the method does not override any method in the superclass.

    Args:
        method (Callable[..., Any]): The method to be checked for overriding.

    Returns:
        Callable[..., Any]: The original method if it correctly overrides a method in the superclass.

    Raises:
        OverrideError: If the method does not override any method in the superclass.
    """

    if not callable(method):
        raise TypeError(f"{method.__name__} is not a callable")

    @functools.wraps(method)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        cls = args[0].__class__
        if not any(hasattr(base_class, method.__name__) for base_class in cls.__bases__):
            raise OverrideError(f"{method.__name__} does not override any method in superclass")
        return method(*args, **kwargs)

    return wrapper


def update_global(name: str, value: Any) -> None:
    """
    Register or update a global variable or constant as internal to the module.

    Args:
        name (str): The name of the variable or constant.
        value (Any): The value of the variable or constant.
    """
    if not hasattr(sys.modules[__name__], '_global_inner_items'):
        setattr(sys.modules[__name__], '_global_inner_items', {})

    global_inner_items = getattr(sys.modules[__name__], '_global_inner_items')
    global_inner_items[name] = value


def get_global(name: str) -> Any:
    """
    Retrieve a global variable or constant that is marked as internal to the module.

    Args:
        name (str): The name of the variable or constant.

    Returns:
        Any: The value of the variable or constant, if it exists.

    Raises:
        KeyError: If the variable or constant is not found.
    """
    if not hasattr(sys.modules[__name__], '_global_inner_items'):
        raise KeyError(f"No internal globals registered in module")

    global_inner_items = getattr(sys.modules[__name__], '_global_inner_items')

    if name in global_inner_items:
        return global_inner_items[name]
    else:
        raise KeyError(f"{name} not found in internal globals")
