import asyncio
import aiohttp
from typing import Any, Dict, Callable, Awaitable
from loguru import logger
import traceback

class ConductorClient:
    def __init__(
        self,
        base_url: str,
        session: aiohttp.ClientSession = None,
        poll_interval: int = 0.5,
    ):
        self.base_url = base_url
        self.poll_interval = poll_interval
        self.session = session or aiohttp.ClientSession()

    async def poll_tasks(self, task_type: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/poll/batch/{task_type}?count=20"
        async with self.session.get(url) as response:
            if response.status != 200:
                return None
            return await response.json()

    async def update_task(
        self,
        task_id: str,
        workflowInstanceId: str,
        status: str,
        output: Dict[str, Any] = None,
    ) -> None:
        url = f"{self.base_url}/tasks"
        payload = {
            "taskId": task_id,
            "status": status,
            "output": output or {},
            "workflowInstanceId": workflowInstanceId,
        }
        async with self.session.post(url, json=payload) as response:
            logger.info(f"Update task response: {await response.text()}")

    async def close(self) -> None:
        await self.session.close()

    async def register_worker(
        self,
        task_type: str,
        task_handler: Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]],
    ) -> None:
        logger.info(f"Registering worker for task type: {task_type}")
        while True:
            try:
                tasks = await self.poll_tasks(task_type)
                if len(tasks):
                    for task in tasks:
                        task_id = task["taskId"]
                        workflowInstanceId = task["workflowInstanceId"]
                        try:
                            result = await task_handler(task)
                            await self.update_task(
                                task_id, workflowInstanceId, "COMPLETED", result
                            )
                        except Exception as e:
                            logger.error(f"Execute task {task_type} failed {str(e)}")
                            traceback.print_exc()
                            await self.update_task(
                                task_id, workflowInstanceId, "FAILED", {"error": str(e)}
                            )
                else:
                    await asyncio.sleep(
                        self.poll_interval
                    )  # 没有任务，等待一段时间再拉取
            except Exception as e:
                logger.error(f"Error occurred: {str(e)}")
                await asyncio.sleep(self.poll_interval)
