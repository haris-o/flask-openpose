# Simple Flask server with both implementations of Openpose

## Installation
```bash
git clone https://github.com/haris-osmanbegovic/flask-openpose
cd flask-openpose
bash ./setup.sh
docker build . -t flask-openpose
docker run --name flask-openpose -td flask-openpose:latest
```

## Usage
Navigate to `localhost:5001`

NOTE: Docker container requires at least 10GB RAM for full processing
(face, hands, body) using the default openpose algorithm. Recommended 
allocation is 16GB. 