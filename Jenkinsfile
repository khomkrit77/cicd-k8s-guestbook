pipeline {
    agent any
    
    environment {
        // กำหนดตัวแปรไว้ใช้งาน (เปลี่ยนชื่อ User ให้ตรงกับ Docker Hub ของคุณ)
        DOCKER_HUB_USER = 'romeokiller'
        IMAGE_NAME      = 'cicd-k8s-guestbook'
        
        // พาธของไฟล์กุญแจ Kubeconfig ที่เราก๊อปปี้เข้าไปใน Jenkins Container
        KUBECONFIG      = '/var/jenkins_home/config'
    }

    stages {
        stage('Checkout') {
            steps {
                // ดึงโค้ดล่าสุดจาก GitHub
                checkout scm
            }
        }

        stage('Build & Push Image') {
            steps {
                script {
                    // 1. Build Image พร้อมระบุเลข Build Number และ Latest
                    def appImage = docker.build("${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}")
                    
                    // 2. Login และ Push ขึ้น Docker Hub
                    docker.withRegistry('', 'dockerhub-credentials') { // ตรวจสอบ ID Credentials ใน Jenkins ให้ตรง
                        appImage.push()
                        appImage.push('latest')
                    }
                }
            }
        }

        stage('Kubernetes Deployment') {
            steps {
                script {
                    // 1. สั่ง Apply ไฟล์ทั้งหมดในโฟลเดอร์ k8s (เพื่ออัปเดต Service/PV/PVC)
                    sh "kubectl --kubeconfig=${KUBECONFIG} apply -f k8s/"

                    // 2. บังคับให้อัปเดต Deployment ของหน้าเว็บด้วย Image เวอร์ชันใหม่ล่าสุดที่เพิ่ง Build
                    // วิธีนี้จะทำให้ K8s ทำการ Rolling Update (สลับ Pod เก่า-ใหม่ให้เอง)
                    sh "kubectl --kubeconfig=${KUBECONFIG} set image deployment/guestbook-web guestbook=${DOCKER_HUB_USER}/${IMAGE_NAME}:${BUILD_NUMBER}"
                    
                    // 3. ตรวจสอบสถานะการ Deploy
                    sh "kubectl --kubeconfig=${KUBECONFIG} rollout status deployment/guestbook-web"
                }
            }
        }
    }

    post {
        success {
            echo '🚀 Deployment Successful!'
        }
        failure {
            echo '❌ Deployment Failed. Please check logs.'
        }
    }
}
