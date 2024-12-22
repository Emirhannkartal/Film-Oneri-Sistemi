import pandas as pd

ratings = pd.read_csv("c:/Users/emirh/OneDrive/Masaüstü/proje/archive/rating.csv")
movies = pd.read_csv("c:/Users/emirh/OneDrive/Masaüstü/proje/archive/movie.csv")

def get_film_turleri():
    turler = set()
    for tur_list in movies['genres']:  
        for tur in tur_list.split('|'):
            turler.add(tur)
    return list(turler) 


tur_sayilari = {}

for tur_list in movies['genres']:
    for tur in tur_list.split('|'):
        if tur in tur_sayilari:
            tur_sayilari[tur] += 1  
        else:
            tur_sayilari[tur] = 1  

tur_sayilari_df = pd.DataFrame(list(tur_sayilari.items()), columns=['Tür', 'Film Sayısı'])
tur_sayilari_df = tur_sayilari_df.sort_values(by='Film Sayısı', ascending=False)

print(tur_sayilari_df)


