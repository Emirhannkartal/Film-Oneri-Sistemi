import pandas as pd
import tkinter as tk
from tkinter import messagebox, Listbox, StringVar, ttk
from mlxtend.frequent_patterns import apriori, association_rules
from turler import get_film_turleri 

film_turleri = get_film_turleri()

populer_filmler = pd.read_csv("populer_filmler_filtered.csv")

film_stats = pd.read_csv("cleaned_movies.csv")

ratings = pd.read_csv("cleaned_ratings.csv")
kullanici_ids = ratings['userId'].unique()
kullanici_names = [f"Kullanıcı {user_id}" for user_id in kullanici_ids]

ratings_pivot = ratings.pivot(index='userId', columns='movieId', values='rating').fillna(0)
ratings_binary = ratings_pivot.apply(lambda x: x > 0).astype(int)  

print("Kullanıcı-Film Binary Matrisi:")
print(ratings_binary)

sik_ogrenceler = apriori(ratings_binary, min_support=0.1, use_colnames=True)

print("Sık Öğeler:")
print(sik_ogrenceler)

if not sik_ogrenceler.empty:
    kurallar = association_rules(sik_ogrenceler, metric="confidence", min_threshold=0.3)
else:
    kurallar = pd.DataFrame()

print("Birliktelik Kuralları:")
print(kurallar)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.consequents = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, antecedents, consequents):
        node = self.root
        for item in sorted(antecedents):
            if item not in node.children:
                node.children[item] = TrieNode()
            node = node.children[item]
        node.is_end = True
        node.consequents.update(consequents)

    def search(self, items):
        node = self.root
        for item in sorted(items):
            if item in node.children:
                node = node.children[item]
            else:
                return []
        return list(node.consequents) if node.is_end else []


trie = Trie()
for _, row in kurallar.iterrows():
    
    trie.insert(list(row['antecedents']), list(row['consequents']))

def print_trie(node=None, indent=""):
    if node is None:
        node = trie.root
    for child, child_node in node.children.items():
        print(f"{indent}{child}: {child_node.consequents}")
        if child_node.children:
            print_trie(child_node, indent + "  ")

print("\nTrie Yapısındaki Sonuçlar:")
print_trie()

def film_oner():
    secim = secim_var.get()
    
    if secim == "Popüler Film Önerileri":
        secilen_tur = tur_secim_var.get()
        
        genre_films = populer_filmler[populer_filmler['genre'] == secilen_tur]
        if not genre_films.empty:
           
            önerilen_film = genre_films.sample(1)['title'].values[0]
            output_var.set(f"Önerilen Popüler Film ({secilen_tur}): {önerilen_film}")
        else:
            output_var.set("Bu türde popüler film yok.")
    
    elif secim == "Kişiselleştirilmiş Film Önerileri (Türe Göre)":
        kullanici_index = kullanici_listbox.curselection()
        if not kullanici_index:
            messagebox.showwarning("Uyarı", "Bir kullanıcı seçin!")
            return
        kullanici_id = kullanici_ids[kullanici_index[0]]
    
        kullanici_filmleri = ratings[ratings['userId'] == kullanici_id]
        if not kullanici_filmleri.empty:
            izlenen_film_ids = kullanici_filmleri['movieId'].unique()
            izlenen_turler = film_stats[film_stats['movieId'].isin(izlenen_film_ids)]['genres'].dropna().str.split('|').explode().unique()
            if izlenen_turler.size > 0:
                film_öners = film_stats[film_stats['genres'].str.split('|').apply(
                        lambda x: any(tur in izlenen_turler for tur in x)
                    )]
              
                film_öners = film_öners[~film_öners['movieId'].isin(izlenen_film_ids)]
                if not film_öners.empty:
                    önerilen_film = film_öners.sample().iloc[0]['title']
                    output_var.set(f"Kullanıcı {kullanici_id} için önerilen film: {önerilen_film}")
                else:
                    output_var.set("Bu kullanıcının izlediği türe göre önerilecek film yok.")
            else:
                output_var.set("Bu kullanıcının izlediği tür bilgisi mevcut değil.")
        else:
            output_var.set("Bu kullanıcının izlediği film yok.")
    
    elif secim == "Birliktelik Kurallarına Dayalı Öneriler (Türe Göre)":
        secilen_tur = tur_secim_var.get()
        önerilen_filmler = []
       
        turdeki_film_ids = set(film_stats[film_stats['genres'].str.contains(secilen_tur)]['movieId'].tolist())
        
      
        filtrelenmis_kurallar = kurallar[kurallar['antecedents'].apply(lambda x: any(film in turdeki_film_ids for film in x))]
        for index, row in filtrelenmis_kurallar.iterrows():
            önerilen_filmler.extend(list(row['consequents']))
        
        if önerilen_filmler:
            film_isimleri = film_stats[film_stats['movieId'].isin(önerilen_filmler)]['title'].unique()
            output_var.set(f"Önerilen Filmler: {', '.join(film_isimleri)}")
        else:
            output_var.set("Bu türde önerilecek film yok.")
    
    elif secim == "Birliktelik Kurallarına Dayalı Öneriler (Film Adına Göre)":
        film_adi = film_adi_entry.get()
        if not film_adi:
            messagebox.showwarning("Uyarı", "Bir film adı girin!")
            return

        film_id_series = film_stats[film_stats['title'].str.contains(film_adi, case=False, na=False)]['movieId']
        if film_id_series.empty:
            output_var.set("Bu adda bir film bulunamadı.")
            return

        film_id = film_id_series.iloc[0]  
        onerilen_filmler = trie.search([film_id])

        if onerilen_filmler:
            film_isimleri = film_stats[film_stats['movieId'].isin(onerilen_filmler)]['title'].unique()
            output_var.set(f"'{film_adi}' için önerilen filmler: {', '.join(film_isimleri)}")
        else:
            output_var.set("Bu filmle ilişkili önerilecek film yok.")
    
    elif secim == "Kişiselleştirilmiş Film Önerileri (Film Adına Göre)":
        kullanici_index = kullanici_listbox.curselection()
        if not kullanici_index:
            messagebox.showwarning("Uyarı", "Bir kullanıcı seçin!")
            return
        kullanici_id = kullanici_ids[kullanici_index[0]]

        kullanici_filmleri = ratings[ratings['userId'] == kullanici_id]
        if kullanici_filmleri.empty:
            output_var.set("Bu kullanıcının izlediği film yok.")
            return

        izlenen_film_ids = kullanici_filmleri['movieId'].unique()
        onerilen_filmler = []
        for film_id in izlenen_film_ids:
            onerilen_filmler.extend(trie.search([film_id]))

        
        onerilen_filmler = list(set(onerilen_filmler) - set(izlenen_film_ids))
        
        if onerilen_filmler:
            film_isimleri = film_stats[film_stats['movieId'].isin(onerilen_filmler)]['title'].unique()
            output_var.set(f"Kullanıcı {kullanici_id} için önerilen filmler: {', '.join(film_isimleri)}")
        else:
            output_var.set("Bu kullanıcının izlediği filmlerle ilişkili önerilecek film yok.")

