
#!/bin/bash
echo "🚀 Deploying The Ω Depot..."

# Install requirements
pip install -r requirements.txt

# Set up secrets if not present
mkdir -p ~/.streamlit
cp .streamlit/secrets.toml ~/.streamlit/secrets.toml

# Run the app
streamlit run app.py
