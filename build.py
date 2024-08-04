import os
import shutil

# Build the distribution
os.system("python setup.py sdist bdist_wheel")

# Remove the build folder
if os.path.exists('build'):
    shutil.rmtree('build')
    print("Build directory removed.")

# Remove the previous wheel folder
if os.path.exists('wheel'):
    shutil.rmtree('wheel')
    print("Previous wheel directory removed.")

# Rename the dist folder to wheel
if os.path.exists('dist'):
    os.rename('dist', 'wheel')
    print("Dist directory renamed to wheel.")
