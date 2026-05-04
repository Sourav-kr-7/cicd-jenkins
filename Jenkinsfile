pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        DOCKER_IMAGE = "souravkr7/cicd-app"
        DOCKERFILE_PATH = "docker/Dockerfile"
        WORKSPACE_DIR = "/mnt/c/Users/Sourav/.jenkins/workspace/github-auto-ci_cicd-jenkins_main"
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

        stage('Deploy to Staging') {
    steps {
        bat '''
        wsl bash -c "cd /mnt/c/Users/Sourav/.jenkins/workspace/github-auto-ci_cicd-jenkins_main && ls && ansible-playbook -i ansible/inventory.ini ansible/deploy.yml"
        '''
    }
}

        stage('Integration Test (Staging)') {
            steps {
                // ✅ Fixed quoting (single line bash)
                bat '''
                wsl bash -c "for i in {1..5}; do curl -f http://localhost:8081 && exit 0; sleep 3; done; exit 1"
                '''
            }
        }

        stage('Deploy to Production') {
    steps {
        bat '''
        wsl bash -c "cd /mnt/c/Users/Sourav/.jenkins/workspace/github-auto-ci_cicd-jenkins_main && ansible-playbook -i ansible/inventory.ini ansible/deploy.yml"
        '''
    }
}

        stage('Integration Test (Production)') {
            steps {
                bat 'wsl curl -f http://localhost:8082 || exit 1'
            }
        }
    }
}
