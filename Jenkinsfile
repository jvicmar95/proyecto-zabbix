pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "jvicmar95/proyecto-zabbix:latest"
  }

  stages {
    stage('Clonar repo') {
      steps {
        checkout scm
      }
    }

    stage('Build Docker image') {
      steps {
        sh 'docker build -t $DOCKER_IMAGE .'
      }
    }

    stage('Login Docker Hub') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
        }
      }
    }

    stage('Push Docker image') {
      steps {
        sh 'docker push $DOCKER_IMAGE'
      }
    }
  }
}
