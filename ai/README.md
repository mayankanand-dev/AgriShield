# AgriShield AI Service

AI-powered inference service for crop monitoring, risk assessment, yield prediction, and farm advisory.

## Features

- **Crop Health Detection**: Detect crop diseases and health issues from images
- **Damage Assessment**: Quantify crop damage from weather events  
- **Yield Prediction**: Predict expected crop yield based on farm context
- **Risk Scoring**: Calculate insurance risk scores
- **Soil OCR**: Extract soil nutrient data from reports
- **Agricultural Advisory**: Generate recommendations based on farm data

## Setup

### Requirements

- Python 3.9+
- Virtual environment
- FastAPI & Uvicorn
- ML frameworks (PyTorch, scikit-learn)

### Installation

1. **Create virtual environment**:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source venv/bin/activate  # Linux/Mac
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running the Service

Start the FastAPI server:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The service will be available at:
- **API**: `http://localhost:8000`
- **API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
- `GET /health` - Service health status and model versions

### Crop Health
- `POST /v1/crop-health` - Detect crop health from image
  - Input: image, crop type, growth stage
  - Output: label, severity, confidence, detection boxes

### Damage Assessment
- `POST /v1/damage-assessment` - Assess crop damage from event
  - Input: images, crop type, event type
  - Output: damage percentage, severity, detections, confidence

### Yield Prediction  
- `POST /v1/yield-prediction` - Predict crop yield
  - Input: crop, area (ha), sowing date, optional weather/history
  - Output: yield value, unit, confidence

### Risk Scoring
- `POST /v1/risk-score` - Calculate farm insurance risk score
  - Input: weather, crop, soil data, optional history
  - Output: risk score (0-1), risk band, contributing factors

### Soil OCR
- `POST /v1/soil-ocr` - Extract soil data from report/image
  - Input: PDF or image file
  - Output: N, P, K, pH values with confidence

### Advisory
- `POST /v1/advisory` - Generate agricultural recommendations
  - Input: farm context (crop, soil, weather, history)
  - Output: recommendations, warnings

## Project Structure

```
ai/
├── app/                    # FastAPI application
│   ├── main.py            # Application entry point
│   ├── config.py          # Configuration & env vars
│   ├── routes/            # API endpoints
│   ├── schemas/           # Request/response models
│   └── services/          # Business logic
│
├── collection/            # External data collection
│   ├── geometry/          # Farm boundary calculations
│   ├── satellite/         # Sentinel-2 imagery
│   ├── weather/           # Weather API client
│   ├── soil/              # Soil data API
│   └── external/          # Shared utilities
│
├── feature_engineering/   # Raw data → model features
├── inference/            # Model predictions
├── models/               # Trained model files & metadata
├── training/             # Model training pipelines
├── recommendation/       # Advisory rule engine
├── evaluation/           # Metrics & reports
├── utils/                # Utility functions
├── tests/                # Test suite
├── data/                 # Data directories
└── requirements.txt      # Python dependencies
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Training Models

Each model has its own training pipeline:

```bash
# Crop health
python training/crop_health/train.py

# Damage assessment  
python training/damage/train.py

# Yield prediction
python training/yield/train.py

# Risk scoring
python training/risk/train.py
```

## Environment Variables

See `.env.example` for all available configuration options:

- `DEBUG` - Enable debug mode
- `MOCK_MODE` - Return sample data without real models
- `MIN_CONFIDENCE` - Minimum confidence threshold (0-1)
- `MODEL_DIR` - Path to trained models directory
- `UPLOAD_DIR` - Path for temporary file uploads

## Docker

Build and run with Docker:

```bash
docker build -t agrishield-ai .
docker run -p 8000:8000 agrishield-ai
```

## License

Proprietary - AgriShield Project 2026
