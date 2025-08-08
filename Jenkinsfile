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

        stage('Setting up Virtual Environment and Installing dependencies') {
            steps {
                script {
                    echo 'Setting up Virtual Environment and Installing dependencies'
                    sh '''#!/bin/bash
                        python3 -m venv ${VENV_DIR}
                        source ${VENV_DIR}/bin/activate

                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }
    }
}
