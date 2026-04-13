pipeline {
    agent any

    options {
        timestamps()
    }

    parameters {
        booleanParam(name: 'REQUIRE_PROD_APPROVAL', defaultValue: true, description: 'Require manual approval before production deploy')
        choice(name: 'DEPLOY_TARGET', choices: ['staging', 'production'], description: 'Where to deploy (production will still honor approval gate if enabled)')
        string(name: 'DOCKER_IMAGE', defaultValue: 'your-dockerhub-username/my-app', description: 'Docker image repo (e.g. user/my-app)')
    }

    environment {
        DOCKER_IMAGE = "${params.DOCKER_IMAGE}"
        DOCKERFILE_PATH = "docker/Dockerfile"
        ANSIBLE_INVENTORY = "ansible/inventory.ini"
        ANSIBLE_PLAYBOOK = "ansible/deploy.yml"
    }

    triggers {
        // GitHub webhook trigger (requires "GitHub plugin" + job configured with GitHub webhook)
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build (sanity)') {
            steps {
                echo "Building application..."
            }
        }

        stage('Test') {
            steps {
                dir('app') {
                    sh 'python -m pip install --upgrade pip'
                    sh 'pip install -r requirements.txt'
                }
                sh 'pytest -q'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -f ${DOCKERFILE_PATH} -t ${DOCKER_IMAGE}:${BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest .'
            }
        }

        stage('Docker Push') {
            when {
                expression { env.BRANCH_NAME == 'master' || env.BRANCH_NAME == 'main' }
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_PASS')]) {
                    sh 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
                }
                sh 'docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}'
                sh 'docker push ${DOCKER_IMAGE}:latest'
            }
        }

        stage('Deploy to Staging') {
            when {
                expression { params.DEPLOY_TARGET == 'staging' }
            }
            steps {
                sh 'ansible-playbook ${ANSIBLE_PLAYBOOK} -i ${ANSIBLE_INVENTORY} -e "target_env=staging docker_image=${DOCKER_IMAGE}:latest"'
            }
        }

        stage('Approval') {
            when {
                allOf {
                    expression { params.DEPLOY_TARGET == 'production' }
                    expression { params.REQUIRE_PROD_APPROVAL }
                }
            }
            steps {
                input message: 'Approve deployment to Production?'
            }
        }

        stage('Deploy to Production') {
            when {
                expression { params.DEPLOY_TARGET == 'production' }
            }
            steps {
                sh 'ansible-playbook ${ANSIBLE_PLAYBOOK} -i ${ANSIBLE_INVENTORY} -e "target_env=production docker_image=${DOCKER_IMAGE}:latest"'
            }
        }
    }
}

