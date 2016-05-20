import os
try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice here too
from tkinter import filedialog	
#import tkFileDialog as filedialog
import subprocess
from subprocess import call
#importing swiftclient to create a connection to interact with the server
import swiftclient
#to pretty print arbitrary data structures
import pprint

#setup connection to interact with the server
def setup_connection():
    try:
        conn = swiftclient.Connection(
                user='admin',
                key='admin',
                authurl='http://52.36.194.192/auth/v1.0',
                )		
    except Exception as e:
        print (e)
        print ("Authorization error.")
    return conn

def upload(root):
    upload = Toplevel(root)
    upload.title("Upload pictures to your swiftstack node")
    upload.transient(root)
    upload.resizable(FALSE, FALSE)
    upload.geometry("400x300")
    container_name = StringVar();
    file_name = StringVar();
    Label(upload, text="Enter container name").grid(row=0, sticky=W)
    Entry(upload, textvariable=container_name).grid(row=0, column=1, sticky=W)
    a = Button(upload, text="Upload", command= lambda: upload_file(upload, container_name.get()))
    a.grid(row=3, column=1, sticky=W)
    print ("Upload")

def upload_file(upload, container_name):
    print (container_name)
    input_file_name = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    print (input_file_name)
    Label(upload, text="Filename").grid(row=4, sticky=W)
    file_name = Entry(upload, text=input_file_name)
    file_name.grid(row=4, column=1, sticky=W)
    file_name.insert(END, input_file_name)
    b = Button(upload, text="Push", command =lambda: push_to_cluster(upload, container_name, input_file_name))
    b.grid(row=5, column=1, sticky=W)
    print ("Upload file")

def push_to_cluster(upload, container_name, file_name):
    result = ''
    conn = setup_connection()
    try:
        with open(file_name, 'r') as f:
            result = conn.put_object(container_name, file_name, contents=f.read(), content_type='text/plain')
            if (result != None):
                result = "File succesfully uploaded"
    except Exception as e:
        result = e
    create_gui(upload, result)

def list_containers(root):
    list_containers_layout = Toplevel(root)
    list_containers_layout.title("List all containers for an account")
    list_containers_layout.transient(root)
    list_containers_layout.resizable(FALSE, FALSE)
    list_containers_layout.geometry("400x300")
    a = Button(list_containers_layout, text="List all containers", command= lambda: list_all_containers(list_containers_layout))
    a.grid(row=1, column=1, sticky=W)
    print ("List Containers")

def list_all_containers(root):
    result = ''
    conn = setup_connection()
    try:
        for container in conn.get_account()[1]:
            result = result +  container['name'] + "\n"
    except Exception as e:
        print (e)
        result = e
    print (result)
    create_gui(root, result)

def list_content_in_container(root):
    content_container = Toplevel(root)
    content_container.title("List contents in a container")
    content_container.transient(root)
    content_container.resizable(FALSE, FALSE)
    content_container.geometry("800x300")
    container_name = StringVar();
    Label(content_container, text="Enter container name").grid(row=0, sticky=W)
    Entry(content_container, textvariable=container_name).grid(row=0, column=1, sticky=W)
    a = Button(content_container, text="Get contents", command=lambda: get_contents(content_container, container_name.get()))
    a.grid(row=1, column=1, sticky=W)
    print ("List contents in a container")

def get_contents(root, container_name):
    result = ''
    conn = setup_connection()
    try:
        if (len(conn.get_container(container_name)[1]) == 0):
            result = "No contents found for container " + container_name + "."
            print (result)
            create_gui(root, result)
        for data in conn.get_container(container_name)[1]:
            print ('{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified']))
            result = result + '{0}\t{1}\t{2}'.format(data['name'], data['bytes'], data['last_modified']) + "\n"

    except Exception as e:
        print (e)
        result = "Error getting contents of containers."
    print (result)
    create_gui(root, result)

def create_container(root):
    container_block = Toplevel(root)
    container_block.title("Enter name of container")
    container_block.transient(root)
    container_block.resizable(FALSE, FALSE)
    container_block.config(height=500)
    container_block.geometry("500x300")
    container_name = StringVar()
    Label(container_block, text="Enter name of container").grid(row=0, column=1, sticky=W)
    Entry(container_block, textvariable=container_name).grid(row=1, column=1, sticky=E)
    b = Button(container_block, text="Submit", command=lambda: make_container(container_block, container_name.get()))
    b.grid(row=2, column=1, sticky=E)

def make_container(root, name):
    conn = setup_connection()
    print (conn)
    print (dir(conn))
    try:
        if (name == ''):
            result = "Name cannot be empty"
            create_gui(root, result)
            return
        result = conn.put_container(name)
        print (result)
        if (result == None):
            result = "Container '" + name + "' created."
    except:
        print ("There was an error processing your request")
        result = "There was an error processing your request"
    create_gui(root, result)

