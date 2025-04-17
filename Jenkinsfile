pipeline {
  agent any

  stages {
    stage('Checkout Code') {
      steps {
        git branch: 'main', url: 'https://github.com/Jeevana-Sree/echo-task.git'
      }
    }

    stage('Build and Deploy') {
      steps {
        sh 'docker-compose down'
        sh 'docker-compose up --build -d'
      }
    }
  }

  post {
    success {
      echo 'Build and deploy successful!'
    }
    failure {
      echo 'Build or deploy failed.'
    }
  }
}
