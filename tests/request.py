import requests

from requests_toolbelt.multipart.encoder import MultipartEncoder

m = MultipartEncoder(
    fields={
        "annotations": '{"userId": 345786, "conferenceId": 890678}',
        "image": ("image", open("test.png", "rb"), "image/png"),
    }
)

# bentoml serve endpoint 
# response =requests.post(
#     "http://0.0.0.0:3000/predict_async", data=m, headers={"Content-Type": m.content_type}
# )

# yatai endpoint
response =requests.post(
    "http://emotion-yatai.127.0.0.1.sslip.io/predict_async", data=m, headers={"Content-Type": m.content_type}
)


print(response.content)
