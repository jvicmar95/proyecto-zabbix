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
    - --tls=false
    ports:
    - containerPort: 2375
    volumeMounts:
    - mountPath: /var/lib/docker
      name: docker-graph-storage
    - mountPath: /home/jenkins/agent
      name: workspace-volume
      readOnly: false
  - name: jnlp
    image: jenkins/inbound-agent:3309.v27b_9314fd1a_4-1
    env:
    - name: JENKINS_AGENT_WORKDIR
      value: /home/jenkins/agent
    volumeMounts:
    - mountPath: /home/jenkins/agent
      name: workspace-volume
      readOnly: false
  volumes:
  - name: docker-graph-storage
    emptyDir: {}
  - name: workspace-volume
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
