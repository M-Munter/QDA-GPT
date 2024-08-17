import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from qda_gpt.views import run_analysis_async

logger = logging.getLogger(__name__)


class AnalysisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the group
        await self.channel_layer.group_add("analysis_group", self.channel_name)
        await self.accept()
        logger.debug("WebSocket connection accepted\n")

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard("analysis_group", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

    async def run_analysis(self, event):
        analysis_data = event['analysis_data']

        # Perform the analysis
        result = await run_analysis_async(analysis_data)

        # Send the result back to the group
        await self.channel_layer.group_send(
            "analysis_group",
            {
                "type": "send_analysis_result",
                "content": result,
            }
        )

    async def send_analysis_result(self, event):
        content = event['content']
        # Send the content as JSON over WebSocket
        await self.send(text_data=json.dumps(content))

