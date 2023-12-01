from pyspark.sql import SparkSession, Row, functions
                                                                                                                                                                                                                                 
def loadMovieNames():
        movieNames = {}                                                                                                                                                                                                          
        with open("u.item") as f:
                for line in f:
                        fields = line.split("|")
                        movieNames[int(fields[0])] = fields[1]
        return movieNames
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
def parseInput(line):
        fields = line.split()                                                                                                                                                                                                    
        return (int(fields[1]), (float(fields[2])))
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
if __name__ == "__main__":
        # The main script - create our SparkContext
        spark = SparkSession.builder.appName("BestMovies").getOrCreate()
                                                                                                                                                                                                                                 
        movieNameLookUp = loadMovieNames()                                                                                                                                                                                       
                                                                                                                                                                                                                                 
        lines = spark.sparkContext.textFile("hdfs:///user/maria_dev/ml-100k/u.data")
        movieRatings = lines.map(parseInput)
        movieRatings = spark.createDataFrame(movieRatings,["movieID","rating"])
        combined_data = movieRatings.groupBy("movieID").agg(functions.avg("rating").alias("avg_rating"),
                                                              functions.count("rating").alias("count_rating"))
        results = combined_data.orderBy(functions.desc("avg_rating")).take(10)
                                                                                                                                                                                                                                 
                                                                                                                                                                                                                                 
        for movie in results:
                print(movieNameLookUp[movie["movieID"]], movie["avg_rating"], movie["count_rating"])
                                                                                                                                                                                                                                 
        spark.stop() 