"""
Web Interface for Azure AI Agent Chat

This web application provides a user interface for interacting with the AI agent
through REST API calls to the agent service.

To run: python web_app.py
Web interface available at: http://127.0.0.1:8005
"""

import json
import logging
import os
from pathlib import Path
from typing import AsyncGenerator, Dict

import httpx
from fastapi import FastAPI, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
from fastapi.staticfiles import StaticFiles
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from otel import configure_oltp_grpc_tracing

tracer = configure_oltp_grpc_tracing(tracer_name="zava_web_app")
logger = logging.getLogger(__name__)

rls_users = {
    "00000000-0000-0000-0000-000000000000": "Head Office",
    "f47ac10b-58cc-4372-a567-0e02b2c3d479": "Seattle",
    "6ba7b810-9dad-11d1-80b4-00c04fd430c8": "Bellevue",
    "a1b2c3d4-e5f6-7890-abcd-ef1234567890": "Tacoma",
    "d8e9f0a1-b2c3-4567-8901-234567890abc": "Spokane",
    "3b9ac9fa-cd5e-4b92-a7f2-b8c1d0e9f2a3": "Everett",
    "e7f8a9b0-c1d2-3e4f-5678-90abcdef1234": "Redmond",
    "9c8b7a65-4321-fed0-9876-543210fedcba": "Kirkland",
    "2f4e6d8c-1a3b-5c7e-9f0a-b2d4f6e8c0a2": "Online",
}

# Agent service configuration
AGENT_SERVICE_URL = os.environ.get("services__dotnet-agent-app__http__0", "http://127.0.0.1:8006")  # noqa: SIM112 - naming controlled by aspire


