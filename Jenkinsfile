pipeline {
  agent {
    kubernetes {
      label 'dind-agent'
      defaultContainer 'dind'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: dind
    image: docker:20.10-dind
    securityContext:
      privileged: true
    command:
    - dockerd-entrypoint.sh
    args:
    - --host=tcp://127.0.0.1:2375
    - --host=unix:///var/run/docker.sock
    ports:
    - containerPort: 2375
    volumeMounts:
    - mountPath: /var/lib/docker
      name: docker-graph-storage
  volumes:
  - name: docker-graph-storage
    emptyDir: {}
"""
    }
  }

  environment {
    DOCKER_HOST = "tcp://127.0.0.1:2375"
    DOCKER_IMAGE = "jvicmar95/proyecto-zabbix:latest"
  }

  stages {
    stage('Build Docker image') {
      steps {
        sh 'docker version'
        sh 'docker build -t $DOCKER_IMAGE .'
      }
    }

    stage('Push Docker image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh 'docker push $DOCKER_IMAGE'
        }
      }
    }
  }
}
