import json
from typing import Any
import boto3
from safety_backend.rpc import RpcRequest, RpcTimeoutError


class LambdaDatabaseClient:
    def __init__(self, function_name: str) -> None:

        self.function_name = function_name

        self.client = boto3.client("lambda")

    def call(self, request: RpcRequest) -> dict[str, Any]:
        response = self.client.invoke(
            FunctionName=self.function_name,
            InvocationType="RequestResponse",
            Payload=json.dumps({"action": request.action, "payload": request.payload}).encode("utf-8"),
        )
        status_code = int(response.get("StatusCode", 0))
        if status_code >= 500:
            raise RpcTimeoutError("database lambda invocation failed")
        payload = json.loads(response["Payload"].read().decode("utf-8"))
        if "statusCode" in payload:
            if int(payload["statusCode"]) >= 500:
                raise RpcTimeoutError("database lambda returned an error")
            return json.loads(payload.get("body") or "{}")
        return payload
