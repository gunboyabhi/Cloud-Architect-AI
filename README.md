
## Important steps
pip install -r requirements.txt

Install Graphviz - https://graphviz.org/download/#windows


FastAPI struture:

fastapi-app/
│── app/
│   ├── main.py                         # Entry point
│   ├── api/                            # API routes
│   │   │── endpoints.py                # Business logic for APIs
|   ├── utils/
|   |   ├── generate_architecture.py    # generate cloud architecture (png)
|   |   ├── llm.py                      # Gets response from llm
|   |   ├── prompts.py                  # defined common prompts
│── .env                                # Environment variables
│── requirements.txt                    # Dependencies
│── README.md




## Features of the application:

1. Architecture Overview
2. Architecture diagram
3. Infrastructure as a code
4. Detailed Evaluation
  1. Comprehensive Analysis
  2. Actionable Recommendations for Enhancement
5. cost predictor
6. DR strategy
7. Infrastructure deployment