# HealthGuide AI Machine Learning Service

This directory contains the Python-based machine learning workflow for HealthGuide AI. It includes data preparation, model training, and a FastAPI service that exposes disease prediction and health assessment results.

## Components

- `train.py`: trains a Random Forest classifier on the provided disease dataset
- `api/main.py`: FastAPI server for prediction and disease information endpoints
- `ai/reasoning.py`: symptom risk scoring and follow-up question logic
- `ai/report_generator.py`: report generation for assessment results
- `dataset/`: disease and symptom datasets
- `models/`: saved trained model artifacts

## Workflow

1. Load the disease dataset from the dataset folder.
2. Train a classifier to predict likely diseases from symptom indicators.
3. Save the model and label encoder into the models directory.
4. Serve predictions through the FastAPI API.

## Run locally

Prerequisites:
- Python 3.10+
- pip

Install dependencies:

```bash
cd healthguide_ai_ml2
pip install -r requirements.txt
```

Generate the dataset (if not already present):

```bash
python generate_dataset.py
```

Train the model:

```bash
python train.py
```

Start the API:

```bash
uvicorn api.main:app --reload
```

## API endpoints

- `GET /`: health check
- `GET /health`: detailed health status
- `GET /symptoms`: available symptom features
- `GET /diseases`: available disease information
- `GET /diseases/{disease_name}`: get specific disease details
- `POST /predict`: predict diseases based on symptoms
- `POST /assistant`: chat with the AI health assistant

## API Usage Examples

### Get Available Symptoms

```bash
curl http://localhost:8000/symptoms
```

### Get Disease Information

```bash
curl http://localhost:8000/diseases
```

### Make a Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough", "headache"]}'
```

### Chat with AI Assistant

```bash
curl -X POST http://localhost:8000/assistant \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I have a fever and cough, what should I do?",
    "history": []
  }'
```

## Environment Variables

Create a `.env` file in the project root with:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=production
```

## Docker Deployment

Build the Docker image:

```bash
docker build -t healthguide-ai-ml .
```

Run the container:

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  healthguide-ai-ml
```

## Render Deployment

This project includes a `render.yaml` configuration file for easy deployment to Render.

1. Push this repository to GitHub
2. Connect your GitHub repository to Render
3. Render will automatically build and deploy using the `render.yaml` configuration
4. Set the `OPENAI_API_KEY` environment variable in Render dashboard

## Testing

Run tests with pytest:

```bash
pytest tests/
```

## Project Structure

```
.
├── api/
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── ai/
│   ├── __init__.py
│   ├── reasoning.py         # Risk assessment logic
│   └── report_generator.py  # Report generation
├── knowledge/
│   ├── __init__.py
│   └── diseases.py          # Disease information database
├── dataset/
│   └── disease_dataset.csv  # Training dataset
├── models/                  # Trained model artifacts (git ignored)
├── utils/
│   ├── __init__.py
│   └── preprocess.py        # Data preprocessing utilities
├── tests/
│   ├── __init__.py
│   └── test_api.py          # API tests
├── notebooks/
│   └── training.ipynb       # Training notebook
├── train.py                 # Model training script
├── generate_dataset.py      # Dataset generation script
├── requirements.txt         # Python dependencies
├── runtime.txt              # Python version
├── Dockerfile               # Docker configuration
├── .dockerignore
├── .gitignore
├── .env.example             # Environment variables template
├── Procfile                 # Heroku/Render configuration
├── render.yaml              # Render deployment configuration
└── README.md
```

## Disclaimer

This assessment service is for informational purposes only and should not replace professional medical advice. Users should always consult with qualified healthcare professionals for medical concerns.

## License

MIT License - feel free to use and modify as needed.
