pipeline {
    agent { label 'python-agent' }

    environment {
        VENV = 'venv'

        // Nexus (keep as-is)
        NEXUS_REGISTRY = "13.232.8.122:8082"
        IMAGE_NAME = "python-devops-app"
        IMAGE_TAG = "${BUILD_NUMBER}"

        // ECR
        AWS_REGION = "ap-south-1"
        ECR_ACCOUNT_ID = "193913969706"
        ECR_REGISTRY = "${ECR_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        ECR_REPO = "python-devops-app"
    }

    stages {


        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-creds',
                    url: 'https://github.com/ChandrikaJain26/python-devops-app.git'
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

                nohup python app/main.py > app.log 2>&1 &
                APP_PID=$!
                sleep 5

                cd performance
                pip install locust
                locust --headless -u 10 -r 2 -t 20s \
                    -f locustfile.py --host http://localhost:8080

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
                docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        // ✅ KEEP NEXUS PUSH (unchanged)
        stage('Push Docker Image to Nexus') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'nexus-docker-creds',
                    usernameVariable: 'NEXUS_USER',
                    passwordVariable: 'NEXUS_PASS'
                )]) {
                    sh '''
                    docker login -u $NEXUS_USER -p $NEXUS_PASS http://$NEXUS_REGISTRY
                    docker tag ${IMAGE_NAME}:latest $NEXUS_REGISTRY/${IMAGE_NAME}:${IMAGE_TAG}
                    docker push $NEXUS_REGISTRY/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        // ✅ NEW: Push image to ECR (IAM role based login)
        stage('Login & Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION \
                | docker login --username AWS --password-stdin $ECR_REGISTRY

                docker tag ${IMAGE_NAME}:latest \
                  $ECR_REGISTRY/$ECR_REPO:$IMAGE_TAG

                docker push $ECR_REGISTRY/$ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        // ✅ NEW: GitOps update for Argo CD
        stage('Update GitOps Manifest') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_PASS'
                )]) {
                    sh '''
                    sed -i "s|image:.*|image: $ECR_REGISTRY/$ECR_REPO:$IMAGE_TAG|g" k8s/deployment.yml

                    git config user.name "jenkins"
                    git config user.email "jenkins@local"

                    git add k8s/deployment.yml
                    git commit -m "Deploy image $IMAGE_TAG via Argo CD"
                    git push https://${GIT_USER}:${GIT_PASS}@github.com/ChandrikaJain26/python-devops-app.git HEAD:main
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ Build ${IMAGE_TAG} deployed successfully via Argo CD"
        }
        failure {
            echo "❌ Pipeline failed"
        }
    }
}
