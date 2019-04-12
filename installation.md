# environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# tf-openpose

### installation
```
git clone https://www.github.com/ildoonet/tf-pose-estimation
cd tf-openpose
python setup.py install
```

### download models
```
cd models/graph/cmu
bash download.sh
```

# starting the app

```
export FLASK_APP=main.py
flask run
```
