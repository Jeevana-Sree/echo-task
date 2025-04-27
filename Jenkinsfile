pipeline {
    agent any

    stages {
        stage('Pull Docker Image') {
            steps {
                sh 'docker-compose pull'
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Build Confirmation') {
            steps {
                echo 'Containers are running fine!'
            }
        }

        stage('Shutdown Containers') {
            steps {
                sh 'docker-compose down'
            }
        }
    }
}
