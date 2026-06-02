import argparse
import json
from pathlib import Path
from typing import Any

from safety_backend.app import create_app

DEFAULT_OPENAPI_VERSION = "3.0.3"


def build_openapi(
    *,
    backend_url: str | None = None,
    title: str | None = None,
    version: str | None = None,
    deadline: float | None = None,
) -> dict[str, Any]:
    app = create_app()
    app.openapi_version = DEFAULT_OPENAPI_VERSION
    document = app.openapi()
    document["openapi"] = DEFAULT_OPENAPI_VERSION

    if title:
        document["info"]["title"] = title
    if version:
        document["info"]["version"] = version

    if backend_url:
        document["x-google-backend"] = {
            "address": backend_url.rstrip("/"),
            "path_translation": "APPEND_PATH_TO_ADDRESS",
        }
        if deadline is not None:
            document["x-google-backend"]["deadline"] = deadline

    document["x-google-allow"] = "configured"
    return document


def write_openapi(document: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GCP API Gateway OpenAPI spec.")
    parser.add_argument(
        "--backend-url",
        help="Public HTTPS backend URL that GCP API Gateway forwards to.",
    )
    parser.add_argument(
        "--output",
        default="build/openapi-gateway.json",
        help="Output path. Defaults to build/openapi-gateway.json.",
    )
    parser.add_argument("--title", help="Override OpenAPI title.")
    parser.add_argument("--version", help="Override OpenAPI version.")
    parser.add_argument("--deadline", type=float, help="GCP API Gateway backend deadline seconds.")
    args = parser.parse_args()

    document = build_openapi(
        backend_url=args.backend_url,
        title=args.title,
        version=args.version,
        deadline=args.deadline,
    )
    write_openapi(document, Path(args.output))


if __name__ == "__main__":
    main()
