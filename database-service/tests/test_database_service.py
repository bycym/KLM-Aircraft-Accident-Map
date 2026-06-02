from safety_database.lambda_handler import lambda_handler




def test_lambda_handler_returns_json_response(monkeypatch) -> None:
    class Handler:
        def handle(self, request):
            assert request == {"action": "years", "payload": {}}
            return {"years": [2019]}

    monkeypatch.setattr("safety_database.lambda_handler._handler", Handler())

    response = lambda_handler({"action": "years", "payload": {}}, None)

    assert response["statusCode"] == 200
    assert response["body"] == '{"years": [2019]}'
