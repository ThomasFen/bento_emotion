# Steps
## Installation
Install requirements(Python 3.8)

    pip install -r requirements.txt

Load models into bento

    python load-model.py
## Run prediction service

Create bento endpoint on port 3000

    BENTOML_CONFIG=./cfg.yml bentoml serve --production
Test 

    cd tests && python async.py

## Run containerized prediction service
Build the bento and generate a docker image 

```bash
$ bentoml build
Successfully built Bento(tag="emotion_recognition:zd2vyafvicgucaav").

$ bentoml containerize emotion_recognition:zd2vyafvicgucaav
Successfully built Bento container for "emotion_recognition:zd2vyafvicgucaav" with tag(s) "emotion_recognition:zd2vyafvicgucaav"

$ docker run -p 3000:3000 --rm -v $(pwd)/cfg.yml:/home/bentoml/configuration.yml \
             -e BENTOML_CONFIG=/home/bentoml/configuration.yml \
             emotion_recognition:zd2vyafvicgucaav serve --production
Starting production BentoServer from "emotion_recognition:zd2vyafvicgucaav" running on http://0.0.0.0:3000
```
Test 

    cd tests && python async.py