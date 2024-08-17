import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from qda_gpt.views import run_analysis_async

logger = logging.getLogger(__name__)

class AnalysisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Handle the WebSocket connection and join the analysis group
        await self.channel_layer.group_add("analysis_group", self.channel_name)
        await self.accept()
        logger.debug("WebSocket connection accepted\n")

    async def disconnect(self, close_code):
        # Handle WebSocket disconnection and leave the analysis group
        await self.channel_layer.group_discard("analysis_group", self.channel_name)

    async def receive(self, text_data):
        # Handle incoming data from WebSocket and log the received data
        data = json.loads(text_data)


    async def run_analysis(self, event):
        # Triggered by an event to run the analysis
        analysis_data = event['analysis_data']

        # Perform the asynchronous analysis task
        result = await run_analysis_async(analysis_data)

        # Send the analysis result back to the WebSocket group
        await self.channel_layer.group_send(
            "analysis_group",
            {
                "type": "send_analysis_result",
                "content": result,  # Include the analysis result in the event content
            }
        )

    async def send_analysis_result(self, event):
        # Send the analysis result to the WebSocket client
        content = event['content']
        # Send the content as JSON over the WebSocket connection
        await self.send(text_data=json.dumps(content))

