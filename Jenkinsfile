pipeline {
    agent any

    environment {
        VENV_DIR    = 'venv'
        GCP_PROJECT = 'lunar-parsec-468107-k2'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {
        stage('Checkout') {
            steps {
                // simpler, built-in checkout
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: 'https://github.com/vssvedanth/MLOPS_Hotel_reservation_project.git'
            }
        }

        stage('Setup venv & Install deps') {
            steps {
                echo 'Creating venv and installing dependencies…'
                sh '''#!/bin/bash
                set -e

                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate && \
                pip install --upgrade pip setuptools wheel && \
                pip install -e .
                '''
            }
        }

        stage('Build & Push Docker to GCR') {
            steps {
                echo 'Building and Pushing Docker Image to GCR…'
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                sh '''#!/bin/bash
                set -e

                export PATH=$PATH:${GCLOUD_PATH}
                gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                gcloud config set project ${GCP_PROJECT}
                gcloud auth configure-docker --quiet

                docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                docker push  gcr.io/${GCP_PROJECT}/ml-project:latest
                '''
                }
            }
        }
    }
}
