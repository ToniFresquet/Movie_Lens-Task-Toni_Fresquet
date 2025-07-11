import pandas as pd

df_ratings = pd.read_csv('data/ml-1m/ratings.dat', sep='::', names=['userId', 'movieId', 'rating', 'timestamp'], engine='python')
df_movies = pd.read_csv('data/ml-1m/movies.dat', sep='::', names=['movieId', 'title', 'genres'], engine='python', encoding='ISO-8859-1')	
df_users = pd.read_csv('data/ml-1m/users.dat', sep='::', names=['userId', 'Gender', 'Age', 'Occupation', 'Zip-code'], engine='python')


def get_top_10_movies_by_rating():
	df_ratings['rating'] = pd.to_numeric(df_ratings['rating'], errors='coerce')									#Convert ratings from object (string) to numeric type

	df_ratings_by_movieID = df_ratings.groupby('movieId')['rating'].agg(['mean', 'count'])						#Group by movieId and calculate mean and count of ratings
	df_ratings_by_movieID = df_ratings_by_movieID[df_ratings_by_movieID['count'] >= 10]							#Remove movies with less than 10 ratings

	df_top10_rated_movies = df_ratings_by_movieID.sort_values(by=('mean'), ascending=False).head(10)  			

	df_merged = pd.merge(df_top10_rated_movies, df_movies, on='movieId')  										

	print("The following are the top 10 best rated movies (with at least 10 ratings):")
	print(df_merged[['title', 'genres', 'mean', 'count']].head(10))  


def get_age_group_with_most_ratings():
	
	df_rating_per_user = df_ratings.groupby('userId').size().reset_index(name='rating_count')					

	df_rating_per_age_group = pd.merge(df_users[['userId', 'Age']], df_rating_per_user, on='userId')  			
	df_rating_per_age_group = df_rating_per_age_group.groupby('Age')['rating_count'].sum().reset_index()		
	df_rating_per_age_group = df_rating_per_age_group.sort_values(by=('rating_count'), ascending=False) 		

	age_mapping = {
        1: "< 18",
        18: "18-24",
        25: "25-34",
        35: "35-44",
        45: "45-49",
        50: "50-55",
        56: "56+"
    }

	top_age_group = df_rating_per_age_group.iloc[0] 															# Get the age group with the most ratings
	top_age_group_label = age_mapping.get(top_age_group['Age'], "Unknown age group")

	print("The age group with more ratings is the group:", top_age_group_label)
	print("With a total of:", df_rating_per_age_group['rating_count'].iloc[0], "ratings.")


if __name__ == "__main__":
	print("Question #1: Which are the Top 10 best rated movies (consider only movies which have at least 10 ratings)?")
	print("--"*25)
	get_top_10_movies_by_rating() 
	print("--"*25)
	print("\n\n")
	print("Question #2: Which age group give the most ratings overall?")
	print("--"*25)
	get_age_group_with_most_ratings()
	print("--"*25)