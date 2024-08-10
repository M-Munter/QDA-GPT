import logging
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from qda_gpt.views import run_analysis_async

logger = logging.getLogger(__name__)

def truncate_message(message, max_length=100):
    return (message[:max_length] + '...') if len(message) > max_length else message

class AnalysisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.debug("WebSocket connection accepted\n")
        print()

    async def disconnect(self, close_code):
        logger.debug("WebSocket connection closed\n")
        print()

    async def receive_json(self, content):
        logger.debug("Entered receive_json method\n")
        logger.debug(f"Received JSON: {truncate_message(str(content))}\n")
        print()
        try:
            analysis_data = content.get('analysis_data')
            if analysis_data:
                logger.debug(f"Starting analysis: {truncate_message(str(analysis_data))}\n")
                print()
                result = await run_analysis_async(analysis_data)
                logger.debug(f"Analysis result: {truncate_message(str(result))}\n")
                await self.send_json(result)
            else:
                logger.debug("No analysis data found in received JSON\n")
                print()
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}\n")
            print()
            await self.send_json({'error': 'Invalid JSON format'})
        except Exception as e:
            logger.error(f"Error processing JSON: {e}\n")
            print()
            await self.send_json({'error': str(e)})

    async def run_analysis(self, event):
        logger.debug("run_analysis called\n")
        print()
        analysis_data = event['analysis_data']
        result = await run_analysis_async(analysis_data)
        await self.send_json(result)


    async def send_json(self, content):
        logger.debug("send_json called\n")
        try:
            if not isinstance(content, dict):
                raise ValueError("Content to be sent is not a dictionary")
            json_content = json.dumps(content)
            logger.debug(f"Serialized JSON content: {json_content}\n")
            await self.send(text_data=json_content)
        except (TypeError, ValueError) as e:
            logger.error(f"Error serializing JSON data: {e}\nContent: {content}\n")
            await self.send_message({'error': 'Error serializing JSON data', 'details': str(e)})
        except Exception as e:
            logger.error(f"Error sending JSON data: {e}\nSerialized Content: {json_content}\n")
            await self.send_message({'error': 'Error sending JSON data', 'details': str(e)})

    async def send_analysis_result(self, event):
        await self.send_json(event["content"])

    async def receive(self, text_data):
        print("######### WebSocket Message Received #########")
        print(f"Received data: {text_data}")
        logger.debug(f"Text message received: {text_data}")
        print(f"Text message received: {text_data}")
        # Simple response for testing
        await self.send(text_data=json.dumps({"message": "Hello, world!"}))

