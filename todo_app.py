import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo アプリケーション")
        
        # データベース初期化
        self.init_database()
        
        # UIの作成
        self.create_ui()
        
        # タスク一覧の更新
        self.update_task_list()
    
    def init_database(self):
        """データベースとテーブルの初期化"""
        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def create_ui(self):
        """UIコンポーネントの作成"""
        # タスク入力フレーム
        input_frame = ttk.Frame(self.root, padding="5")
        input_frame.grid(row=0, column=0, sticky=(tk.W + tk.E))
        
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.grid(row=0, column=0, padx=5)
        
        ttk.Button(input_frame, text="追加", command=self.add_task).grid(row=0, column=1, padx=5)
        
        # タスク一覧フレーム
        list_frame = ttk.Frame(self.root, padding="5")
        list_frame.grid(row=1, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))
        
        self.task_list = ttk.Treeview(list_frame, columns=('Task', 'Created', 'Status'), show='headings')
        self.task_list.heading('Task', text='タスク')
        self.task_list.heading('Created', text='作成日時')
        self.task_list.heading('Status', text='状態')
        self.task_list.grid(row=0, column=0, sticky=(tk.W + tk.E + tk.N + tk.S))
        
        # スクロールバーの追加
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.task_list.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N + tk.S))
        self.task_list.configure(yscrollcommand=scrollbar.set)
        
        # ボタンフレーム
        button_frame = ttk.Frame(self.root, padding="5")
        button_frame.grid(row=2, column=0, sticky=(tk.W + tk.E))
        
        ttk.Button(button_frame, text="完了", command=self.complete_task).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="削除", command=self.delete_task).grid(row=0, column=1, padx=5)
    
    def add_task(self):
        """新しいタスクの追加"""
        task = self.task_entry.get().strip()
        if task:
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute('INSERT INTO tasks (task, created_at) VALUES (?, ?)',
                              (task, created_at))
            self.conn.commit()
            self.task_entry.delete(0, tk.END)
            self.update_task_list()
        else:
            messagebox.showwarning("警告", "タスクを入力してください")
    
    def complete_task(self):
        """選択したタスクを完了状態に更新"""
        selected_item = self.task_list.selection()
        if selected_item:
            task_id = self.task_list.item(selected_item[0])['values'][3]  # IDを取得
            self.cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
            self.conn.commit()
            self.update_task_list()
        else:
            messagebox.showwarning("警告", "タスクを選択してください")
    
    def delete_task(self):
        """選択したタスクの削除"""
        selected_item = self.task_list.selection()
        if selected_item:
            task_id = self.task_list.item(selected_item[0])['values'][3]  # IDを取得
            self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            self.conn.commit()
            self.update_task_list()
        else:
            messagebox.showwarning("警告", "タスクを選択してください")
    
    def update_task_list(self):
        """タスク一覧の更新"""
        for item in self.task_list.get_children():
            self.task_list.delete(item)
        
        self.cursor.execute('SELECT id, task, created_at, completed FROM tasks ORDER BY created_at DESC')
        for task in self.cursor.fetchall():
            status = "完了" if task[3] else "未完了"
            self.task_list.insert('', tk.END, values=(task[1], task[2], status, task[0]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()