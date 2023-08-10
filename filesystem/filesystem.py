import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess

class GUIFileSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI File System")
        self.current_directory = os.getcwd()
        
        self.tree = ttk.Treeview(root)
        self.tree.heading('#0', text='File System')
        self.tree.bind("<Double-1>", self.on_tree_double_click)
        
        self.tree.pack(expand=True, fill='both')
        self.update_tree(self.current_directory)
        
        self.create_file_button = ttk.Button(root, text="Create File", command=self.create_file)
        self.create_file_button.pack(side="left")
        
        self.create_dir_button = ttk.Button(root, text="Create Directory", command=self.create_directory)
        self.create_dir_button.pack(side="left")
        
        self.view_button = ttk.Button(root, text="View Content", command=self.view_content)
        self.view_button.pack(side="left")
        
        self.modify_button = ttk.Button(root, text="Modify Content", command=self.modify_content)
        self.modify_button.pack(side="left")
        
        self.delete_button = ttk.Button(root, text="Delete", command=self.delete_item)
        self.delete_button.pack(side="left")
        
        self.refresh_button = ttk.Button(root, text="Refresh", command=self.refresh)
        self.refresh_button.pack(side="left")
        
    def update_tree(self, path):
        self.tree.delete(*self.tree.get_children())
        for item in os.listdir(path):
            self.tree.insert('', 'end', text=item, open=False)
    
    def on_tree_double_click(self, event):
        item = self.tree.selection()[0]
        item_text = self.tree.item(item, "text")
        new_path = os.path.join(self.current_directory, item_text)
        
        if os.path.isdir(new_path):
            self.current_directory = new_path
            self.update_tree(new_path)
    
    def create_file(self):
        name = simpledialog.askstring("Create File", "Enter file name (without extension):")
        if name:
            new_path = os.path.join(self.current_directory, name + '.txt')
            if os.path.exists(new_path):
                messagebox.showerror("Error", "File already exists.")
                return
            with open(new_path, 'w'):
                pass  # Create an empty file
            self.update_tree(self.current_directory)
            messagebox.showinfo("Success", f"File '{name}.txt' created successfully.")
    
    def create_directory(self):
        name = simpledialog.askstring("Create Directory", "Enter directory name:")
        if name:
            new_path = os.path.join(self.current_directory, name)
            if os.path.exists(new_path):
                messagebox.showerror("Error", "Directory already exists.")
                return
            os.mkdir(new_path)
            self.update_tree(self.current_directory)
            messagebox.showinfo("Success", f"Directory '{name}' created successfully.")
    
    def view_content(self):
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        item_path = os.path.join(self.current_directory, item_text)
        
        if os.path.isfile(item_path):
            with open(item_path, 'r') as file:
                content = file.read()
                self.show_text_content(content)
        else:
            messagebox.showerror("Error", "Select a file to view its content.")
    
    def show_text_content(self, content):
        text_window = tk.Toplevel(self.root)
        text_window.title("File Content")
        
        text_widget = tk.Text(text_window)
        text_widget.pack(expand=True, fill="both")
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
    
    def modify_content(self):
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        item_path = os.path.join(self.current_directory, item_text)
        
        if os.path.isfile(item_path):
            try:
                subprocess.run(['start', '', item_path], check=True, shell=True)
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "Unable to open the file with the default text editor.")
        else:
            messagebox.showerror("Error", "Select a file to modify its content.")
    
    def delete_item(self):
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        item_path = os.path.join(self.current_directory, item_text)
        
        if os.path.isdir(item_path):
            if messagebox.askyesno("Confirm Deletion", f"Delete directory '{item_text}'?"):
                os.rmdir(item_path)
                messagebox.showinfo("Success", f"Directory '{item_text}' deleted successfully.")
        else:
            if messagebox.askyesno("Confirm Deletion", f"Delete file '{item_text}'?"):
                os.remove(item_path)
                messagebox.showinfo("Success", f"File '{item_text}' deleted successfully.")
        
        self.update_tree(self.current_directory)
    
    def refresh(self):
        self.update_tree(self.current_directory)

def main():
    root = tk.Tk()
    app = GUIFileSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
