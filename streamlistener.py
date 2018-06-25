from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("local[2]", "Tweet Streaming App")
ssc = StreamingContext(sc, 10)

ssc.checkpoint( "file:/home/sandeep/tweets/checkpoint/")

socket_stream = ssc.socketTextStream("10.162.0.2",5556)

lines = socket_stream.window(20)

lines.count().map(lambda x: 'Tweets in this batch: %s' % x).pprint()

words = lines.flatMap( lambda twit: twit.split(" ") )

pairs = words.map( lambda word: (word.lower(), 1 ) )

wordCounts = pairs.reduceByKey( lambda a, b: a + b )

wordCounts.pprint()

ssc.start()
ssc.awaitTermination()
