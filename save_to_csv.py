from pyspark.sql.functions import col
from pyspark.sql import SQLContext, SparkSession
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from collections import namedtuple
# from pyspark.sql.functions import desc
from pyspark.ml import PipelineModel
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.evaluation import BinaryClassificationEvaluator,MulticlassClassificationEvaluator
sc = SparkContext("local[2]", "Tweet Streaming App")
ssc = StreamingContext(sc, 10)
sqlContext = SQLContext(sc)
#ssc.checkpoint( "file:/home/sandeep/tweets/checkpoint/")
socket_stream = ssc.socketTextStream("10.162.0.2", 5555) # Internal ip of  the tweepy streamer
lines = socket_stream.window(20)
model=PipelineModel.load("logreg1.model")
lines.pprint()
fields = ("SentimentText")
Tweet = namedtuple( 'Tweet', fields )
def getSparkSessionInstance(sparkConf):
	if ("sparkSessionSingletonInstance" not in globals()):
		globals()["sparkSessionSingletonInstance"] = SparkSession \
			.builder \
			.config(conf=sparkConf) \
			.getOrCreate()
		return globals()["sparkSessionSingletonInstance"]
def do_something(time, rdd):
	print("========= %s =========" % str(time))
	try:
		# Get the singleton instance of SparkSession
		spark = getSparkSessionInstance(rdd.context.getConf())
		# Convert RDD[String] to RDD[Tweet] to DataFrame
		rowRdd = rdd.map(lambda w: Tweet(w))
		linesDataFrame = spark.createDataFrame(rowRdd)
		#predictions = pipeline.transform(linesDataFrame)
		#predictions.show()
		#pipelineFit = pipeline.fit(trainingData)
		#pipelineFit = pipeline.fit(linesDataFrame)
		#predictions = pipeline.transform(linesDataFrame)
		#predictions.filter(predictions['prediction'] == 0) \
		#	.select("SentimentText","Sentiment","probability","label","prediction") \
		#	.orderBy("probability", ascending=False) \
		#	.show(n = 10, truncate = 30)
		#predictions.filter(predictions['prediction'] == 1) \
		#	.select("SentimentText","Sentiment","probability","label","prediction") \
		#	.orderBy("probability", ascending=False) \
		#	.show(n = 10, truncate = 30)
		# Evaluate, metricName=[accuracy | f1]default f1 measure
		#predictions.show()
		#evaluator = BinaryClassificationEvaluator(rawPredictionCol="prediction",labelCol="label")
		#print("F1: %g" % (evaluator.evaluate(predictions)))
		
		# Creates a temporary view using the DataFrame
		linesDataFrame.createOrReplaceTempView("tweets")
		# Do tweet character count on table using SQL and print it
		lineCountsDataFrame = spark.sql("select SentimentText, length(SentimentText) as TextLength from tweets")
		#predictions = pipeline.transfrm(lineCountsDataFrame)
		#predictions.show()
		lineCountsDataFrame.show()
		#lineCountsDataFrame.coalesce(1).write.format("com.databricks.spark.csv").save("dirwithcsv")
		lineCountsDataFrame.coalesce(1).write.format("com.databricks.spark.csv").save("dirwithcsv1")
		predictions = model.transform(lineCountsDataFrame)
		predictions.show()
	except:
		pass
# key part!
lines.foreachRDD(do_something)
ssc.start()
ssc.awaitTermination()
