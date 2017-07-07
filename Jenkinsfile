#!groovy

node() {
    currentBuild.result = "SUCCESS"

    try {
       stage('Checkout'){
          checkout scm
       }

       stage('Setup environment'){
          env.PATH = "~/pytools/bin:~/.local/bin:${env.PATH}"
       }

       stage('Install deps'){
          sh """
	    . /var/lib/jenkins/venv/bin/activate
	    pip install -r requirements.txt
	  """
       }

       stage('Test'){
	  sh """
	    . /var/lib/jenkins/venv/bin/activate
	    nosetests -svv 
          """
       }

       stage('Build Docker'){
	  sh """
            docker build -t inventory/service .
          """
       }

       stage('Store Image'){
	  sh """
            docker tag inventory/service:latest 059888644488.dkr.ecr.us-east-1.amazonaws.com/inventory/service:1.0
            docker push 059888644488.dkr.ecr.us-east-1.amazonaws.com/inventory/service:1.0
          """
       }

       stage('Run DB Migration') {

       }

       stage('Deploy'){
          echo 'Push to Repo'
       }

       stage('Run Integration Tests'){

       }

       stage('Cleanup'){
          echo 'prune and cleanup'
       }
    }
    catch (err) {
        currentBuild.result = "FAILURE"
        throw err
    }
}
