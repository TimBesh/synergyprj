# Импорт библиотек
import tkinter as tk 
from tkinter import ttk 
import sqlite3 

class Main(tk.Frame):  #класс главного окона
    def __init__(self, root): # передаём сюда главное окно
        super().__init__(root) # передаём сюда все свойства нашего главного окна
        self.init_main()
        self.db = db # добавляем чтобы могли обращаться к бд
        self.view_records()

    def init_main(self): # создаём метод для хранения и иницилизации объектов графического интерфейса 
        toolbar = tk.Frame(bg='#d7d8e0', bd=2) #тут находятся все кнопки
        toolbar.pack(side=tk.TOP, fill=tk.X) # помещаем на главное окно

        # создаём кнопки

        self.add_img = tk.PhotoImage(file='.\\img\\add.png') # добавление
        btn_add= tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog) 
        btn_add.pack(side=tk.LEFT)

        self.del_img = tk.PhotoImage(file='.\\img\\del.png') # удаления
        btn_del = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.del_img, command=self.delete_record) 
        btn_del.pack(side=tk.LEFT)

        self.srch_img = tk.PhotoImage(file='.\\img\\srch.png') # поиска
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.srch_img, command=self.open_search_dialog) 
        btn_search.pack(side=tk.LEFT)

        self.chng_img = tk.PhotoImage(file='.\\img\\chng.png') # изменения
        btn_change = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.chng_img, command=self.open_update_dialog) 
        btn_change.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='.\\img\\refresh.png') # обновления
        btn_change = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_records) 
        btn_change.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('id', 'name', 'tel', 'email', 'salary'), height=45, show="headings")
        # создаём таблицу со значениями в приложении
        self.tree.column('id', width=30, anchor=tk.CENTER) 
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=100, anchor=tk.CENTER)
        # прописываем человекочитаемые названия, те были для программы
        self.tree.heading('id', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='Е=mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT)

    def open_dialog(self): # метод вызова дочернего окна Child с главного окна
        Child()

    def open_update_dialog(self): # метод вызова дочернего окна Update с главного окна
        Update()

    def records(self, name, tel, email, salary): # метод для добавления данных
        self.db.insert_data(name, tel, email, salary)
        self.view_records() 

    def view_records(self): #  Отображение данных в тривиев
        self.db.cur.execute('SELECT * FROM prj')
        [self.tree.delete(i) for i in self.tree.get_children()] 
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()] 
        

    def delete_record(self): # функция удаления
        for select_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM prj WHERE id=?', (self.tree.set(select_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def update_record(self, name, tel, email, salary): # функция изменения
        self.db.cur.execute('UPDATE prj SET name=?, tel=?, email=?, salary=? WHERE id=?', (name, tel, email, salary, self.tree.set(self.tree.selection()[0], "#1")))
        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self): # функция открывания дочернего окна сёрч
        Search()
    
    def search_records(self, name): # функция поиска
        self.db.cur.execute("SELECT * FROM prj WHERE name LIKE ?", ("%" + name + "%", ))
        
        [self.tree.delete(i) for i in self.tree.get_children()]

        [self.tree.insert("", "end", values=row) for row in self.db.cur.fetchall()] # метод поиска по ФИО



class Child(tk.Toplevel): # создадим первое дочернее окно, функционал будет в новом окне программы открываться 
    def __init__(self): # дочернее окно может всё тоже самое что и главное окно
        super().__init__(root)
        self.init_child() # для хранения и иницилиазации данных
        self.view = app # нужен чтобы обращаться к методам из главного окна

# дочернее окно
    def init_child(self):
        self.title('Добававить сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set() # перехватываем все события
        self.focus_set()  # перехватываем фокус


        # создаём форму для добавления нового контакта,в init_child т.к занимается хранением и иницилизацией граф. элементов интерфейса
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50) # создаём и размещаем лейбел
        label_select = tk.Label(self, text='Телефон:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail:')
        label_sum.place(x=50, y=110)
        label_sal = tk.Label(self, text='Зарплата:')
        label_sal.place(x=50, y=140)
        
        self.entry_name = ttk.Entry(self) #строки для ввода
        self.entry_name.place(x=200,y=50)
        self.entry_email = ttk.Entry(self) 
        self.entry_email.place(x=200,y=80)
        self.entry_tel = ttk.Entry(self) 
        self.entry_tel.place(x=200,y=110)
        self.entry_salary = ttk.Entry(self) 
        self.entry_salary.place(x=200,y=140)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy) # кнопка для закрытия доч окна
        self.btn_cancel.place(x=300, y=170)
        
        self.btn_ok = ttk.Button(self, text='Добавить') # чтобы добавлять данные
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(), # чтобы изменялись при нажатии лкм
                                           self.entry_email.get(),
                                           self.entry_tel.get(),
                                           self.entry_salary.get())) 
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')  # чтобы потом удалялось

class Update(Child): # класс дочернего окна для редактирования
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать информацию сотрудника компании')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=220, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_email.get(),
                                              self.entry_tel.get(),
                                              self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
    
    def default_data(self):
        self.db.cur.execute('SELECT * FROM prj WHERE id=?', (self.view.tree.set(self.view.tree.selection() [0], '#1'),))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3]) # чтобы изменять
        self.entry_salary.insert(0, row[4])

# класс поиска
class Search(tk.Toplevel):
    def __init__(self): 
        super().__init__()
        self.init_search()
        self.db = db
        self.view = app
    
    def init_search(self): # окно поиска
        self.title('Поиск сотрудника по ФИО')
        self.geometry('300x300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='ФИО')
        label_search.place(x=60, y=30)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=115, y=30, width=150)

        btn_cancel = ttk.Button(self, text='Отменить', command=self.destroy) # кнопка отмены
        btn_cancel.place(x=195, y=60)

        btn_search = ttk.Button(self, text='Поиск') # кнопка поиска
        btn_search.place(x=115, y=60)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get())) # чтобы на ЛКМ искало и потом закрывалось
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

# база данных
class DB: 
    def __init__(self):
        self.conn = sqlite3.connect('prj.db') # подключаемся к скьлайт три
        self.cur = self.conn.cursor() # создаём таблицу ниже
        self.cur.execute('''CREATE TABLE IF NOT EXISTS prj (
            id INTEGER PRIMARY KEY,             
            name TEXT,
            tel TEXT,
            email TEXT,
            salary TEXT                         
        );
        ''')
        self.conn.commit() # чтобы сохранились изменения

    def insert_data(self, name, tel, email, salary): # Метод чтобы вставлять данные в таблицу срабатывающий при нажатии кнопки добавить
        self.cur.execute('INSERT INTO prj (name, tel, email, salary) VALUES (?, ?, ?, ?);', (name, tel, email, salary)) 
        self.conn.commit()

    

# главное окно
if __name__ == '__main__':  # создаём главное окно
    root = tk.Tk() # наше главное окно
    db = DB() # создаём экземпляр класса чтобы мы к нему могли обращаться
    app = Main(root)
    app.pack()

    root.title('Список сотрудников компании') # даём окну заголовок
    root.geometry('800x450') # размеры окна
    root.resizable(False, False) # значение изменения размеров окна
    root.mainloop() # цикл событий