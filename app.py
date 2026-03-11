from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from openai import OpenAI
import base64
import io

# Initialize the OpenAI client to connect to the local Ollama server
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

def encode_image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to a base64 string for API consumption"""
    try:
        return base64.b64encode(image_bytes).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image: {e}")
        return ""

async def ask_ollama_model(image_bytes: bytes, question: str, model: str = "gemma3:4b") -> str:
    """Ask a question about an image using Ollama via OpenAI-compatible API"""
    base64_image = encode_image_to_base64(image_bytes)
    if not base64_image:
        return "Failed to encode image"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}" # Assuming JPEG. For more robust solution, detect image type.
                            }
                        }
                    ]
                }
            ],
            max_tokens=512,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API Error: {e}")
        return f"Error: {e}"

# Initialize the FastAPI application
app = FastAPI()

# Mount the static directory to serve static files (like index.html and style.css)
app.mount("/static", StaticFiles(directory="receipt_ocr_app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the index.html file"""
    # Ensure the path is correct relative to where the app is run
    html_file_path = Path("receipt_ocr_app/static/index.html")
    if not html_file_path.exists():
        return HTMLResponse(content="Error: index.html not found", status_code=404)
    return html_file_path.read_text()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    """Handle image uploads, process them with the gemma3:4b model, and return the results."""
    if not file.content_type.startswith("image/"):
        return JSONResponse(status_code=400, content={"detail": "Only image files are allowed."})

    image_bytes = await file.read()

    # Ask the two questions to the Ollama model
    extracted_text = await ask_ollama_model(image_bytes, "Extract all the text from the image.", "gemma3:4b")
    accuracy_check = await ask_ollama_model(image_bytes, "Check that the receipt is accurate.", "gemma3:4b")

    return JSONResponse(content={
        "extracted_text": extracted_text,
        "accuracy_check": accuracy_check
    })
