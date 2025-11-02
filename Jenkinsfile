pipeline {
    agent any // Run on any available Jenkins agent

    environment {
        // !!! IMPORTANT: Change this to your Docker Hub username !!!
        DOCKER_HUB_USERNAME = "your-dockerhub-username"
        DOCKER_IMAGE_NAME   = "my-cicd-app"
        DOCKER_CREDENTIALS_ID = "dockerhub-creds" // The ID we set in Step 2
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
                    echo "Building $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME..."
                    
                    // Build the image and tag it with the build number
                    sh "docker build -t $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:$BUILD_NUMBER ."
                    
                    // Also tag it as 'latest'
                    sh "docker tag $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:$BUILD_NUMBER $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:latest"
                }
            }
        }

        stage('Test Container') {
            steps {
                // This is a simple test: run the container, check if it's running, then stop it
                echo "Running container for a quick test..."
                
                // Run the container in detached mode
                sh "docker run -d --name cicd-test-container $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:$BUILD_NUMBER"
                
                // Wait a few seconds for it to start
                sh "sleep 5"
                
                // Check that it's running (this command will fail the build if it's not)
                sh "docker ps -f name=cicd-test-container --format '{{.Names}}' | grep 'cicd-test-container'"
                
                // Stop and remove the test container
                echo "Stopping and removing test container..."
                sh "docker stop cicd-test-container"
                sh "docker rm cicd-test-container"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Logging in and pushing to Docker Hub..."
                // Use the Jenkins credentials to log in to Docker
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    
                    // Push the build number tag
                    sh "docker push $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:$BUILD_NUMBER"
                    
                    // Push the 'latest' tag
                    sh "docker push $DOCKER_HUB_USERNAME/$DOCKER_IMAGE_NAME:latest"
                }
            }
        }
    }
    
    post {
        // This 'post' block runs after all stages
        always {
            // Good practice to log out
            echo "Logging out of Docker Hub..."
            sh 'docker logout'
        }
    }
}