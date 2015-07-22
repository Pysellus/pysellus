```text
virtualenv -p $(which python3) env
source env/bin/activate

pip install -r requirements-dev.txt
python setup.py develop
```
