import asyncio
import aiohttp
from requests_toolbelt.multipart.encoder import MultipartEncoder

requests_count = 0

async def send_request():
    global requests_count
    form_data = aiohttp.FormData()
    form_data.add_field("annotations", '{"userId": 345786, "conferenceId": 890678, "clientFaceDetection": true}')
    form_data.add_field("image", open("test.png", "rb"), filename="test.png", content_type="image/png")
    async with aiohttp.ClientSession() as session:
        async with session.post("http://0.0.0.0:3000/predict_async", data=form_data) as response:
            response_code = response.status
            response_content = await response.content.read()
            print(f"Response code: {response_code}")
            if response_code == 200:
                print(f"Response content: {response_content}")
            requests_count += 1

async def main():
    try:
        tasks = []
        # Create 1000 concurrent tasks to send requests
        for _ in range(600):
            tasks.append(asyncio.create_task(send_request()))
        await asyncio.gather(*tasks)
        tasks = []
    except KeyboardInterrupt:
        pass
    finally:
        print(f"Number of requests sent: {requests_count}")

asyncio.run(main())