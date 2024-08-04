# jh_decorators/performance.py

import logging
import functools
import time
from rich.progress import Progress, TextColumn, TimeRemainingColumn, BarColumn
from rich.console import RenderableType
from rich.progress import Task
from typing import Optional, List
from colorama import Fore, init

# Initialize colorama
init(autoreset=True)


# Timing Decorator
def Timing(output_obj: Optional[List] = None):
    """
    A decorator to measure the execution time of a function and optionally
    output the result to a list object.

    Args:
        output_obj (Optional[list]): An optional list object to store the result.

    Returns:
        Callable: The decorated function with timing functionality.
    """
    if callable(output_obj):
        func = output_obj
        output_obj = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            output_str = f"Function {func.__name__} took {duration:.4f} ms"

            if output_obj is None:
                print(Fore.CYAN + output_str)
            elif isinstance(output_obj, list):
                output_obj.append(output_str)
            return result

        return wrapper

    def decorator(__func):
        @functools.wraps(__func)
        def _wrapper(*args, **kwargs):
            start_time = time.time()
            result = __func(*args, **kwargs)
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            output_str = f"Function {__func.__name__} took {duration:.4f} ms"

            if _wrapper.output_obj is None:
                print(Fore.CYAN + output_str)
            elif isinstance(_wrapper.output_obj, list):
                _wrapper.output_obj.append(output_str)

            return result

        _wrapper.output_obj = output_obj
        return _wrapper

    return decorator


# Logging Decorator
def Log(output_obj: Optional[List] = None):
    """
    A decorator to log function calls, arguments, and return values.
    Optionally outputs the log to a list object.

    Args:
        output_obj (Optional[list]): An optional list object to store the log.

    Returns:
        Callable: The decorated function with logging functionality.
    """
    if callable(output_obj):
        func = output_obj
        output_obj = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_msg_prefix = ""
            try:
                log_msg = f"{log_msg_prefix}Calling {func.__name__} with args: {args}, kwargs: {kwargs}"
                if output_obj is None:
                    print(Fore.YELLOW + log_msg)
                elif isinstance(output_obj, list):
                    output_obj.append(log_msg)
                result = func(*args, **kwargs)
                log_msg = f"{log_msg_prefix}{func.__name__} returned {result}"
                if output_obj is None:
                    print(Fore.YELLOW + log_msg)
                elif isinstance(output_obj, list):
                    output_obj.append(log_msg)
                return result
            except Exception as e:
                log_msg = f"{log_msg_prefix}Error in {func.__name__}: {e}"
                if output_obj is None:
                    print(Fore.RED + log_msg)
                elif isinstance(output_obj, list):
                    output_obj.append(log_msg)
                return None

        return wrapper

    logging.basicConfig(level=logging.INFO)

    def decorator(__func):
        @functools.wraps(__func)
        def _wrapper(*args, **kwargs):
            log_msg_prefix = ""

            try:
                log_msg = f"{log_msg_prefix}Calling {__func.__name__} with args: {args}, kwargs: {kwargs}"
                if _wrapper.output_obj is None:
                    print(Fore.YELLOW + log_msg)
                elif isinstance(_wrapper.output_obj, list):
                    _wrapper.output_obj.append(log_msg)

                result = __func(*args, **kwargs)

                log_msg = f"{log_msg_prefix}{__func.__name__} returned {result}"
                if _wrapper.output_obj is None:
                    print(Fore.YELLOW + log_msg)
                elif isinstance(_wrapper.output_obj, list):
                    _wrapper.output_obj.append(log_msg)

                return result
            except Exception as e:
                log_msg = f"{log_msg_prefix}Error in {__func.__name__}: {e}"
                if _wrapper.output_obj is None:
                    print(Fore.RED + log_msg)
                elif isinstance(_wrapper.output_obj, list):
                    _wrapper.output_obj.append(log_msg)

                return None

        _wrapper.output_obj = output_obj
        return _wrapper

    return decorator


# Progress Bar Decorator with dynamic colors
def ProgressBar(func):
    """
    A decorator to add a progress bar to a function, with dynamic colors based on the progress percentage.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with a progress bar.
    """

    class ColorChangingBarColumn(BarColumn):
        """
        A custom BarColumn class that changes color dynamically based on the progress percentage.
        """

        def render(self, task: Task) -> RenderableType:
            percentage = task.percentage
            if percentage < 20:
                self.style = "red"
            elif percentage < 40:
                self.style = "orange1"
            elif percentage < 60:
                self.style = "yellow"
            elif percentage < 80:
                self.style = "green"
            else:
                self.style = "cyan"
            return super().render(task)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        total = kwargs.get('total', 100)

        progress = Progress(
            TextColumn("[white]{task.description}"),
            ColorChangingBarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeRemainingColumn()
        )

        with progress:
            task_id = progress.add_task(func.__name__, total=total)
            kwargs['progress'] = progress
            kwargs['task_id'] = task_id
            result = func(*args, **kwargs)

        return result

    return wrapper
