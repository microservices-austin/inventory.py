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
	  sh 'virtualenv venv'
          sh 'source venv/bin/activate'
          sh 'pip install -r requirements.txt'
       }

       stage('Test'){
          echo 'run our tests'
       }

       stage('Build Docker'){
          echo 'build docker container'            
       }

       stage('Store Image'){
	  echo 'store image'
       }

       stage('Deploy'){
          echo 'Push to Repo'
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
