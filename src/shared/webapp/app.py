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
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.propagate import inject
from otel import configure_oltp_grpc_tracing

tracer = configure_oltp_grpc_tracing(tracer_name="zava_web_app")
logger = logging.getLogger(__name__)

# Agent service configuration
AGENT_SERVICE_URL = os.environ.get(
    "services__python-agent-app__http__0", "http://127.0.0.1:8006")  # noqa: SIM112 - naming controlled by aspire


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
        self.app.mount(
            "/static", StaticFiles(directory=str(static_dir)), name="static")

    def _setup_routes(self) -> None:
        """Setup all web routes."""
        self.app.get("/", response_class=HTMLResponse)(self.get_chat_page)
        self.app.get("/favicon.ico",
                     response_class=FileResponse)(self.get_favicon)
        self.app.post("/upload")(self.upload_file)
        self.app.get("/chat/stream")(self.stream_chat)
        self.app.delete("/chat/clear")(self.clear_chat)
        self.app.get("/files/{filename}")(self.serve_file)
        self.app.get("/health")(self.health_check)

    async def get_chat_page(self) -> HTMLResponse:
        """Serve the chat HTML page."""
        html_file = Path("static/index.html")
        with html_file.open("r") as f:
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
                raise HTTPException(
                    status_code=413, detail="File too large (max 10MB)")

            # Extract text based on file type
            file_text = ""
            file_extension = (
                file.filename.lower().split(
                    ".")[-1] if file.filename and "." in file.filename else ""
            )

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

    async def stream_chat(self, message: str = "", session_id: str | None = None) -> StreamingResponse:
        """Stream chat responses by proxying to the agent service."""
        if not message.strip():
            return StreamingResponse(
                iter([f"data: {json.dumps({'error': 'Empty message'})}\n\n"]),
                media_type="text/event-stream",
            )

        # Get or create session - use provided session_id or default
        session_id = session_id or "default"

        return StreamingResponse(
            self._generate_stream(message, session_id),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
                "Access-Control-Allow-Origin": "*",
                "Content-Encoding": "identity"
            },
        )

    async def _generate_stream(self, message: str, session_id: str) -> AsyncGenerator[str, None]:
        """Generate streaming response by proxying to agent service."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                # Make request to agent service
                request_data = {
                    "message": message,
                    "session_id": session_id
                }

                async with client.stream(
                    "POST",
                    f"{AGENT_SERVICE_URL}/chat/stream",
                    json=request_data,
                    headers={"Accept": "text/event-stream"}
                ) as response:
                    if response.status_code != 200:
                        yield f"data: {json.dumps({'error': f'Agent service error: {response.status_code}'})}\n\n"
                        return

                    assistant_message = ""
                    async for chunk in response.aiter_text():
                        if chunk.strip():
                            # Parse and forward each chunk
                            lines = chunk.strip().split('\n')
                            for line in lines:
                                if line.startswith('data: '):
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

    async def clear_chat(self, session_id: str = "default") -> Dict:
        """Clear chat history and call agent service to delete thread for specific session."""
        try:
            # Call agent service to clear thread for this session
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.delete(
                    f"{AGENT_SERVICE_URL}/chat/clear",
                    params={"session_id": session_id}
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "status": "success",
                        "message": f"Chat session '{session_id}' cleared successfully",
                        "agent_response": result
                    }
                return {
                    "status": "error",
                    "message": f"Agent service error: {response.status_code}"
                }
        except httpx.RequestError as e:
            logger.error("Connection error to agent service: %s", e)
            return {
                "status": "error",
                "message": f"Connection error to agent service: {e!s}"
            }
        except Exception as e:
            logger.error(
                "Error clearing chat for session %s: %s", session_id, e)
            return {
                "status": "error",
                "message": f"Error clearing chat: {e!s}"
            }

    async def serve_file(self, filename: str) -> FileResponse:
        """Proxy file serving to agent service or serve locally."""
        try:
            # Try to proxy to agent service first
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(f"{AGENT_SERVICE_URL}/files/{filename}")
                if response.status_code == 200:
                    # Save file temporarily and serve it
                    temp_file = Path("/tmp") / filename
                    with temp_file.open("wb") as f:
                        f.write(response.content)
                    return FileResponse(path=str(temp_file))
        except Exception as err:
            logger.error("Error retrieving file from agent service: %s", err)
            raise HTTPException(
                status_code=500, detail="Error retrieving file from agent service") from err

    async def health_check(self) -> Dict:
        """Check health of web app and agent service."""
        web_status = {"status": "healthy", "service": "web_interface"}

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.get(f"{AGENT_SERVICE_URL}/health")
                if response.status_code == 200:
                    agent_status = response.json()
                    return {
                        **web_status,
                        "agent_service": agent_status
                    }
                return {
                    **web_status,
                    "agent_service": {"status": "error", "code": response.status_code}
                }
        except Exception as e:
            logger.error("Error checking health of agent service: %s", e)
            return {
                **web_status,
                "agent_service": {"status": "error", "error": str(e)}
            }


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
