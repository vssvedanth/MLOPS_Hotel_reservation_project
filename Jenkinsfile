pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "lunar-parsec-468107-k2"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                script {
                    echo '📥 Cloning GitHub repo...'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/vssvedanth/MLOPS_Hotel_reservation_project.git'
                        ]]
                    )
                }
            }
        }

        stage('Setup Virtualenv & Install Dependencies') {
            steps {
                script {
                    echo '🐍 Creating virtualenv & installing dependencies...'
                    sh '''#!/bin/bash
                        set -e
                        python3 --version
                        python3 -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate
                        python -m pip install --upgrade pip
                        if [ -f requirements.txt ]; then
                            pip install -r requirements.txt
                        else
                            echo "⚠ requirements.txt not found, skipping..."
                        fi
                    '''
                }
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo '🐳 Building & pushing Docker image...'
                        sh '''#!/bin/bash
                            set -e
                            export PATH=$PATH:${GCLOUD_PATH}
                            gcloud --version
                            docker --version

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

        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                            
                        '''
                    }
                }
            }
        }
    }
}