def delete_container(root):
    container_block = Toplevel(root)
    container_block.title("Delete container")
    container_block.transient(root)
    container_block.resizable(FALSE, FALSE)
    container_block.config(height=500)
    container_block.geometry("500x300")
    container_name = StringVar()
    Label(container_block, text="Enter name of container").grid(row=0, column=1, sticky=W)
    Entry(container_block, textvariable=container_name).grid(row=1, column=1, sticky=E)
    b = Button(container_block, text="Submit", command=lambda: del_container(container_block, container_name.get()))
    b.grid(row=2, column=1, sticky=E)

def del_container(root, name):
    conn = setup_connection()
    print (conn)
    print (dir(conn))
    try:
        if (name == ''):
            result = "Name cannot be empty"
            create_gui(root, result)
            return
        result = conn.delete_container(name)
        print (result)
        if (result == None):
            result = "Container '" + name + "' deleted."
    except:
        print ("There was an error processing your request")
        result = "There was an error processing your request"
    create_gui(root, result)

def retrieve_object(root):
    get_object_block = Toplevel(root)
    get_object_block.title("Retrive an Obejct")
    get_object_block.transient(root)
    get_object_block.resizable(FALSE, FALSE)
    get_object_block.config(height=500)
    get_object_block.geometry("500x300")
    container_name = StringVar()
    file_name = StringVar()
    Label(get_object_block, text="Enter name of container").grid(row=0, column=1, sticky=W)
    Entry(get_object_block, textvariable=container_name).grid(row=1, column=1, sticky=E)
    Label(get_object_block, text="Enter name of object/file:").grid(row=2, column=1, sticky=W)
    Entry(get_object_block, textvariable=file_name).grid(row=4, column=1, sticky=E)
    b = Button(get_object_block, text="Submit", command=lambda: get_object(get_object_block, container_name.get(), file_name.get()))
    b.grid(row=5, column=1, sticky=E)

def get_object(root, container_name, file_name):
    conn = setup_connection();
    try:
        obj = conn.get_object(container_name, file_name)
        with open(file_name, 'w') as file:
            file.write(obj[1])
            result = "File successfully downloaded at " + os.getcwd()
    except Exception as e:
        result = e
        print ("There was an error downloading the file.")
    create_gui(root, result)

def delete_object(root):
    del_object_block = Toplevel(root)
    del_object_block.title("Retrive an Obejct")
    del_object_block.transient(root)
    del_object_block.resizable(FALSE, FALSE)
    del_object_block.config(height=500)
    del_object_block.geometry("500x300")
    container_name = StringVar()
    file_name = StringVar()
    Label(del_object_block, text="Enter name of container").grid(row=0, column=1, sticky=W)
    Entry(del_object_block, textvariable=container_name).grid(row=1, column=1, sticky=E)
    Label(del_object_block, text="Enter name of object/file:").grid(row=2, column=1, sticky=W)
    Entry(del_object_block, textvariable=file_name).grid(row=4, column=1, sticky=E)
    b = Button(del_object_block, text="Submit", command=lambda: del_object(del_object_block, container_name.get(), file_name.get()))
    b.grid(row=5, column=1, sticky=E)

def del_object(root, container_name, file_name):
    conn = setup_connection()
    if (len(container_name) == 0):
        create_gui(root, "Container name cannot be empty")
        return
    if (len(file_name) == 0):
        create_gui(root, "File name cannot be empty")
        return
    try:
        result = conn.delete_object(container_name, file_name)
        if (result == None):
            result = "Deleted object " + file_name + "."
    except Exception as e:
        result = e
        print ("There was an error deleting the object")
    print (result)
    create_gui(root, result)

def create_gui(root, result=None):
    Label(root, text='Result :').grid(row="99", column="1", sticky=W)
    console_frame = Frame(root)
    console_frame.grid(row="100", column="1", columnspan="2")    
    console_text = Text(console_frame, fg="green", bg="black")
    console_text.insert(INSERT, result)
    console_text.pack(expand=1, fill=BOTH)
    scrollbar = Scrollbar(console_frame, command=console_text.yview)
    scrollbar.pack(side="right", fill=Y)
    console_text['yscrollcommand'] = scrollbar.set

def main():
    root = Tk()
    Label(root, text="What action do you want to perform").grid(row=0, sticky=W)
    a = Button(root, text="List Containers", command=lambda: list_containers(root))
    b = Button(root, text="List contents in a container", command=lambda: list_content_in_container(root))
    c = Button(root, text="Create a container", command=lambda: create_container(root))
    d = Button(root, text="Delete container", command=lambda: delete_container(root))
    e = Button(root, text="Push an object", command=lambda: upload(root))
    f = Button(root, text="Retrieve an Object", command=lambda: retrieve_object(root))
    g = Button(root, text="Delete an Object", command=lambda:  delete_object(root))
    a.grid(row=1, column=1, sticky=W)
    b.grid(row=2, column=1, sticky=W)
    c.grid(row=3, column=1, sticky=W)
    d.grid(row=4, column=1, sticky=W)
    e.grid(row=5, column=1, sticky=W)
    f.grid(row=6, column=1, sticky=W)
    g.grid(row=7, column=1, sticky=W)
    root.mainloop()

if __name__ == "__main__":
    main()
   