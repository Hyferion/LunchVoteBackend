## Installation

1. Clone this repository
2. Navigate to the project root and execute on the command line
```
pip install --editable .
export FLASK_APP=lunchvote/lunchvote.py
# Only for debugging, not in production mode:
export FLASK_DEBUG=true
# Start server
flask run --host=0.0.0.0
```
This should start a webserver listening on port 5000 which is available from the outside world.