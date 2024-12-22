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
