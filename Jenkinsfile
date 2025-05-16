properties([
  parameters([
    string(name: 'APP_VERSION', defaultValue: '1.0', description: 'Introduce la versión a desplegar (ej. 1.0, 2.0, etc.)')
  ])
])

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
    args:
    - dockerd
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

  - name: kubectl
    image: lachlanevenson/k8s-kubectl:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /home/jenkins/agent
      name: workspace-volume

  - name: jnlp
    image: jenkins/inbound-agent:3309.v27b_9314fd1a_4-1
    resources:
      requests:
        memory: "256Mi"
        cpu: "100m"
    env:
    - name: JENKINS_AGENT_WORKDIR
      value: /home/jenkins/agent
    volumeMounts:
    - mountPath: /home/jenkins/agent
      name: workspace-volume

  nodeSelector:
    kubernetes.io/os: linux
  restartPolicy: Never
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
    DOCKER_IMAGE = "jvicmar95/proyecto-zabbix:${APP_VERSION}"
  }

  stages {
    stage('⏳ Esperar Docker') {
      steps {
        sh 'echo "⏱ Esperando que Docker esté disponible..."'
        sh 'sleep 20'
      }
    }

    stage('🐳 Build Docker image') {
      steps {
        sh 'echo "🔍 Verificando Docker..." && docker version'
        sh 'echo "🏗️ Construyendo imagen $DOCKER_IMAGE..." && docker build -t $DOCKER_IMAGE .'
      }
    }

    stage('📤 Push Docker image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh 'echo "🔐 Login en Docker Hub..." && echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
          sh 'echo "📦 Subiendo imagen a Docker Hub..." && docker push $DOCKER_IMAGE'
        }
      }
    }

    stage('🚀 Deploy to Kubernetes') {
      steps {
        container('kubectl') {
          sh 'echo "📂 Listando archivos..." && ls -la'
          sh 'echo "🔧 Verificando kubectl..." && kubectl version --client'
          sh 'echo "🚀 Aplicando deployment.yaml..." && kubectl apply -f deployment.yaml'
          sh 'echo "🔁 Actualizando imagen del deployment..." && kubectl set image deployment/web-nginx nginx=$DOCKER_IMAGE -n jenkins'
          sh 'echo "♻️ Borrando pod antiguo (si existe)..." && kubectl delete pod -l app=web-nginx -n jenkins || true'
          sh 'echo "⌛ Esperando nuevo pod..." && sleep 10'
          sh 'echo "📦 Nuevo pod desplegado:" && kubectl get pods -l app=web-nginx -n jenkins'
          sh 'echo "🌍 Servicio expuesto:" && kubectl get svc web-nginx -n jenkins'
        }
      }
    }
  }
}
