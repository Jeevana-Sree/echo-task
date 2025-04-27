pipeline {
    agent any

    stages {
        stage('Build Docker Containers') {
            steps {
                sh 'docker-compose build'
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
