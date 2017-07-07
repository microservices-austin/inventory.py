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
	    nosetests -svv 
          """
       }

       stage('Build Docker'){
	  sh """
            docker build -t inventory/service .
          """
       }

       stage('Store Image'){
	  echo 'store image'
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
