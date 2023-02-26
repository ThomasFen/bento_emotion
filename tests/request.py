import argparse
import asyncio
import aiohttp
from requests_toolbelt.multipart.encoder import MultipartEncoder

async def send_request(url):
    form_data = aiohttp.FormData()
    form_data.add_field("annotations", '{"userId": 345786, "conferenceId": 890678, "clientFaceDetection": true}')
    form_data.add_field("image", open("test.png", "rb"), filename="test.png", content_type="image/png")
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=form_data) as response:
            response_code = response.status
            response_content = await response.content.read()
            print(f"Response code: {response_code}")
            if response_code == 200:
                print(f"Response content: {response_content}")

async def main(url, num_requests, send_one_by_one):
    try:
        if send_one_by_one:
            for i in range(num_requests):
                await send_request(url)
        else:
            tasks = []
            # Create `num_requests` concurrent tasks to send requests
            for _ in range(num_requests):
                tasks.append(asyncio.create_task(send_request(url)))
            await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="the URL to send the requests to")
    parser.add_argument("num_requests", type=int, help="the number of requests to send")
    parser.add_argument("--one-by-one", action="store_true", help="send requests one by one instead of at once")
    args = parser.parse_args()

    asyncio.run(main(args.url, args.num_requests, args.one_by_one))
