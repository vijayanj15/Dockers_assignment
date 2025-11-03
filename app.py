from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    """A simple 'Hello World' route for testing the CI/CD pipeline."""
    # This new message will show that our webhook worked
    return "Hello, World! This is my FULLY AUTOMATIC CI/CD PIPELINE! V3.0"

if __name__ == "__main__":
    # Note: 0.0.0.0 makes it accessible from outside the container
    app.run(host='0.0.0.0', port=5000)