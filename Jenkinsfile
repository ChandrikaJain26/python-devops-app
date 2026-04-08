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

                echo "Starting Flask app for performance testing..."
                nohup python app/main.py > app.log 2>&1 &
                APP_PID=$!

                echo "Waiting for app to start..."
                sleep 5

                cd performance
                python -m pip install locust

                python -m locust --headless \
                    -u 10 -r 2 -t 20s \
                    -f locustfile.py \
                    --host http://localhost:8080

                echo "Stopping Flask app..."
                kill $APP_PID
                '''
             }
         }

        
        stage('SonarCloud Scan') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'
                    withSonarQubeEnv('SonarCloud') {      
                        sh "${scannerHome}/bin/sonar-scanner"               
                    }
                }
            }
        }
        stage('Docker Build') {
            steps {
                sh '''
                docker build -t python-devops-app:latest .
                '''
            }
        }

    }
}
