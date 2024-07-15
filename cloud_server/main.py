import os, json, requests
from dotenv import load_dotenv
from flask import Flask
from loguru import logger

load_dotenv()

# Init Flask app
app = Flask(__name__)

conductor_base_url = os.getenv("CONDUCTOR_BASE_URL", "http://localhost:8080/api")

with open("./tasks.json", encoding="utf-8") as f:
    task_json = json.load(f)

with open("./workflow.json", encoding="utf-8") as f:
    workflow_json = json.load(f)


@app.route("/api/whisper-inference", methods=["POST"])
def run_whisper_inference():
    workflow_name = workflow_json["name"]
    r = requests.post(
        f"{conductor_base_url}/workflow",
        json={
            "name": workflow_name,
            "version": 1,
            "input": {
                "video_url": "https://www.learningcontainer.com/wp-content/uploads/2020/05/sample-mp4-file.mp4",
                "model_instance_id": "60f2e9c1b1a1d50001",
            },
        },
    )


def init_conductor_workflow_and_tasks():
    r = requests.post(f"{conductor_base_url}/metadata/taskdefs", json=task_json)
    r.raise_for_status()
    logger.info(f"Tasks created successfully.")

    r = requests.put(f"{conductor_base_url}/metadata/workflow", json=[workflow_json])
    r.raise_for_status()
    logger.info("Workflow created successfully.")


if __name__ == "__main__":
    init_conductor_workflow_and_tasks()
    app.run(port=5000)
