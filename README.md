# Steps
## Installation
Install requirements (Python 3.8)

    pip install -r requirements.txt

Load models into bento

    python load-model.py
## Run prediction service

Create bento endpoint on port 3000

    BENTOML_CONFIG=./cfg.yml bentoml serve --production

## Or: Run containerized prediction service
Build the bento 
```bash
$ bentoml build
Successfully built Bento(tag="emotion_recognition:zd2vyafvicgucaav").
```

### Docker
Generate Docker image
```bash
$ bentoml containerize emotion_recognition:zd2vyafvicgucaav
Successfully built Bento container for "emotion_recognition:zd2vyafvicgucaav" with tag(s) "emotion_recognition:zd2vyafvicgucaav"

$ docker run -p 3000:3000 --rm -v $(pwd)/cfg.yml:/home/bentoml/configuration.yml \
             -e BENTOML_CONFIG=/home/bentoml/configuration.yml \
             emotion_recognition:zd2vyafvicgucaav serve --production
Starting production BentoServer from "emotion_recognition:zd2vyafvicgucaav" running on http://0.0.0.0:3000
```
### Kubernetes
Install the [Yatai](https://github.com/bentoml/Yatai) components and follow their instructions to push the bento to Yatai 
```
$ bentoml yatai login --api-token {YOUR_TOKEN} --endpoint http://127.0.0.1:8080
$ bentoml push emotion_recognition:zd2vyafvicgucaav
│ Successfully pushed model "emotion:uouhv7vvg2ka6aav"
│ Successfully pushed model "blazeface_back:uprkd2fvg2ka6aav"
│ Successfully pushed bento "emotion_recognition:zd2vyafvicgucaav" 
```

Go to the deployments page: http://127.0.0.1:8080/deployments, click Create button and follow the instructions on the UI. Paste this into the BentoML configuration textfield
```
runners.timeout=1 runners.batching.enabled=true runners.batching.max_batch_size=100 runners.batching.max_latency_ms=60
```

__Note__: The yatai-deployment component script installs a metrics server, which is needed for auto-scaling. If the metric pod fails during installation, try adding the following to `spec.template.spec.containers[].args` in the metrics-server _deployment_ of [components.yaml](https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml) and apply it manually.
```
- --kubelet-insecure-tls
```
## Test
Run a simple test script. Send many requests at once `python request.py {URL} {REQUEST_AMOUNT}`, or send them one after another `python request.py {URL} {REQUEST_AMOUNT} --one-by-one`
```
$ cd tests && python request.py http://emotion-yatai.127.0.0.1.sslip.io/predict_async 2000
...
Response content: b'{"userId":345786,"conferenceId":890678,"clientFaceDetection":true,"emotions":[{"raw":{"neutral":0.05500756949186325,"happy":0.1018536314368248,"sad":0.16155335307121277,"surprise":0.09337092190980911,"fear":0.31956708431243896,"disgust":0.2149820476770401,"anger":0.04546269401907921,"contempt":0.008202659897506237},"dominantEmotion":"fear"}],"date":"2023-02-25T19:39:19.216+00:00","duration":0.063389253616333}'
Response code: 500
Response code: 503
...
```
- Response code 500 usually means the request was cancelled because a Runner is too busy (`timeout` in config).
- Response code 503 usually means bento removed the request from the adaptive batching queue of the emotion model, because it figured out that the inference time + queue wait time would be higher than `max_latency_ms` in config.
- Response code 502 usually means a general resource issue, try adding more memory/cpu when using Yatai.

Starting the service without the BentoML config options timeout/max_latency_ms would greatly increase the latency of requests when the system is under load. This is because none of the requests would be cancelled.