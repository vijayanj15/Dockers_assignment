from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    """A simple 'Hello World' route for testing the CI/CD pipeline."""
    return "Hello from your CI/CD Pipeline! V1.0"

if __name__ == "__main__":
    # Note: 0.0.0.0 makes it accessible from outside the container
    app.run(host='0.0.0.0', port=5000)