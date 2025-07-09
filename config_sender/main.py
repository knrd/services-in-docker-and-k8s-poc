import asyncio
import uuid
import os
import logging
from aio_pika import connect, Message, ExchangeType

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    logger.info("Connecting to RabbitMQ")
    connection = await connect(os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/"))
    logger.info("Connected to RabbitMQ")
    logger.info("Simulating delay for connection testing")
    await asyncio.sleep(3)
    channel = await connection.channel()
    exchange = await channel.declare_exchange("config_exchange", ExchangeType.DIRECT)
    queue = await channel.declare_queue("config_requests")
    await queue.bind(exchange, routing_key="request")

    async with queue.iterator() as queue_iter:
        logger.info("Listening for incoming messages...")
        async for message in queue_iter:
            async with message.process():
                logger.info("Processing message")
                name = message.body.decode()
                reply_name = f"reply-to-{name}"
                registered_id = str(uuid.uuid4())
                
                reply_queue = message.reply_to
                if reply_queue:
                    response = f"{reply_name},{registered_id}"
                    logger.info(f"Sending response: {response} to {reply_queue}")
                    await exchange.publish(
                        Message(body=response.encode(), correlation_id=message.correlation_id),
                        routing_key=reply_queue
                    )
                    logger.info("Response sent successfully")

if __name__ == "__main__":
    asyncio.run(main())
