import os
from vastai import VastAPIClient
from dotenv import load_dotenv

load_dotenv()

vast_ai_apikey = os.getenv("VAST_AI_API_KEY")
vast_ai_client = VastAPIClient(vast_ai_apikey)

instances =  vast_ai_client.list_available_instances(
    disk_space=100,
    gpu_total_ram=40960,
    gpu_ram=40960
)
for instance in instances:
    print(instance)
