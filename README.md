# Jh_decorators

`jh_decorators` is a Python library designed to enhance the functionality of Python functions and classes through the use of decorators. It provides tools for documentation, internal item marking, performance measurement, logging, and serialization/deserialization.

## Features

- **Documentation Tools:** Decorators for adding detailed documentation to functions and classes, and marking items as documented.
- **Interface Tools:** Decorators for marking functions or classes as internal and ensuring methods override those in a superclass.
- **Performance Tools:** Decorators for timing function execution and logging activities.
- **Serialization Tools:** Decorators for converting class instances to/from JSON, XML, YAML, and dictionary formats.

## Installation

Install `jh_decorators` from a local wheel file with the following command:

```bash
pip install path/to/wheel/jh_decorators-0.1.0-py3-none-any.whl
```

Make sure the path to the `.whl` file is correct and accessible from your command line environment. This method is ideal for offline installations or when using a custom-built version.

## PyCharm Integration

PyCharm users can build and run scripts directly from the `README.md` file using clickable links. Here's how:

1. Ensure you have a `build.py` script at the root of your project that handles the build process.
2. To run the script directly from this `README.md`, use PyCharm to open this file and then click on the link below:

    ```bash
    python build.py
    ```

3. After building, you can also reinstall the package directly by clicking on:

    ```bash
    pip install --force-reinstall wheel/jh_decorators-0.1.0-py3-none-any.whl
    ```

These links will execute the commands in PyCharm without needing to open the terminal.

## Usage

### Documentation

- `@Annotation(...)`: Adds custom documentation to the decorated function or class.
- `@Documented`: Marks a function or class as having been documented.

### Interface

- `@Inner`: Marks a function or class as internal, not exposed to end users.
- `@Override`: Ensures a method overrides a method in its superclass, raises `OverrideError` if not.

### Performance

- `@Timing(...)`: Measures and optionally reports the execution time of the decorated function.
- `@Log(...)`: Logs function calls, arguments, and return values.

### Serialization

- `@Jsonize`: Adds JSON serialization and deserialization methods to the class.
- `@XMLize`: Adds XML serialization and deserialization methods to the class.
- `@YAMLize`: Adds YAML serialization and deserialization methods to the class.
- `@Dictize`: Adds dictionary conversion methods to the class.

### API Generation

- `generate_api(include_unannotated: bool = False) -> None`: Generates a `.pyi` file containing the signatures and docstrings of the annotated functions.

    ```python
    from jh_decorators.documentation import generate_api

    if __name__ == "__main__":
        generate_api(include_unannotated=True)
    ```

    This utility generates a `.pyi` file with the same name as the module, replacing all `Annotation` decorators with a default `Documented` decorator without any details for simplicity. It generates all dynamic changes such as adding methods to classes or changing function/class documentation into a static `.pyi` file, making it better for IDE code checking.

## Contributing

Contributions to `jh_decorators` are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) and [security guidelines](SECURITY.md) to start.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
