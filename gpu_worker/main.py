import os
from loguru import logger
from dotenv import load_dotenv
from conductor.client.worker.worker_task import worker_task
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from vastai import VastAPIClient

load_dotenv()

vast_ai_apikey = os.getenv("VAST_AI_API_KEY")
vast_ai_client = VastAPIClient(vast_ai_apikey)


@worker_task(task_definition_name="whisper_inference", worker_id="whisper_inference_worker")
def whisper_inference(task):
    task_id = task.task_id
    input_data = task.input_data
    video_path = input_data.get("video_path")
    logger.info("Start running whisper inference, video_path: {}".format(video_path))
    if not video_path:
        raise ValueError("video_path is required")
    return {"video_path": video_path}


def main():
    api_config = Configuration(
        debug=True,
    )
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    # start worker polling
    task_handler.start_processes()


if __name__ == "__main__":
    main()
