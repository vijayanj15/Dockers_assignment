pipeline {
    agent any // Run on any available Jenkins agent

    environment {
        // !!! IMPORTANT: Change this to your Docker Hub username (e.g., "vijay") !!!
        DOCKER_HUB_USERNAME = "vijay"
        DOCKER_IMAGE_NAME   = "my-cicd-app"
        DOCKER_CREDENTIALS_ID = "dockerhub-creds"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // This checks out the code from the GitHub repo
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                // We must 'cd' into the 'cicd_app' folder where the Dockerfile is
                dir('cicd_app') {
                    echo "Building %DOCKER_HUB_USERNAME%/%DOCKER_IMAGE_NAME%..."
                    
                    // Build the image and tag it (using 'bat' for Windows)
                    bat "docker build -t %DOCKER_HUB_USERNAME%/%DOCKER_IMAGE_NAME%:%BUILD_NUMBER% ."
                    
                    // Also tag it as 'latest'
                    bat "docker tag %DOCKER_HUB_USERNAME%/%DOCKER_IMAGE_NAME%:%BUILD_NUMBER% %DOCKER_HUB_USERNAME%/%DOCKER_IMAGE_NAME%:latest"
                }
            }
        }

        stage('Test Container') {
            steps {
                echo "Running container for a quick test..."
                
                // Run the container in detached mode
                bat "docker run -d --name cicd-test-container %DOCKER_HUB_USERNAME%/%DOCKER_IMAGE_NAME%:%BUILD_NUMBER%"
                
                // Wait 5 seconds (Windows 'timeout' command instead of 'sleep')
                bat "timeout /t 5"
                
                // Check that it's running (Windows 'findstr' command instead of 'grep')
                bat "docker ps -f name=cicd-test-container --format \"{{.Names}}\" | findstr \"cicd-test-container\""
                
                // Stop and remove the test container
                echo "Stopping and removing test container..."
                bat "docker stop cicd-test-container"
                bat "docker rm cicd-test-container"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Logging in and pushing to Docker Hub..."
                // Use the Jenkins credentials to log in to Docker
                // Note: %VAR% is the Windows syntax for environment variables
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                    
                    // Push the build number tag
                    bat "docker push %DOCKER_HUB_USERNAME%/%DOCKER_IMAGE_NAME%:%BUILD_NUMBER%"
                    
                    // Push the 'latest' tag
                    bat "docker push %DOCKER_HUB_USERNAME%/%DOCKER_IMAGE_NAME%:latest"
                }
            }
        }
    }
    
    post {
        always {
            echo "Logging out of Docker Hub..."
            // Use 'bat' for the logout command
            bat "docker logout"
        }
    }
}