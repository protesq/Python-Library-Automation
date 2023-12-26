import os
import sqlite3
import sys
import tkinter as tk
from tkinter import END, messagebox
from tkcalendar import DateEntry
from tkinter import ttk


def main():
    global show_button, main_page, user_add_entry, listbox, table2_entry, table3_entry, table4_entry, users_combobox
    main_page = tk.Tk()
    main_page.title("Anasayfa")

    screen_width = main_page.winfo_screenwidth()
    screen_height = main_page.winfo_screenheight()

    window_width = 1920
    window_height = 1080

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    main_page.geometry(f"{window_width}x{window_height}+{x}+{y}")
    main_page.configure(bg="white")
######################-Frame1-####################################
    frame = tk.Frame(main_page, bg="white")
    frame.pack(pady=20, padx=10, anchor="nw")

    labelfont = ("Arial", 15)
    label = tk.Label(frame, text="Kullanıcı Seç:", font=labelfont)
    label.pack(side=tk.LEFT, padx=10)

    users_combobox = ttk.Combobox(frame, width=20)
    users_combobox.pack(side=tk.LEFT, padx=10)

    populate_users_combobox(users_combobox)

    show_button = tk.Button(frame, text="Kullanıcının Kitaplarını Göster", command=lambda: get_selected_user_books(users_combobox))
    show_button.pack(side=tk.LEFT, padx=10)
    
    labelp = tk.Label(frame, text="Kullanıcı Adı:", font=labelfont)
    labelp.pack(side=tk.LEFT, padx=10)


    users_combobox = ttk.Combobox(frame, width=20)
    users_combobox.pack(side=tk.LEFT, padx=10)

    populate_users_combobox(users_combobox)

    
    label2 = tk.Label(frame, text="Kitap Adı:", font=labelfont)
    label2.pack(side=tk.LEFT, padx=10)

    table2_entry = tk.Entry(frame, width=40, show="")
    table2_entry.pack(side=tk.LEFT, padx=10)

    label3 = tk.Label(frame, text="Eklenme Tarihi:", font=labelfont)
    label3.pack(side=tk.LEFT, padx=10)

    table3_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    table3_entry.pack(side=tk.LEFT, padx=10)

    label4 = tk.Label(frame, text="Geri Alma Tarihi:", font=labelfont)
    label4.pack(side=tk.LEFT, padx=10)

    table4_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
    table4_entry.pack(side=tk.LEFT, padx=10)

    add_button = tk.Button(frame, text="Ekle", command=add_data)
    add_button.pack(side=tk.LEFT, padx=10)
##################################################################
######################-Frame2-####################################
##################################################################
    frame2 = tk.Frame(main_page, bg="white")
    frame2.pack(pady=20, padx=10, anchor="nw")

    label3 = tk.Label(frame2, text="Kullanıcı İsmi:", font=labelfont)
    label3.pack(side=tk.LEFT, padx=10)   

    user_add_entry = tk.Entry(frame2, width=25, show="")
    user_add_entry.pack(side=tk.LEFT, padx=10)

    k_add_button = tk.Button(frame2, text="Kaydet", command=add_user)
    k_add_button.pack(side=tk.LEFT, padx=10)

    k_g_button = tk.Button(frame2, text="Kullanıcı Güncelleme", command=update_user_window)
    k_g_button.pack(side=tk.LEFT, padx=10)

    label5 = tk.Label(frame2, text="Veri seçip sil'e tıklayınız !", font=labelfont)
    label5.pack(side=tk.LEFT, padx=10)

    k_delete_button = tk.Button(frame2, text="Sil", command=delete_selected_book)
    k_delete_button.pack(side=tk.LEFT, padx=10)
    
########################---FRAME3----############################
   # frame3 = tk.Frame(main_page, bg="white")
    #frame3.pack(pady=20, padx=10, anchor="nw")

##################################################################
    listbox = tk.Listbox(main_page, width=500,height=60)
    listbox.pack(side=tk.RIGHT, pady=20, anchor="nw")

    main_page.mainloop()

def refresh_combobox():
    populate_users_combobox(users_combobox)


