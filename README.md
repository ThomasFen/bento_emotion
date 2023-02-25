# Steps
## Installation
Install requirements(Python 3.8)

    pip install -r requirements.txt

Load models into bento

    python load-model.py
## Run prediction service

Create bento endpoint on port 3000

    BENTOML_CONFIG=./cfg.yml bentoml serve --production

## Or: Run containerized prediction service
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

## Test
Run simple test script.

Response code 500 usually means the request was cancelled because a Runner is too busy (`timeout` in config).

Response code 503 usually means bento removed the request from the adaptive batching queue of the emotion model, because it figured out that the inference time + queue wait time would be lower than `max_latency_ms` in config.
```
$ cd tests && python async.py
...
Response content: b'{"userId":345786,"conferenceId":890678,"clientFaceDetection":true,"emotions":[{"raw":{"neutral":0.05500756949186325,"happy":0.1018536314368248,"sad":0.16155335307121277,"surprise":0.09337092190980911,"fear":0.31956708431243896,"disgust":0.2149820476770401,"anger":0.04546269401907921,"contempt":0.008202659897506237},"dominantEmotion":"fear"}],"date":"2023-02-25T19:39:19.216+00:00","duration":0.063389253616333}'
Response code: 500
Response code: 503
...
```

Starting the service without the config file would greatly increase the latency of requests when the system is under load. This is because none of the requests would be cancelled.