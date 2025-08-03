# Ollama Vision Agent

A Flask-based application that provides AI-powered vision operations using LLaVA model through Ollama. 

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (for running Ollama)

## Hosting Ollama with Docker

Ollama is used to run the LLaVA model locally for image description.

1. **Start the Ollama Docker container:**
   ```bash
   docker run -d --name ollama \
     -p 11434:11434 \
     -v ollama_data:/root/.ollama \
     ollama/ollama
   ```
   Ollama will now be accessible at `http://localhost:11434`

2. **Pull the `llava:7b` model:**
   From running docker container execute the following command.
   ```bash
   ollama pull llava:7b
   ```

3. **Test the model:**
   Once the `llava:7b` model is pulled, you can test it with the following cURL command:
   ```bash
   curl http://localhost:11434/api/chat -d '{
     "model": "llava:7b",
     "messages": [
       {
         "role": "user", 
         "content": "What is in this image?",
         "images": ["iVBORw0KGgoAAAANSUhEUgAAAG...base64_image_data"]
       }
     ]
   }'
   ```

### Flask App Setup

1. **Clone/Navigate to the repository**
   ```bash
   cd ollama-vision-service
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.lock.txt
   ```

4. **Environment Configuration**
   The application uses a `.env` file for configuration. Default values:
   ```env
   OLLAMA_API_BASE=http://localhost:11434
   OLLAMA_MODEL=llava:7b
   FLASK_PORT=5006
   ```

### Running the Flask App

```bash
python app.py
```

The API will be available at `http://localhost:5006`

## API Usage

### Describe Image Endpoint

**POST** `/describe`

Upload an image file and receive an AI-generated description.

#### Request
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: Form data with `image` field containing the image file

### OCR Image Endpoint

**POST** `/ocr`

Upload an image file and extract all visible text using AI-powered OCR.

#### Request
- **Method**: POST
- **Content-Type**: multipart/form-data
- **Body**: Form data with `image` field containing the image file

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OLLAMA_API_BASE` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | LLaVA model name | `llava:7b` |
| `FLASK_PORT` | Flask server port | `5006` |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
