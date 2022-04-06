# Import modules for tkinter application
from textwrap import fill
from tkinter import *
import json
from tkinter.ttk import Style, Treeview
from turtle import bgcolor, left
from uuid import uuid4
from prompt import *

class ProjectTreeNode:
    def __init__(self, text, isFolder=True):
        self.text = text
        self.children = []
        self.isFolder = isFolder
        self.id = uuid4()

project_tree = []

windowTitle = ""

with open('.version') as version_file:
    version = version_file.read().split('.')
    major = version[0]
    minor = version[1]
    patch = version[2]
    build = version[3]
    windowTitle = f'API HAWK - {major}.{minor}.{patch} build {int(build)}'

# Get the settings out of settings.json
settings = {}

with open('settings.json') as json_file:
    settings = json.load(json_file)

# Create main window
root = Tk()

icon_folder = PhotoImage(file="assets/folder.png")
icon_get_request = PhotoImage(file="assets/get-request.png")

# Set window icon from assets
img = PhotoImage(file='./assets/logo.png')
root.iconphoto(True, img)

# Styling of the application
style = Style()
style.configure('Treeview', 
    fieldbackground = settings['colorSceme']['background2'],
    fieldforeground = settings['colorSceme']['foreground'],
    foreground = settings['colorSceme']['foreground'],
    background = settings['colorSceme']['background2'],
    rowheight = 30
)

style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

style.layout('Treeview.Item', 
             [('Treeitem.padding',
               {'children': [('Treeitem.indicator', {'side': 'left', 'sticky': ''}),
                 ('Treeitem.image', {'side': 'left', 'sticky': ''}),
                 ('Treeitem.text', {'side': 'left', 'sticky': ''})],
                'sticky': 'nswe'})])

style.map('Treeview',
    background = [('selected', settings['colorSceme']['background_light'])],
    foreground = [('selected', settings['colorSceme']['foreground_light'])]
)

# Set app background from settings
root['bg'] = settings['colorSceme']['background']

# Create a file hierarchy at the left on the window
endpoint_hierarchy = Treeview(root, show='tree')
scrollbar = Scrollbar(root, orient="vertical", command=endpoint_hierarchy.yview)
scrollbar.pack(side='left', fill='y')

endpoint_hierarchy.configure(yscrollcommand=scrollbar.set)

endpoint_hierarchy.heading('#0',text='directory:',anchor='w')

endpoint_hierarchy.pack(side='left', fill=Y)

def prompt(question):
    win = popupWindow(root, question)
    root.wait_window(win.top)
    return win.value

def update_project_tree():
    print(f"updating project tree, now with {len(project_tree)} root folders")
    endpoint_hierarchy.delete(*endpoint_hierarchy.get_children())
    for project_node in project_tree:
        endpoint_hierarchy.insert('', 'end', f'Item{project_node.id}', text = '     ' + project_node.text, image= icon_folder if project_node.isFolder else icon_get_request)

def command_file_exit():
    root.quit()

def command_project_new_folder():
    folder_name = prompt("Folder name: ")
    new_project_node = ProjectTreeNode(folder_name, isFolder=True)
    project_tree.append(new_project_node)
    update_project_tree()

def command_project_new_endpoint():
    endpoint_name = prompt("Endpoint name: ")
    new_project_node = ProjectTreeNode(endpoint_name, isFolder=False)
    project_tree.append(new_project_node)
    update_project_tree()

# Create the menu bar
menubar = Menu(root)  
file_menu = Menu(menubar, tearoff=0)
project_menu = Menu(menubar, tearoff=0)

file_menu.add_command(label="exit", command=command_file_exit)

project_menu.add_command(label="New Folder", command=command_project_new_folder)
project_menu.add_command(label="New Endpoint", command=command_project_new_endpoint)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Project", menu=project_menu)

root.config(menu=menubar)  

# Start the main window
root.title(windowTitle)
root.geometry("500x500")
root.mainloop()