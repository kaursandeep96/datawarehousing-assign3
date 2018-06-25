# datawarehousing-assign3
# Twitter Tweet Extraction:
## For extracting the tweets, first, Apache Spark was installed on EC2. For, that open jdk was installed using command:
```sh
sudo apt-get -y install openjdk-8-jdk-headless
```
New folder was created to download apache spark in that using:
```sh
mkdir ~/server
```
Directory was changed to:
```sh
cd ~/server
```
Apache Spark was downloaded using:
```sh
wget http://apache.mirror.rafal.ca/spark/spark-2.3.0/spark-2.3.0-bin-hadoop2.7.tgz
```
and unpacked using:
```sh
sudo tar zxvf spark-2.3.0-bin-hadoop2.7.tgz
```
Then, global variables were set using:
```sh
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
export SPARK_HOME=~/server/spark-2.3.0-bin-hadoop2.7
export PYSPARK_PYTHON=python3
```
Then, ~/.profile file was opened and these variables were appended in that using:
```sh
Export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
Export SPARK_HOME=~/server/spark-2.3.0-bin-hadoop2.7
Export PYSPARK_PYTHON=python3
```

After following these steps session is restarted.

The next step was Startup Master step. Master is  the incharge of cluster and this is where all the jobs are being submitted. The master was started by using following steps:
```sh
cd ~/server
Sudo ./spark-2.3.0-bin-hadoop2.7/sbin/start-master.sh
```

Slave Startup was done using the following commands:
```sh
sudo ./spark-2.3.0-bin-hadoop2.7/sbin/start-slave.sh
spark://35.203.101.174:7077.
```

After setting up master and slave startups, session was started with the master using:
```sh
$SPARK_HOME/bin/pyspark --master spark://35.203.101.174:7077
```

SPARK STREAMING FROM TWITTER
Spark streaming divides the data into batches after that spark engine processes the the batches and finally generates the stream of results.

SENTIMENT ANALYSIS ALGORITHM:
We performed sentiment analysis using Logistic regression classifier.

FEATURE SELECTION:
The feature selection and feature extraction was done with the help of data pipeline method. Spark provides the users with set of Machine Learning algorithms which help the users in extraction, feature selection, transformation, clustering and more. All these can be done using data pipelines.