class WebApp:
    """Handles all web interface functionality for the AI Agent Chat application."""

    def __init__(self, app: FastAPI) -> None:
        """Initialize the web interface with FastAPI app."""
        self.app = app

        self._setup_routes()
        self._setup_static_files()

    def _setup_static_files(self) -> None:
        """Setup static file serving."""
        # Use absolute path since parent navigation isn't working as expected
        static_dir = Path("static")
        self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    def _setup_routes(self) -> None:
        """Setup all web routes."""
        self.app.get("/", response_class=HTMLResponse)(self.get_chat_page)
        self.app.get("/favicon.ico", response_class=FileResponse)(self.get_favicon)
        self.app.post("/upload")(self.upload_file)
        self.app.get("/chat/stream")(self.stream_chat)
        self.app.delete("/chat/clear")(self.clear_chat)
        self.app.get("/files/{filename}")(self.serve_file)
        self.app.get("/health")(self.health_check)
        self.app.get("/agent/rls-users")(self.get_rls_users)

    async def get_chat_page(self) -> HTMLResponse:
        """Serve the chat HTML page."""
        html_file = Path("static/index.html")
        with html_file.open("r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())

    async def get_favicon(self) -> FileResponse:
        """Serve the favicon.ico file."""
        favicon_path = Path("static/favicon.ico")
        return FileResponse(favicon_path, media_type="image/x-icon")

    async def upload_file(self, file: UploadFile, message: str = Form(None)) -> Dict:
        """Handle file upload and extract text content."""
        try:
            # Check file size (10MB limit)
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:
                raise HTTPException(status_code=413, detail="File too large (max 10MB)")

            # Extract text based on file type
            file_text = ""
            file_extension = file.filename.lower().split(".")[-1] if file.filename and "." in file.filename else ""

            if file_extension in ["txt", "md"]:
                file_text = content.decode("utf-8")
            elif file_extension in ["pdf"]:
                # Could integrate PDF parsing
                file_text = f"[PDF file: {file.filename}]"
            elif file_extension in ["doc", "docx"]:
                # Could integrate Word parsing
                file_text = f"[Word document: {file.filename}]"
            else:
                file_text = f"[Uploaded file: {file.filename}]"

            # Prepare the message with file content
            if message:
                combined_message = f"{message}\n\nAttached file content:\n{file_text}"
            else:
                combined_message = f"Please analyze this file:\n\n{file_text}"

            return {"content": combined_message, "filename": file.filename}

        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {e}")
            return {"error": f"Error processing file: {e!s}"}

    async def stream_chat(
        self, message: str = "", session_id: str | None = None, rls_user_id: str | None = None
    ) -> StreamingResponse:
        """Stream chat responses by proxying to the agent service."""
        if not message.strip():
            return StreamingResponse(
                iter([f"data: {json.dumps({'error': 'Empty message'})}\n\n"]),
                media_type="text/event-stream",
            )

        # Validate RLS user ID is provided
        if not rls_user_id:
            return StreamingResponse(
                iter([f"data: {json.dumps({'error': 'RLS User ID is required'})}\n\n"]),
                media_type="text/event-stream",
            )

        # Get or create session - use provided session_id or default
        session_id = session_id or "default"

        return StreamingResponse(
            self._generate_stream(message, session_id, rls_user_id),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
                "Access-Control-Allow-Origin": "*",
                "Content-Encoding": "identity",
            },
        )

    async def _generate_stream(self, message: str, session_id: str, rls_user_id: str) -> AsyncGenerator[str, None]:
        """Generate streaming response by proxying to agent service."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Make request to agent service
                request_data = {"message": message, "session_id": session_id, "rls_user_id": rls_user_id}

                async with client.stream(
                    "POST",
                    f"{AGENT_SERVICE_URL}/chat/stream",
                    json=request_data,
                    headers={"Accept": "text/event-stream"},
                ) as response:
                    if response.status_code != 200:
                        yield f"data: {json.dumps({'error': f'Agent service error: {response.status_code}'})}\n\n"
                        return

                    assistant_message = ""
                    async for chunk in response.aiter_text():
                        if chunk.strip():
                            # Parse and forward each chunk
                            lines = chunk.strip().split("\n")
                            for line in lines:
                                if line.startswith("data: "):
                                    # Remove 'data: ' prefix
                                    data_str = line[6:]
                                    try:
                                        data = json.loads(data_str)

                                        # Convert agent service response format to web format
                                        if data.get("content"):
                                            assistant_message += data["content"]
                                            yield f"data: {json.dumps({'content': data['content']})}\n\n"
                                        elif data.get("file_info"):
                                            yield f"data: {json.dumps({'file': data['file_info']})}\n\n"
                                        elif data.get("error"):
                                            yield f"data: {json.dumps({'error': data['error']})}\n\n"
                                        elif data.get("done"):
                                            # Agent service signals completion
                                            break
                                    except json.JSONDecodeError:
                                        # Skip malformed JSON
                                        continue

            # Send completion signal
            yield "data: [DONE]\n\n"

        except httpx.RequestError as e:
            logger.error(f"Connection error to agent service: {e!s}")
            yield f"data: {json.dumps({'error': f'Connection error to agent service: {e!s}'})}\n\n"
        except Exception as e:
            logger.error(f"Streaming error: {e!s}")
            yield f"data: {json.dumps({'error': f'Streaming error: {e!s}'})}\n\n"

    async def clear_chat(self, request: Request) -> Dict:
        """Clear chat history and call agent service to delete thread for specific session."""
        session_id = "unknown"  # Initialize for error logging
        try:
            # Parse JSON body from the request
            request_data = await request.json()
            session_id = request_data.get("session_id", "default")
            rls_user_id = request_data.get("rls_user_id", "00000000-0000-0000-0000-000000000000")

            # Call agent service to clear thread for this session
            async with httpx.AsyncClient(timeout=60.0) as client:
                # Send as JSON body to match the ChatRequest model
                agent_request_data = {
                    "message": "",  # Required field in ChatRequest but not used for clear
                    "session_id": session_id,
                    "rls_user_id": rls_user_id,
                }
                response = await client.request("DELETE", f"{AGENT_SERVICE_URL}/chat/clear", json=agent_request_data)

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "status": "success",
                        "message": f"Chat session '{session_id}' cleared successfully",
                        "agent_response": result,
                    }
                return {"status": "error", "message": f"Agent service error: {response.status_code}"}
        except httpx.RequestError as e:
            logger.error("Connection error to agent service: %s", e)
            return {"status": "error", "message": f"Connection error to agent service: {e!s}"}
        except Exception as e:
            logger.error("Error clearing chat for session %s: %s", session_id, e)
            return {"status": "error", "message": f"Error clearing chat: {e!s}"}

    async def serve_file(self, filename: str) -> Response:
        """Proxy file serving to agent service or serve locally."""
        try:
            # Try to proxy to agent service first
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(f"{AGENT_SERVICE_URL}/files/{filename}")
                if response.status_code == 200:
                    # Determine content type based on file extension
                    file_extension = filename.lower().split(".")[-1] if "." in filename else ""
                    content_type_map = {
                        "png": "image/png",
                        "jpg": "image/jpeg",
                        "jpeg": "image/jpeg",
                        "gif": "image/gif",
                        "svg": "image/svg+xml",
                        "pdf": "application/pdf",
                        "txt": "text/plain",
                        "csv": "text/csv",
                        "json": "application/json",
                    }
                    content_type = content_type_map.get(file_extension, "application/octet-stream")

                    # Return content directly as bytes
                    return Response(
                        content=response.content,
                        media_type=content_type,
                        headers={"Content-Disposition": f"inline; filename={filename}"},
                    )

                # Agent service returned non-200 status
                raise HTTPException(
                    status_code=response.status_code, detail=f"Agent service error: {response.status_code}"
                )
        except HTTPException:
            # Re-raise HTTPExceptions to maintain proper error handling
            raise
        except Exception as err:
            logger.error("Error retrieving file from agent service: %s", err)
            raise HTTPException(status_code=500, detail="Error retrieving file from agent service") from err

    async def get_rls_users(self) -> Dict:
        """Get the list of available RLS users."""
        # Convert dictionary to list format expected by frontend
        users_list = [{"id": user_id, "name": name} for user_id, name in rls_users.items()]
        return {"status": "success", "users": users_list}

    async def health_check(self) -> Response:
        """Check health of web app and agent service."""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(f"{AGENT_SERVICE_URL}/health")
                if response.status_code == 200:
                    # Both web app and agent service are healthy
                    return Response(status_code=200)
                # Agent service is unhealthy
                logger.warning("Agent service health check failed with status: %d", response.status_code)
                return Response(status_code=503)
        except Exception as e:
            # Cannot reach agent service
            logger.error("Error checking health of agent service: %s", e)
            return Response(status_code=503)


# FastAPI app
app = FastAPI(title="Azure AI Agent Web Interface")
FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()  # Instrument httpx client for tracing

# Initialize web app
web_app = WebApp(app)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8005))
    logger.info("Starting web interface on port %d", port)
    logger.info("Agent service URL: %s", AGENT_SERVICE_URL)
    uvicorn.run(app, host="127.0.0.1", port=port)