def create_table():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS kitaplar2 (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        k_adi TEXT,
        kitap_adi TEXT,
        eklenme_tarihi TEXT,
        gerialma_tarihi TEXT
    )
    '''
    cursor.execute(create_table_query)
    connection.commit()
    connection.close()

def add_data():
    create_table()  # Tablo varsa oluştur, yoksa atla
    
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    
    table2_entry_text = table2_entry.get()
    table3_entry_date = table3_entry.get()
    table4_entry_date = table4_entry.get()
    k_entry_text = users_combobox.get()
    
    add_book = '''
    INSERT INTO kitaplar2 (k_adi, kitap_adi, eklenme_tarihi, gerialma_tarihi)
    VALUES (?, ?, ?, ?)
    '''
    
    try:
        cursor.execute(add_book, (k_entry_text, table2_entry_text, table3_entry_date, table4_entry_date))
        connection.commit()
        messagebox.showinfo('Başarıyla eklendi!', 'Kitap eklendi!')
    except sqlite3.Error as e:
        print(e)
        messagebox.showerror('Hata', f'Veritabanına kaydedilirken bir hata oluştu: {str(e)}')
    finally:
        connection.close()

def populate_users_combobox(combobox):
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT k_adi FROM kitaplar2")
    users = cursor.fetchall()

    connection.close()

    combobox['values'] = [user[0] for user in users] if users else []



def get_selected_user_books(combobox):
    selected_user = combobox.get()

    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM kitaplar2 WHERE k_adi = ?", (selected_user,))
        user_books = cursor.fetchall()

        listbox.delete(0, tk.END)
        if user_books:
            for book in user_books:
                listbox.insert(tk.END, f"ID: {book[0]}, Kullanıcı Adı: {book[1]}, Kitap Adı: {book[2]}, Eklenme Tarihi: {book[3]}, Geri Alma Tarihi: {book[4]}")
        else:
            messagebox.showinfo('Bilgi', 'Kullanıcıya ait kitap bulunamadı.')
    except sqlite3.Error as e:
        print("Veritabanı hatası:", e)
    finally:
        connection.close()

def delete_selected_book():

    selected_book = listbox.curselection()  # Seçilen öğenin indeksini al
    if selected_book:  # Eğer bir öğe seçildiyse devam et
        confirmation = messagebox.askyesno("Onay", "Bu kitabı silmek istediğinizden emin misiniz?")
        if confirmation:
            selected_book_id = listbox.get(selected_book[0]).split(':')[1].split(',')[0].strip()  # Öğenin ID'sini al
            selected_user = users_combobox.get()  # Seçilen kullanıcıyı al
            connection = sqlite3.connect('database.sqlite')
            cursor = connection.cursor()

            try:
                cursor.execute("DELETE FROM kitaplar2 WHERE id = ? AND k_adi = ?", (selected_book_id, selected_user))
                connection.commit()
                messagebox.showinfo("Bilgi", "Kitap başarıyla silindi.")
                get_selected_user_books(users_combobox)  # Listeyi güncelle
            except sqlite3.Error as e:
                print("Veritabanı hatası:", e)
            finally:
                connection.close()

def add_user():
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    
    user_add_text = user_add_entry.get()
    
    add_book = '''
    INSERT INTO kitaplar2 (k_adi)
    VALUES (?)
    '''
    
    try:
        cursor.execute(add_book, (user_add_text,))
        connection.commit()
        messagebox.showinfo('Başarıyla eklendi!', 'Kullanıcı eklendi!')
        refresh = "SELECT k_adi FROM kitaplar2"
        cursor.execute(refresh)
        data = cursor.fetchall()
        users_combobox['values'] = data
    except sqlite3.Error as e:
        print(e)
        messagebox.showerror('Hata', f'Veritabanına kaydedilirken bir hata oluştu: {str(e)}')
    finally:
        connection.close()


def update_user_window():
    update_window = tk.Toplevel(main_page)
    update_window.title("Kullanıcı Güncelleme")

    labelfont = ("Arial", 15)

    labelid = tk.Label(update_window, text="Kullanıcı Seç:", font=labelfont)
    labelid.pack(side=tk.LEFT, padx=10)

    # Database'den kullanıcıları çek
    connection = sqlite3.connect('database.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT k_adi FROM kitaplar2")
    users = cursor.fetchall()
    connection.close()

    users_combobox = ttk.Combobox(update_window, width=25, values=users)
    users_combobox.pack(side=tk.LEFT, padx=10)

    label4 = tk.Label(update_window, text="Yeni Kullanıcı İsmi:", font=labelfont)
    label4.pack(side=tk.LEFT, padx=10)

    k_g_entry = tk.Entry(update_window, width=25, show="")
    k_g_entry.pack(side=tk.LEFT, padx=10)

    def close_update_window():
        update_window.destroy()
        main_page.deiconify() 
        populate_users_combobox(users_combobox)

    def perform_update():
        new_username = k_g_entry.get()
        selected_user = users_combobox.get()

        if new_username and selected_user:
            connection = sqlite3.connect('database.sqlite')
            cursor = connection.cursor()

            try:
                cursor.execute("UPDATE kitaplar2 SET k_adi = ? WHERE k_adi = ?", (new_username, selected_user))
                connection.commit()

                # Kullanıcıları güncelle
                cursor.execute("SELECT DISTINCT k_adi FROM kitaplar2")
                updated_users = cursor.fetchall()
                users_combobox['values'] = updated_users
            except sqlite3.Error as e:
                print(e)
                messagebox.showerror('Hata !', f'Güncellenirken bir hata oluştu. Hata: {str(e)}')
            finally:
                connection.close()
                close_update_window()  # Güncelleme penceresini kapat ve ana pencereye geri dön

    update_button = tk.Button(update_window, text="Güncelle", command=perform_update)
    update_button.pack()

    back_button = tk.Button(update_window, text="Geri Dön", command=close_update_window)
    back_button.pack()

    main_page.withdraw()    
if __name__ == '__main__':
    main()
