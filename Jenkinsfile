pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        DOCKER_IMAGE = "souravkr7/cicd-app"
        DOCKERFILE_PATH = "docker/Dockerfile"
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Building application..."
            }
        }

        stage('Test') {
            steps {
                dir('app') {
                    bat 'python -m pip install --upgrade pip'
                    bat 'pip install -r requirements.txt'
                }
                bat 'pytest -q'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -f %DOCKERFILE_PATH% -t %DOCKER_IMAGE%:%BUILD_NUMBER% -t %DOCKER_IMAGE%:latest .'
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat 'echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin'
                }
                bat 'docker push %DOCKER_IMAGE%:%BUILD_NUMBER%'
                bat 'docker push %DOCKER_IMAGE%:latest'
            }
        }

        stage('Deploy') {
            steps {
                bat 'wsl ansible-playbook /mnt/c/Users/Sourav/.jenkins/workspace/github-auto-ci_cicd-jenkins_main/ansible/deploy.yml'
            }
        }
    }
}
    
