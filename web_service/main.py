import asyncio
import uuid
import os
import logging
from aiohttp import web
from aio_pika import connect, Message, ExchangeType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

config = {"reply_name": "", "registered_id": ""}

async def fetch_config():
    retry_interval = 5
    while True:
        try:
            logger.info("Attempting to connect to RabbitMQ")
            connection = await connect(os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/"))
            logger.info("Successfully connected to RabbitMQ")
            break
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}, retrying in {retry_interval}s...")
            await asyncio.sleep(retry_interval)

    channel = await connection.channel()
    queue = await channel.declare_queue("config_requests")
    exchange = await channel.declare_exchange("config_exchange", ExchangeType.DIRECT)
    await queue.bind(exchange, routing_key="request")
    
    reply_queue = await channel.declare_queue(exclusive=True)
    await reply_queue.bind(exchange, routing_key=reply_queue.name)
    
    correlation_id = str(uuid.uuid4())
    logger.info("Generated correlation_id: %s", correlation_id)
    await exchange.publish(
        Message(
            body=os.getenv("SRV_WEB_NAME", "web-service").encode(),
            reply_to=reply_queue.name,
            correlation_id=correlation_id
        ),
        routing_key="request"
    )
    
    async with reply_queue.iterator() as queue_iter:
        logger.info("Waiting for configuration reply...")
        async for message in queue_iter:
            async with message.process():
                logger.info("Processing message with correlation_id: %s", message.correlation_id)
                if message.correlation_id == correlation_id:
                    reply_name, registered_id = message.body.decode().split(",")
                    config.update(reply_name=reply_name, registered_id=registered_id)
                    logger.info("Received configuration: %s", config)
                    return

async def status_handler(request):
    return web.json_response({
        "reply_name": config["reply_name"],
        "registered_id": config["registered_id"]
    })

async def start_background_tasks(app):
    app["config_fetcher"] = asyncio.create_task(fetch_config())

async def cleanup_background_tasks(app):
    app["config_fetcher"].cancel()
    await app["config_fetcher"]

app = web.Application()
app.add_routes([web.get("/status", status_handler)])
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)


if __name__ == "__main__":
    web.run_app(app, port=8080)
