import asyncio
import os
from loguru import logger
from dotenv import load_dotenv
from conductor_client import ConductorClient
from vastai import VastAPIClient

load_dotenv()

vast_ai_apikey = os.getenv("VAST_AI_API_KEY")
vast_ai_client = VastAPIClient(vast_ai_apikey)
conductor_base_url = os.getenv("CONDUCTOR_BASE_URL", "http://localhost:8080/api")


async def whisper_inference(task):
    input_data = task.get("inputData")
    video_path = input_data.get("video_path")
    logger.info("Start running whisper inference, video_path: {}".format(video_path))
    if not video_path:
        raise ValueError("video_path is required")
    return {"video_path": video_path}


async def main():
    conductor_client = ConductorClient(base_url=conductor_base_url)
    await conductor_client.register_worker("whisper_inference", whisper_inference)


if __name__ == "__main__":
    asyncio.run(main())
