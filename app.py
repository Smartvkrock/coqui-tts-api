from flask import Flask, request, send_file
from TTS.api import TTS
import os
import uuid

app = Flask(__name__)

# Load TTS model (lightweight English model)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

@app.route('/generate', methods=['POST'])
def generate_voice():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return {"error": "No text provided"}, 400
        
        # Generate unique filename
        filename = f"/tmp/{uuid.uuid4()}.wav"
        
        # Generate speech
        tts.tts_to_file(text=text, file_path=filename)
        
        # Send file
        return send_file(filename, mimetype='audio/wav')
    
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/health', methods=['GET'])
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
