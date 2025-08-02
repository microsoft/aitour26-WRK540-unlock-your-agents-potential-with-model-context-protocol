"""
Web Interface for Azure AI Agent Chat

This web application provides a user interface for interacting with the AI agent
through REST API calls to the agent service.

To run: python web_app.py
Web interface available at: http://127.0.0.1:8005
"""

import json
import logging
import sys
from pathlib import Path
from typing import AsyncGenerator, Dict

# Add workshop folder to path to import shared modules
sys.path.append(str(Path(__file__).parent.parent / "workshop"))

import httpx
from fastapi import FastAPI, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from utilities import Utilities

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Agent service configuration
AGENT_SERVICE_URL = "http://127.0.0.1:8006"


class WebApp:
    """Handles all web interface functionality for the AI Agent Chat application."""
    
    def __init__(self, app: FastAPI) -> None:
        """Initialize the web interface with FastAPI app."""
        self.app = app
        self.utilities = Utilities()
        
        self._setup_routes()
        self._setup_static_files()
    
    def _setup_static_files(self) -> None:
        """Setup static file serving."""
        # Use absolute path since parent navigation isn't working as expected
        static_dir = Path("/workspace/src/shared/static")
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
    
    async def get_chat_page(self) -> HTMLResponse:
        """Serve the chat HTML page."""
        html_file = Path("/workspace/src/shared/static/index.html")
        with html_file.open("r") as f:
            return HTMLResponse(content=f.read())
    
    async def get_favicon(self) -> FileResponse:
        """Serve the favicon.ico file."""
        favicon_path = Path("/workspace/src/shared/static/favicon.ico")
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
            file_extension = (
                file.filename.lower().split(".")[-1] if file.filename and "." in file.filename else ""
            )

            if file_extension in ["txt", "md"]:
                file_text = content.decode("utf-8")
            elif file_extension in ["pdf"]:
                file_text = f"[PDF file: {file.filename}]"  # Could integrate PDF parsing
            elif file_extension in ["doc", "docx"]:
                file_text = f"[Word document: {file.filename}]"  # Could integrate Word parsing
            else:
                file_text = f"[Uploaded file: {file.filename}]"

            # Prepare the message with file content
            if message:
                combined_message = f"{message}\n\nAttached file content:\n{file_text}"
            else:
                combined_message = f"Please analyze this file:\n\n{file_text}"

            return {"content": combined_message, "filename": file.filename}

        except Exception as e:
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
                                    data_str = line[6:]  # Remove 'data: ' prefix
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
            yield f"data: {json.dumps({'error': f'Connection error to agent service: {e!s}'})}\n\n"
        except Exception as e:
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
            return {
                "status": "error", 
                "message": f"Connection error to agent service: {e!s}"
            }
        except Exception as e:
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
        except Exception:
            pass
        
        # Fallback to local file serving
        files_dir = Path(self.utilities.shared_files_path) / "files"
        file_path = files_dir / filename
        
        if not file_path.exists() or not file_path.is_file():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Security check: ensure the file is within the files directory
        try:
            file_path.resolve().relative_to(files_dir.resolve())
        except ValueError as exc:
            raise HTTPException(status_code=403, detail="Access denied") from exc
        
        return FileResponse(path=str(file_path))
    
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
            return {
                **web_status,
                "agent_service": {"status": "error", "error": str(e)}
            }


# FastAPI app
app = FastAPI(title="Azure AI Agent Web Interface")

# Initialize web app
web_app = WebApp(app)


if __name__ == "__main__":
    import uvicorn

    print("Starting web interface...")
    print(f"Agent service URL: {AGENT_SERVICE_URL}")
    uvicorn.run(app, host="127.0.0.1", port=8005)
