pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "lunar-parsec-468107-k2"
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

        stage('Building and Pushing Docker Image to GCR'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing Docker Image to GCR.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest 

                        '''
                    }
                }
            }
        }


    }
}
