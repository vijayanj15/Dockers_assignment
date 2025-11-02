// Declarative Pipeline for CI/CD
pipeline {
    agent any // Run on any available Jenkins agent

    // Environment variables used in the pipeline
    environment {
        // --- IMPORTANT ---
        // 1. You will change this later to your Docker Hub username/repo
        // 2. The ID 'dockerhub-creds' MUST match the credential ID you create in Jenkins
        // -----------------
        DOCKERHUB_IMAGE_NAME = '<your-dockerhub-username>/<your-repo-name>'
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-creds'
        PROJECT_DIR = 'cicd_app' // The subdirectory where our app lives
    }

    stages {
        stage('Checkout') {
            steps {
                // Get the code from GitHub
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Build the image and tag it with 'latest' and the Git commit hash
                    // We 'cd' into the project directory to find the Dockerfile
                    sh "docker build -t ${env.DOCKERHUB_IMAGE_NAME}:latest -f ${env.PROJECT_DIR}/Dockerfile ${env.PROJECT_DIR}"
                    sh "docker build -t ${env.DOCKERHUB_IMAGE_NAME}:${env.GIT_COMMIT.take(7)} -f ${env.PROJECT_DIR}/Dockerfile ${env.PROJECT_DIR}"
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    // Run the container in detached mode and give it a name for cleanup
                    // We map port 8081 on the host to 5000 in the container
                    sh "docker run -d --name test_container -p 8081:5000 ${env.DOCKERHUB_IMAGE_NAME}:latest"
                    
                    // Give the container a moment to start
                    sh "sleep 5"
                    
                    // Test the endpoint. 'grep' will fail the build if the string isn't found.
                    echo "Testing container endpoint..."
                    sh "curl -s http://localhost:8081 | grep 'Hello from your CI/CD Pipeline'"
                }
            }
            post {
                // This 'always' block runs regardless of whether the stage succeeded or failed
                always {
                    // Clean up: Stop and remove the test container
                    echo "Stopping and removing test container..."
                    sh "docker stop test_container"
                    sh "docker rm test_container"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                // Use the 'dockerhub-creds' secret to log in and push
                withCredentials([string(credentialsId: env.DOCKERHUB_CREDENTIALS_ID, variable: 'DOCKERHUB_PASSWORD')]) {
                    // --- IMPORTANT ---
                    // You will need to change <your-dockerhub-username> in the login command below
                    // -----------------
                    sh "echo $DOCKERHUB_PASSWORD | docker login -u <your-dockerhub-username> --password-stdin"
                    sh "docker push ${env.DOCKERHUB_IMAGE_NAME}:latest"
                    sh "docker push ${env.DOCKERHUB_IMAGE_NAME}:${env.GIT_COMMIT.take(7)}"
                }
            }
        }

        stage('Deploy (Optional)') {
            steps {
                // This is a placeholder for your deployment step.
                echo "Deploying application... (This is just a placeholder)"
            }
        }
    }

    post {
        // This block runs at the end of the entire pipeline
        always {
            // Clean up the Docker login
            echo "Logging out of Docker Hub..."
            sh "docker logout"
        }
    }
}