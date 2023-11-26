from mrjob.job import MRJob
from mrjob.job import MRStep

class RatingsBreakdown(MRJob):
        def steps(self):
                return [
                        MRStep(mapper=self.mapper_get_ratings,
                               reducer=self.reducer_get_count)
                       ]
        def mapper_get_ratings(self,_,line):
                user_id, movie_id, rating, rating_time = line.split('\t')
                yield  rating,1
        def reducer_get_count(self,key,values):
                yield key, sum(values)

if __name__== '__main__':
        RatingsBreakdown.run()