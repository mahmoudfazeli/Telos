**Installation Instructions**

TELOS is a web application built with FastAPI and can be run locally using Uvicorn. Follow these steps to set up and run the project:

1.  **Clone the Repository**: Clone the GitHub repository to your local machine.
2.  **Install Dependencies**: Navigate to the directory containing the **requirements.txt** file and run the following command to install all required dependencies:

```bash
pip install -r requirements.txt
```

1.  **Set Up Environment Variables**: You'll need to provide your OpenAI API key as an environment variable. Replace **YOUR_API_KEY** with your actual key:

2.  **Run the Application**: Navigate to the directory containing **fastapi_app.py** and run the following command:

```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
```

3.  **Access the Application**: Open your web browser and navigate to **http://0.0.0.0:8000** to interact with TELOS.