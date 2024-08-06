# Jh_decorators

`jh_decorators` is a Python library designed to enhance the functionality of Python functions and classes through the use of decorators. It provides tools for documentation, internal item marking, performance measurement, logging, and serialization/deserialization. / `jh_decorators` 是一个Python库，通过使用装饰器来增强Python函数和类的功能。它提供了文档编写、内部项标记、性能测量、日志记录和序列化/反序列化的工具。

## Features / 功能

- **Documentation Tools / 文档工具:** Decorators for adding detailed documentation to functions and classes, and marking items as documented. / 用于向函数和类添加详细文档的装饰器，并将项目标记为已记录。
- **Interface Tools / 接口工具:** Decorators for marking functions or classes as internal and ensuring methods override those in a superclass. / 用于将函数或类标记为内部的装饰器，并确保方法重载超类中的方法。
- **Performance Tools / 性能工具:** Decorators for timing function execution and logging activities. / 用于测量函数执行时间和记录活动的装饰器。
- **Serialization Tools / 序列化工具:** Decorators for converting class instances to/from JSON, XML, YAML, and dictionary formats. / 用于将类实例与JSON、XML、YAML和字典格式互相转换的装饰器。

## Installation / 安装

Install `jh_decorators` from a local wheel file with the following command: / 通过以下命令从本地轮文件安装 `jh_decorators`：

```bash
pip install path/to/wheel/jh_decorators-0.1.0-py3-none-any.whl
```

Make sure the path to the `.whl` file is correct and accessible from your command line environment. This method is ideal for offline installations or when using a custom-built version. / 确保 `.whl` 文件的路径是正确的，并且可以从命令行环境访问。此方法适用于离线安装或使用自定义构建版本的情况。

## PyCharm Integration / PyCharm 集成

PyCharm users can build and run scripts directly from the `README.md` file using clickable command instructions. Here's how: / PyCharm 用户可以使用可点击的指令直接从 `README.md` 文件构建和运行脚本。操作如下：

1. Ensure you have a `build.py` script at the root of your project that handles the build process. / 确保在项目根目录下有一个 `build.py` 脚本来处理构建过程。
2. To run the script directly from this `README.md`, use PyCharm to open this file and then click on the command below: / 要直接从此 `README.md` 运行脚本，请使用 PyCharm 打开此文件，然后点击下面的指令：

    ```bash
    python build.py
    ```

3. After building, you can also reinstall the package directly by clicking on: / 构建完成后，您还可以通过点击以下指令直接重新安装软件包：

    ```bash
    pip install --force-reinstall wheel/jh_decorators-0.1.0-py3-none-any.whl
    ```

These commands will execute in PyCharm without needing to open the terminal. / 这些命令将在 PyCharm 中执行，无需打开终端。

## Usage / 使用

### Documentation / 文档

- `@Annotation(...)`: Adds custom documentation to the decorated function or class. / 向被装饰的函数或类添加自定义文档。
- `@Documented`: Marks a function or class as having been documented. / 将函数或类标记为已记录。

### Interface / 接口

- `@Inner`: Marks a function or class as internal, not exposed to end users. / 将函数或类标记为内部，不向最终用户公开。
- `@Override`: Ensures a method overrides a method in its superclass, raises `OverrideError` if not. / 确保方法重载其超类中的方法，如果没有则引发 `OverrideError`。

### Performance / 性能

- `@Timing(...)`: Measures and optionally reports the execution time of the decorated function. / 测量并可选择报告被装饰函数的执行时间。
- `@Log(...)`: Logs function calls, arguments, and return values. / 记录函数调用、参数和返回值。
- `@ProgressBar`: Adds a progress bar to a function, with dynamic colors based on progress percentage. This decorator is a specialized wrapper around the rich library's progress bar functionality. / 向函数添加进度条，进度条颜色根据进度百分比动态变化。这个装饰器是对 rich 库进度条功能的特化封装。

### Serialization / 序列化

- `@Jsonize`: Adds JSON serialization and deserialization methods to the class. / 为类添加JSON序列化和反序列化方法。
- `@XMLize`: Adds XML serialization and deserialization methods to the class. / 为类添加XML序列化和反序列化方法。
- `@YAMLize`: Adds YAML serialization and deserialization methods to the class. / 为类添加YAML序列化和反序列化方法。
- `@Dictize`: Adds dictionary conversion methods to the class. / 为类添加字典转换方法。

### API Generation / API 生成

- `generate_api(include_unannotated: bool = False) -> None`: Generates a `.pyi` file containing the signatures and docstrings of the annotated functions. / 生成包含注释函数签名和文档字符串的 `.pyi` 文件。

    ```python
    from jh_decorators.documentation import generate_api

    if __name__ == "__main__":
        generate_api(include_unannotated=True)
    ```

    This utility generates a `.pyi` file with the same name as the module, replacing all `Annotation` decorators with a default `Documented` decorator without any details for simplicity. It generates all dynamic changes such as adding methods to classes or changing function/class documentation into a static `.pyi` file, making it better for IDE code checking. / 该工具生成一个与模块同名的 `.pyi` 文件，将所有 `Annotation` 装饰器替换为默认的 `Documented` 装饰器，不带任何详细信息以简化操作。它将所有动态更改（如向类添加方法或更改函数/类文档）生成到静态 `.pyi` 文件中，使其更适合 IDE 代码检查。

### Global Variable Management / 全局变量管理

- `update_global(name: str, value: Any) -> None`: Registers or updates a global variable or constant as internal to the module. / 注册或更新全局变量或常量，并将其标记为模块的内部变量。
- `get_global(name: str) -> Any`: Retrieves a global variable or constant that is marked as internal to the module. / 检索标记为模块内部的全局变量或常量。

## Contributing / 贡献

Contributions to `jh_decorators` are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) and [security guidelines](SECURITY.md) to start. / 欢迎为 `jh_decorators` 贡献代码！请阅读[贡献指南](CONTRIBUTING.md)和[安全指南](SECURITY.md)以开始。

## License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. / 该项目根据 MIT 许可证授权 - 有关详细信息，请参见 [LICENSE](LICENSE) 文件。

---

For detailed information about each feature, please refer to the [API Documentation](API_Documentation.md). / 有关每个功能的详细信息，请参阅 [API 文档](API_Documentation.md)。
