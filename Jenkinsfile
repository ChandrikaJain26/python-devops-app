pipeline {
    agent { label 'python-agent' }

    environment {
        VENV = 'venv'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                python3 -m venv $VENV
                . $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pip install -r requirements-test.txt
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                . $VENV/bin/activate
                python -m pytest tests --junitxml=unit-report.xml
                '''
            }
        }

        stage('Functional Tests') {
            steps {
                sh '''
                . $VENV/bin/activate
                chmod +x functional_test.sh
                ./functional_test.sh
                '''
            }
        }

        stage('Performance Tests') {
            steps {
                sh '''
                . $VENV/bin/activate
                python -m pip install locust
                cd performance
                python -m locust --headless -u 10 -r 2 -t 20s \
                  -f locustfile.py \
                  --host http://localhost:8080
                '''
            }
        }
    }
}
