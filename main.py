import tkinter as tk
from tkinter import simpledialog
import sqlite3

class Library:
    def __init__(self, root):
        self.root = root
        self.root.title("Библиотека")
        self.root.geometry("600x400")
        
        self.init_database()
        
        self.create_widgets()
        self.show_books()

    def init_database(self):
        self.conn = sqlite3.connect('library.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title NVARCHAR(50),
                author NVARCHAR(50),
                status NVARCHAR(50)
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        tk.Button(self.root, text="Добавить книгу", command=self.add_book).pack(pady=5)
        tk.Button(self.root, text="Выдать книгу", command=self.give_book).pack(pady=5)
        tk.Button(self.root, text="Вернуть книгу", command=self.return_book).pack(pady=5)
        tk.Button(self.root, text="Обновить", command=self.show_books).pack(pady=5)
        
        self.listbox = tk.Listbox(self.root, width=60, height=15)
        self.listbox.pack(pady=10)

    def add_book(self):
        title = simpledialog.askstring("Добавить книгу", "Название книги:")
        if title:
            author = simpledialog.askstring("Добавить книгу", "Автор:")
            if author:
                self.cursor.execute("INSERT INTO books (title, author, status) VALUES (?, ?, ?)", 
                    (title, author, "в наличии"))
                self.conn.commit()
                self.show_books()

    def give_book(self):
        selection = self.listbox.curselection()
        if selection:
            book_text = self.listbox.get(selection[0])
            book_id = book_text.split(".")[0]
            
            reader = simpledialog.askstring("Выдать книгу", "Имя читателя:")
            if reader:
                self.cursor.execute("UPDATE books SET status = ? WHERE id = ?", 
                    (f"выдана: {reader}", book_id))
                self.conn.commit()
                self.show_books()

    def return_book(self):
        selection = self.listbox.curselection()
        if selection:
            book_text = self.listbox.get(selection[0])
            book_id = book_text.split(".")[0]
            
            self.cursor.execute("UPDATE books SET status = ? WHERE id = ?", 
             ("В наличии", book_id))
            self.conn.commit()
            self.show_books()

    def show_books(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        
        for book in books:
            status = "В наличии" if book[3] == "В наличии" else f"{book[3]}"
            self.listbox.insert(tk.END, f"{book[0]}. {book[1]} - {book[2]} ({status})")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = Library(root)
    root.mainloop()