from pyspark import SparkConf, SparkContext

def loadMovieNames():
        movieNames = {}
        with open("u.item") as f:
                for line in f:
                        fields = line.split("|")
                        movieNames[int(fields[0])] = fields[1]
        return movieNames


def parseInput(line):
        fields = line.split()
        return (int(fields[1]), (float(fields[2]),1.0))


if __name__ == "__main__":
        # The main script - create our SparkContext
        conf = SparkConf().setAppName("WorstMovies")
        sc = SparkContext(conf = conf)

        movieNameLookUp = loadMovieNames()

        lines = sc.textFile("hdfs:///user/maria_dev/ml-100k/u.data")
        movieRatings = lines.map(parseInput)
        grouped_ratings = movieRatings.reduceByKey(lambda movie1,movie2: (movie1[0] + movie2[0], movie1[1]+movie2[1]))
        average_ratings = grouped_ratings.mapValues(lambda totalRating: totalRating[0]/totalRating[1])
        sorted_movies = average_ratings.sortBy(lambda x: x[1])

        results = sorted_movies.take(10)

        for movie in results:
                print(movieNameLookUp[movie[0]], movie[1])
