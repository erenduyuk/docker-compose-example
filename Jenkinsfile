pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repository.git'
            }
        }
        
        stage('Build') {
            steps {
                script {
                    // Build Docker images
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Deploy Docker containers
                    sh 'docker-compose up -d'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Add your testing commands here
                    sh 'echo "Running tests..."'
                    // Example: sh 'pytest tests/'
                }
            }
        }
    }

    post {
        always {
            script {
                // Cleanup Docker containers and images
                sh 'docker-compose down'
                sh 'docker image prune -f'
            }
        }
    }
}
