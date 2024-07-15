import os, time
from loguru import logger
from conductor.client.worker.worker_task import worker_task
from conductor.client.automator.task_handler import TaskHandler
from conductor.client.configuration.configuration import Configuration
from moviepy.video.io.VideoFileClip import VideoFileClip
from concurrent.futures import ProcessPoolExecutor

output_folder = "./outputs"
if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)


def split_segment(input_path, start_time, end_time, output_path):
    video = VideoFileClip(input_path)
    segment = video.subclip(start_time, end_time)
    segment.write_videofile(output_path, codec="libx264")
    video.close()
    print(f"Segment saved to {output_path}")


def split_video_concurrent(input_path, seconds_per_chunk, output_folder):
    video = VideoFileClip(input_path)
    duration = video.duration
    num_segments = int(duration // seconds_per_chunk) + 1

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    start = time.time()
    tasks = []
    with ProcessPoolExecutor() as executor:
        for i in range(num_segments):
            start_time = i * seconds_per_chunk
            end_time = min((i + 1) * seconds_per_chunk, duration)
            output_path = f"{output_folder}/segment_{i+1}.mp4"
            tasks.append(
                executor.submit(
                    split_segment, input_path, start_time, end_time, output_path
                )
            )

        for task in tasks:
            task.result()

    video.close()
    end = time.time()
    logger.info(f"Splitting video took {end - start} seconds")
    segment_files = [
        os.path.join(os.path.dirname(__file__), f"{output_folder}/segment_{i+1}.mp4")
        for i in range(num_segments)
    ]
    return segment_files


@worker_task(task_definition_name="split_video_into_chunks")
def split_video_into_chunks(task):
    # task_id = task.task_id
    task_id = "2e9008c8-e6fb-4082-8e4b-e8180521d64a"
    input_data = task.input_data
    video_path = input_data.get("video_path")
    if not video_path:
        raise ValueError("video_path is required")
    seconds_per_chunk = input_data.get("seconds_per_chunk", 60)

    logger.info(
        "Start splitting video into chunks, video_path: {}, seconds_per_chunk: {}".format(
            video_path, seconds_per_chunk
        )
    )
    task_output_folder = f"{output_folder}/{task_id}"

    # segment_files = split_video_concurrent(
    #     video_path, seconds_per_chunk, task_output_folder
    # )
    segment_files = [
        os.path.join(os.path.dirname(__file__), task_output_folder, file)
        for file in os.listdir(task_output_folder)
    ]
    dynamic_tasks = []
    dynamic_tasks_input = {}

    for i, segment_file in enumerate(segment_files):
        task_ref_name = f"whisper_inference_{i}"
        dynamic_tasks.append(
            {"name": "whisper_inference", "taskReferenceName": task_ref_name}
        )
        dynamic_tasks_input[task_ref_name] = {"video_path": segment_file}

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