root = tk.Tk()
root.title("Film Öneri Sistemi")
root.geometry("500x400")
root.configure(bg="#f0f0f0")


style = ttk.Style()
style.theme_use("clam") 
style.configure("TButton", font=("Arial", 12), foreground="#333", background="#4CAF50")
style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
style.configure("TFrame", background="#f0f0f0")

main_frame = ttk.Frame(root, padding=(20, 10))
main_frame.pack(fill="both", expand=True)

output_var = StringVar()
output_label = ttk.Label(main_frame, textvariable=output_var, font=("Arial", 14), wraplength=400, justify="left")
output_label.pack(pady=10)

secim_var = StringVar(value="Popüler Film Önerileri")
secim_label = ttk.Label(main_frame, text="Öneri Türü Seçin:")
secim_label.pack(anchor="w", pady=5)

secim_options = [
    "Popüler Film Önerileri",
    "Kişiselleştirilmiş Film Önerileri (Türe Göre)",
    "Birliktelik Kurallarına Dayalı Öneriler (Türe Göre)",
    "Birliktelik Kurallarına Dayalı Öneriler (Film Adına Göre)",
    "Kişiselleştirilmiş Film Önerileri (Film Adına Göre)"
]
secim_menu = ttk.Combobox(main_frame, textvariable=secim_var, values=secim_options, state="readonly", width=40)
secim_menu.pack()


kullanici_label = ttk.Label(main_frame, text="Kullanıcı Seçin:")
kullanici_listbox = Listbox(main_frame, height=5, font=("Arial", 10), selectbackground="#4CAF50")
for kullanici in kullanici_names:
    kullanici_listbox.insert(tk.END, kullanici)

film_adi_label = ttk.Label(main_frame, text="Film Adını Girin:")
film_adi_entry = ttk.Entry(main_frame, font=("Arial", 10))

tur_secim_var = StringVar(value=film_turleri[0])
tur_label = ttk.Label(main_frame, text="Film Türü Seçin:")
tur_menu = ttk.Combobox(main_frame, textvariable=tur_secim_var, values=film_turleri, state="readonly", width=40)

def guncelle_arayuz(*args):
    secim = secim_var.get()
  
    kullanici_label.pack_forget()
    kullanici_listbox.pack_forget()
    film_adi_label.pack_forget()
    film_adi_entry.pack_forget()
    tur_label.pack_forget()
    tur_menu.pack_forget()
     
    if secim in [
        "Kişiselleştirilmiş Film Önerileri (Türe Göre)",
        "Kişiselleştirilmiş Film Önerileri (Film Adına Göre)"
    ]:
        kullanici_label.pack(anchor="w", pady=5)
        kullanici_listbox.pack()

    if secim in [
        "Popüler Film Önerileri",
        "Kişiselleştirilmiş Film Önerileri (Türe Göre)",
        "Birliktelik Kurallarına Dayalı Öneriler (Türe Göre)"
    ]:
        tur_label.pack(anchor="w", pady=5)
        tur_menu.pack()
    
    if secim == "Birliktelik Kurallarına Dayalı Öneriler (Film Adına Göre)":
        film_adi_label.pack(anchor="w", pady=5)
        film_adi_entry.pack()
    
    if secim == "Kişiselleştirilmiş Film Önerileri (Film Adına Göre)":
        film_adi_label.pack(anchor="w", pady=5)
        film_adi_entry.pack()
secim_var.trace('w', guncelle_arayuz)
guncelle_arayuz()
oner_button = ttk.Button(main_frame, text="Öneri Getir", command=film_oner, style="TButton")
oner_button.pack(pady=20)
root.mainloop()
