import pandas as pd


ratings_path = "c:/Users/emirh/OneDrive/Masaüstü/proje/archive/rating.csv"
movies_path = "c:/Users/emirh/OneDrive/Masaüstü/proje/archive/movie.csv"

ratings = pd.read_csv(ratings_path)
movies = pd.read_csv(movies_path)


ratings_cleaned = ratings.dropna(subset=['userId', 'movieId', 'rating', 'timestamp'])

ratings_cleaned = ratings_cleaned[ratings_cleaned['rating'] >= 3.0]


movie_counts = ratings_cleaned.groupby('movieId').size().reset_index(name='user_count')


sufficient_views = movie_counts[movie_counts['user_count'] >= 10]['movieId']
ratings_cleaned = ratings_cleaned[ratings_cleaned['movieId'].isin(sufficient_views)]


average_ratings = ratings_cleaned.groupby('movieId')['rating'].mean().reset_index()
average_ratings.rename(columns={'rating': 'average_rating'}, inplace=True)


ratings_with_avg = pd.merge(ratings_cleaned, average_ratings, on='movieId')

ratings_cleaned = ratings_with_avg[ratings_with_avg['average_rating'] >= 4.0]

ratings_cleaned = ratings_cleaned.drop(columns=['timestamp'])


movies_cleaned = movies.dropna(subset=['title', 'genres'])


izlenmis_filmler = ratings_cleaned['movieId'].unique()
movies_cleaned = movies_cleaned[movies_cleaned['movieId'].isin(izlenmis_filmler)]


ratings_cleaned = ratings_cleaned.groupby('userId').filter(lambda x: len(x) <= 20)


user_groups = ratings_cleaned.groupby('userId')

final_ratings = pd.DataFrame()

for user_id, group in user_groups:
    if len(group) > 10:
      
        avg_ratings = group.groupby('movieId')['rating'].mean()
    
        to_drop = avg_ratings.nsmallest(len(group) - 20).index
   
        group = group[~group['movieId'].isin(to_drop)]
    
    final_ratings = pd.concat([final_ratings, group])


final_ratings.to_csv("cleaned_ratings.csv", index=False)
movies_cleaned.to_csv("cleaned_movies.csv", index=False)


print("\nTemizlenmiş Rating Veri Seti:")
print(final_ratings.info())
print(final_ratings.head())

print("\nTemizlenmiş Movie Veri Seti:")
print(movies_cleaned.info())
print(movies_cleaned.head())
