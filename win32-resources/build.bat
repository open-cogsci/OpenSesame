copy setup.py ..\setup-win32.py
cd ..
python setup-win32.py py2exe
del setup-win32.py
move dist win32-build
