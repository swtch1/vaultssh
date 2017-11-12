pipeline {
  agent any

  stages {
    stage('Build') {
      steps {
        sh """
        yum install -y python34
        easy_install-3.4 pip

        /usr/bin/python3 setup.py install
        /usr/bin/python3 tests/unit.py
        /usr/bin/python3 tests/integration.py
        """
      }
    }
    stage('Deploy') {
      steps {
        sh """
        yum install -y python34
        easy_install-3.4 pip

        /usr/bin/python3 setup.py install
        /usr/bin/python3 tests/unit.py
        /usr/bin/python3 tests/integration.py
        """
      }
    }
  }
}
