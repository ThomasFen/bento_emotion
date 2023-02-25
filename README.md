# Steps
Install requirements(Python 3.8)

    pip install -r requirements.txt

Load models into bento

    python load-model.py

Create bento endpoint on port 3000

    BENTOML_CONFIG=./cfg.yml bentoml serve --production
Test 

    cd tests && python async.py