import pandas as pd


ratings = pd.read_csv("c:/Users/emirh/OneDrive/Masaüstü/proje/archive/rating.csv")
movies = pd.read_csv("c:/Users/emirh/OneDrive/Masaüstü/proje/archive/movie.csv")


merged_data = pd.merge(ratings, movies, on='movieId')


film_stats = merged_data.groupby(['movieId', 'title', 'genres']).agg(
    izlenme_sayisi=('userId', 'count'),        
    begeni_sayisi=('rating', 'mean')           
).reset_index()


populer_filmler = film_stats.copy()
populer_filmler['genres'] = populer_filmler['genres'].str.split('|') 


result = []
for genre in populer_filmler['genres'].explode().unique():  
    genre_filmler = populer_filmler[populer_filmler['genres'].apply(lambda x: genre in x)]
    genre_populer = genre_filmler.sort_values(by=['izlenme_sayisi', 'begeni_sayisi'], ascending=False).head(50)
    genre_populer['genre'] = genre
    result.append(genre_populer)


final_result = pd.concat(result, ignore_index=True)


final_result_filtered = final_result[['title', 'genre', 'izlenme_sayisi']]

final_result_filtered.to_csv("populer_filmler_filtered.csv", index=False)

print(final_result_filtered)
