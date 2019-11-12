#!/bin/bash
pip install -e git+https://gitlab.com/datadrivendiscovery/d3m@a8af7585fdd85e2218ca88b257bb0ec71adabfb3#egg=d3m --progress-bar off
pip install -e git+https://gitlab.com/datadrivendiscovery/common-primitives.git@5c43e65d306a4f36d53db2fb497c9869e2fb7294#egg=common_primitives --progress-bar off
pip install -e git+https://gitlab.com/datadrivendiscovery/sklearn-wrap@dist#egg=sklearn-wrap --progress-bar off
pip uninstall -y tensorflow-gpu
export LD_LIBRARY_PATH="$HOME/miniconda/envs/ta1-test-env/lib:$LD_LIBRARY_PATH"
pip install tensorflow==1.12.0
pip install -e . --progress-bar off
pip install -e git+https://github.com/brekelma/dsbox_corex@master#egg=dsbox_corex --progress-bar off
pip list
