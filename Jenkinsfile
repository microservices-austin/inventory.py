#!groovy

node('node') {
    currentBuild.result = "SUCCESS"

    try {
       stage('Checkout'){
          checkout scm
       }
       stage('Test'){
         env.NODE_ENV = "test"
         print "Environment will be : ${env.NODE_ENV}"
       }
       stage('Build Docker'){
           echo 'build docker container'            
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
