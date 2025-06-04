# Build_Autoscaler

## Setup Instructions

### Prerequisites
- Python 3.11.x (recommended)
- Git
- Docker (for containerized deployment)

### 1. Clone the Repository

 run 'git clone https://github.com/yourusername/autoscaling-image-classifier.git
cd autoscaling-image-classifier'

# Create virtual environment

run 'python -m venv venv'

# Activate it
# Windows:
run '.\venv\Scripts\activate'
# Mac/Linux:
source venv/bin/activate


# Install Dependencies

run 'pip install -r requirements.txt'

# Test the Application
Run the Server (Terminal 1)

run python 'model_server.py'

Test with Client (Terminal 2)

run python 'client.py'


# Common Issue

After running python client.py
500 Server Errors and server is crashing.

