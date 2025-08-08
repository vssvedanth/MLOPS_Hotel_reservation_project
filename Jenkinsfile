pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "mlops-new-447207"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Cloning Github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github repo to Jenkins............'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/vssvedanth/MLOPS_Hotel_reservation_project.git']])
                }
            }
        }

        stage('Setting up Virtualenv & Installing dependencies') {
            steps {
                script {
                echo 'Creating venv and installing dependencies…'
                sh '''#!/bin/bash
                    set -e

                    python3 -m venv ${VENV_DIR}

                    source ${VENV_DIR}/bin/activate && \
                    pip install --upgrade pip && \
                    pip install -e .
                '''
                }
            }
        }

    }
}
