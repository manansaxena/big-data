ratings = LOAD '/user/maria_dev/ml-100k/u.data' AS (userId:int, movieId:int, rating:int, ratingTime:int);
metadata = LOAD '/user/maria_dev/ml-100k/u.item' USING PigStorage('|') 
		   AS (movieId:int, movieName:chararray, releaseDate:chararray, imdblink:chararray);

nameLookup = FOREACH metadata GENERATE movieId, movieName, ToUnixTime(ToDate(releaseDate,'dd-MMM-yyy')) AS releaseDate;

groupedRatings = GROUP ratings BY movieId;


averageRatings = FOREACH groupedRatings GENERATE group AS movieId, AVG(ratings.rating) AS avgRating;
bestMovies = FILTER averageRatings BY avgRating > 4.0;
bestMoviesData = JOIN bestMovies by movieId, nameLookup by movieId;
oldestBestMovies = ORDER bestMoviesData BY nameLookup::releaseDate;

DUMP oldestBestMovies;