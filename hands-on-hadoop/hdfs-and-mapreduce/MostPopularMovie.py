from mrjob.job import MRJob
from mrjob.job import MRStep


class MostPopularMovie(MRJob):
        def steps(self):
                return [
                        MRStep(mapper = self.mapper_get_ratings,
                               reducer = self.reducer_count),
                        MRStep(reducer = self.reducer_most_popular_movie)
                       ]
        def mapper_get_ratings(self,_,lines):
                user_id, movie_id, ratings, rating_time = lines.split("\t")
                yield movie_id, 1

        def reducer_count(self, key, values):
                yield None, (key, sum(values))

        def reducer_most_popular_movie(self,_,movie_count_pairs):
                yield max(movie_count_pairs)

if __name__ == "__main__":
        MostPopularMovie.run()
