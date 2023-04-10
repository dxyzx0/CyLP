```shell
cd cylp/cy
rm *.cpp *.so *.html
cd ...
python setup.py build_ext --inplace
# comment `Py_DECREF(f);` in `cylp/cy/CyPivotPythonBase.cpp`
#python setup.py build_ext --inplace
``` 