from mrjob.job import MRJob
from mrjob.job import MRStep


class AverageRatings(MRJob):
        def steps(self):
                return [
                        MRStep(mapper = self.mapper_get_ratings,
                               reducer = self.get_average_ratings)
                ]
        def mapper_get_ratings(self,_,lines):
                user_id, movie_id, ratings, rating_time = lines.split("\t")
                yield movie_id, float(ratings)

        def get_average_ratings(self, key, values):
                values_list = list(values)
                yield key, sum(values_list)/len(values_list)

if __name__ == "__main__":
        AverageRatings.run()
