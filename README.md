# Social Media Engagement Predictor

Production-ready ML application for predicting social media engagement rates.

## 📁 Project Structure

```
CL/
├── 📚 docs/                      # Documentation
│   ├── README.md                 # Project overview
│   ├── COMPLETE_GUIDE.md         # Setup and deployment guide
│   ├── PROJECT_SUMMARY_FULL.md   # Detailed project summary
│   └── SECURITY_DOCUMENTATION.md # Security best practices
│
├── 💻 src/                       # Application source code
│   ├── streamlit_app.py          # Main Streamlit web app
│   ├── azure_monitoring.py       # Application Insights integration
│   ├── azure_config.py           # Azure configuration helper
│   └── table_storage_manager.py  # Azure Table Storage operations
│
├── 🔧 scripts/                   # Utility scripts
│   ├── data_balancing.py         # SMOTE/ADASYN data preprocessing
│   ├── generate_predictions.py   # Batch prediction generator
│   └── key_vault_setup.py        # Azure Key Vault setup
│
├── 📓 notebooks/                 # Jupyter notebooks
│   └── AZURE_ML_WORKSPACE.ipynb  # Azure ML workspace integration
│
├── 📊 data/                      # Data files
│   ├── cleaned_data/             # Training dataset (12,000 posts)
│   ├── predictions/              # Prediction outputs
│   └── database/                 # SQLite database
│
├── 🤖 models/                    # Trained ML models
│   ├── engagement_model.pkl      # HistGradientBoostingRegressor
│   ├── feature_columns.pkl       # Feature names
│   ├── label_encoders.pkl        # Categorical encoders
│   └── experiment_results.json   # Model comparison results
│
├── 📈 mlruns/                    # MLflow experiment artifacts
├── 🗄️ mlflow.db                  # MLflow tracking database
│
├── ☁️ azure_functions_project/   # Azure Functions code
│   ├── ProcessDataHTTP/          # Data processing function
│   ├── host.json                 # Function app configuration
│   └── requirements.txt          # Function dependencies
│
├── 🚀 .github/workflows/         # GitHub Actions CI/CD
│   ├── ci.yml                    # Continuous Integration
│   ├── aca-deploy.yml            # Azure Container Apps deployment
│   ├── ci-basic.yml              # Basic syntax checks
│   └── deploy.yml                # Deployment workflows
│
├── ⚙️ Configuration Files
│   ├── .env                      # Environment variables (secrets)
│   ├── .gitignore                # Git ignore patterns
│   ├── azure-pipelines.yml       # Azure DevOps pipeline
│   ├── azure_config.json         # Azure service configuration
│   ├── Dockerfile                # Container build configuration
│   └── requirements.txt          # Python dependencies
│
└── 🔧 Development
    ├── .venv/                    # Python virtual environment
    └── .streamlit/               # Streamlit configuration
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   streamlit run src/streamlit_app.py
   ```

3. **Access the app:**
   Open http://localhost:8501

## ☁️ Azure Deployment

- **Container App:** https://social-ml-app.gentleglacier-5e8a21de.francecentral.azurecontainerapps.io
- **Resource Group:** rg-social-media-ml
- **Region:** France Central

## 📖 Documentation

- See [docs/README.md](docs/README.md) for detailed project overview
- See [docs/COMPLETE_GUIDE.md](docs/COMPLETE_GUIDE.md) for setup instructions
- See [docs/SECURITY_DOCUMENTATION.md](docs/SECURITY_DOCUMENTATION.md) for security details

## 🧪 Model Performance

- **Algorithm:** HistGradientBoostingRegressor
- **R² Score:** -0.0410
- **MAE:** 0.3613
- **RMSE:** 1.1469
- **Dataset:** 12,000 social media posts (22 features)

## 🔐 Environment Variables

Required in `.env`:
- `AZURE_STORAGE_CONNECTION_STRING`
- `APPLICATIONINSIGHTS_CONNECTION_STRING`
- `AZURE_EVENTHUB_CONNECTION_STRING`
- `APPINSIGHTS_INSTRUMENTATION_KEY`

## 🛠️ Development

- Python 3.11
- MLflow for experiment tracking
- Docker for containerization
- GitHub Actions & Azure DevOps for CI/CD
