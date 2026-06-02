import json
import uuid

from typing import Any

import pika
from dataclasses import dataclass


class RpcTimeoutError(RuntimeError):
    pass


@dataclass(frozen=True)
class RpcRequest:
    action: str
    payload: dict[str, Any]


class RabbitRpcClient:
    def __init__(self, rabbitmq_url: str, queue: str, timeout_seconds: int) -> None:
        self.rabbitmq_url = rabbitmq_url
        self.queue = queue
        self.timeout_seconds = timeout_seconds

    def call(self, request: RpcRequest) -> dict[str, Any]:
        connection = pika.BlockingConnection(
            pika.URLParameters(self.rabbitmq_url)
            )

        try:
            channel = connection.channel()
            result = channel.queue_declare(queue="", exclusive=True)
            callback_queue = result.method.queue
            

            correlation_id = str(uuid.uuid4())

            response: dict[str, Any] = {}

            def on_response(_ch: Any, _method: Any, props: Any, body: bytes) -> None:
                if props.correlation_id == correlation_id:
                    response["body"] = json.loads(body.decode("utf-8"))

            channel.basic_consume(
                queue=callback_queue, on_message_callback=on_response, auto_ack=True
            )
            channel.basic_publish(
                exchange="",
                routing_key=self.queue,
                properties=pika.BasicProperties(
                    reply_to=callback_queue,
                    correlation_id=correlation_id,
                    content_type="application/json",
                ),
                body=json.dumps({"action": request.action, "payload": request.payload}).encode("utf-8"),
            )
            connection.process_data_events(time_limit=self.timeout_seconds)
            if "body" not in response:
                raise RpcTimeoutError("database lookup timed out")
            return response["body"]
        finally:
            connection.close()
