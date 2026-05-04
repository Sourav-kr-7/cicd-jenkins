pipeline {
agent any

```
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

    // ✅ STAGING DEPLOY
    stage('Deploy to Staging') {
        steps {
            bat """
            wsl bash -c "cd ${WORKSPACE_DIR} && ansible-playbook -i ansible/inventory.ini ansible/deploy.yml -l staging"
            """
        }
    }

    // ✅ STAGING TEST (FIXED - SINGLE LINE)
    stage('Integration Test (Staging)') {
        steps {
            bat '''
            wsl bash -c "success=0; for i in $(seq 1 5); do echo Checking staging...; curl -s http://localhost:8081 > /dev/null && success=1 && break; sleep 3; done; if [ $success -eq 1 ]; then exit 0; else exit 1; fi"
            '''
        }
    }

    // ✅ PRODUCTION DEPLOY
    stage('Deploy to Production') {
        steps {
            bat """
            wsl bash -c "cd ${WORKSPACE_DIR} && ansible-playbook -i ansible/inventory.ini ansible/deploy.yml -l production"
            """
        }
    }

    // ✅ PRODUCTION TEST (FIXED - SINGLE LINE)
    stage('Integration Test (Production)') {
        steps {
            bat '''
            wsl bash -c "success=0; for i in $(seq 1 10); do echo Checking production...; curl -s http://localhost:8082 > /dev/null && success=1 && break; sleep 3; done; if [ $success -eq 1 ]; then exit 0; else exit 1; fi"
            '''
        }
    }

    // ✅ MONITORING CHECK
    stage('Monitoring Check') {
        steps {
            bat '''
            wsl bash -c "curl -s http://localhost:8082/metrics | grep http_requests_total"
            '''
        }
    }
}
```

}
