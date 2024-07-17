import os, time
from loguru import logger
from conductor.client.worker.worker_task import worker_task
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from moviepy.video.io.VideoFileClip import VideoFileClip
from concurrent.futures import ProcessPoolExecutor
from pydub import AudioSegment

output_folder = "./outputs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)


def split_audio(file_path, start_time, end_time, output_path):
    audio = AudioSegment.from_mp3(file_path)
    segment = audio[start_time:end_time]
    segment.export(output_path, format="mp3")


def split_audio_concurrent(file_path, seconds_per_chunk, output_folder):
    audio = AudioSegment.from_mp3(file_path)
    segment_length_ms = (
        seconds_per_chunk * 1000
    )  # Convert segment length to milliseconds
    total_length_ms = len(audio)
    num_segments = total_length_ms // segment_length_ms

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    start = time.time()
    tasks = []
    with ProcessPoolExecutor() as executor:
        for i in range(num_segments + 1):
            start_time = i * segment_length_ms
            end_time = min((i + 1) * segment_length_ms, total_length_ms)
            output_path = f"{output_folder}/segment_{i+1}.mp3"
            tasks.append(
                executor.submit(
                    split_audio_concurrent, file_path, start_time, end_time, output_path
                )
            )

        for task in tasks:
            task.result()

    end = time.time()
    logger.info(f"Splitting audio took {end - start} seconds")
    segment_files = [
        os.path.join(os.path.dirname(__file__), f"{output_folder}/segment_{i+1}.mp4")
        for i in range(num_segments)
    ]
    return segment_files


@worker_task(task_definition_name="split_audio_into_chunks")
def split_audio_into_chunks(task):
    task_id = task.task_id
    input_data = task.input_data
    audio_path = input_data.get("audio_path")
    if not audio_path:
        raise ValueError("audio_path is required")
    seconds_per_chunk = input_data.get("seconds_per_chunk", 60)

    logger.info(
        "Start splitting video into chunks, audio_path: {}, seconds_per_chunk: {}".format(
            audio_path, seconds_per_chunk
        )
    )
    task_output_folder = f"{output_folder}/{task_id}"
    segment_files = split_audio_concurrent(
        audio_path, seconds_per_chunk, task_output_folder
    )
    dynamic_tasks = []
    dynamic_tasks_input = {}

    for i, segment_file in enumerate(segment_files):
        task_ref_name = f"whisper_inference_{i}"
        dynamic_tasks.append(
            {"name": "whisper_inference", "taskReferenceName": task_ref_name}
        )
        dynamic_tasks_input[task_ref_name] = {"audio_path": segment_file}

    return {
        "dynamicTasks": dynamic_tasks,
        "dynamicTasksInput": dynamic_tasks_input,
    }


def main():
    api_config = Configuration()
    task_handler = TaskHandler(
        workers=[],
        configuration=api_config,
        scan_for_annotated_workers=True,
    )
    # start worker polling
    task_handler.start_processes()


if __name__ == "__main__":
    main()
