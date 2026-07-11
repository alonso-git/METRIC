# METRIC
A chat based AI support system for customer service agents, focused to help identify and prevent the service cancellation

## Installation
To replicate Python environment and run the server, follow these steps:

1. Make sure Python is installed and up to date: 
    *sudo dnf install python<3.14+>*
    *python --version*
2. Clone the repo: *git clone <repo-url>*
3. Open the backend dir (inside the repo dir): *cd backend*
4. Create a virtual environment: 
    *python -m venv <env-name>*
    *python3 -m venv <env-name>* *If first one fails*
5. Install pip dependencies: *pip install -r requirements.txt*
6. Run the server: *fastapi dev main.py*
7. Documentation will be available at: *127.0.0.1:8000/docs*
8. Done!

If the file *requirements.txt* is not available in the repo, yell at the owner.