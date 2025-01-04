import subprocess
import sys
import os
import platform
import shutil

def display_warning():
    print("""
WARNING: System Commands Usage

Please be aware that some commands in this shell emulator can affect your system in significant ways, including:

- **shutdown**: This command will shut down your computer immediately. Use with caution!
- **del [filename]**: This command permanently deletes the specified file. It is not recoverable.
- **rmdir [name]**: This command will remove an empty directory. If the directory is not empty, this command will fail.
- **cp [source] [destination]**: Incorrect usage or copying over important files may lead to data loss.
- **mv [source] [destination]**: Moving files inappropriately may lead to unintended file loss.

Make sure you understand the implications of these commands before using them. Always double-check your commands, especially when dealing with file deletions or system shutdowns.
""")

def display_help():
    print("""
Welcome to Windows Shell Emulator!

Available commands:
- help: Display this help message.
- clear: Clear the terminal.
- exit: Exit the shell.
- run [command]: Run a specified command in the system.
- pwd: Print current working directory.
- ls: List files and directories in the current directory.
- cd [path]: Change directory to [path].
- echo [text]: Print [text] to the terminal.
- getinfo: Get system information.
- ping [host]: Ping a specified host.
- tasks: List current running tasks.
- kill [pid]: Kill a process by its Process ID (PID).
- mkdir [name]: Create a new directory with the specified name.
- rmdir [name]: Remove a directory with the specified name.
- touch [filename]: Create a new empty file.
- cp [source] [destination]: Copy a file from source to destination.
- mv [source] [destination]: Move (rename) a file from source to destination.
- del [filename]: Delete a specified file.
- whoami: Display the current user name.
- ipconfig: Show current network configuration.
- shutdown: Shutdown the computer.
""")

def clear_terminal():
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
    except Exception as e:
        print("An error occurred:", str(e))

def print_working_directory():
    print(os.getcwd())

def change_directory(path):
    try:
        os.chdir(path)
        print(f"Changed directory to {os.getcwd()}")
    except FileNotFoundError:
        print(f"Directory not found: {path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def echo_text(text):
    print(text)

def get_system_info():
    run_command("systeminfo")

def ping_host(host):
    run_command(f"ping {host}")

def list_tasks():
    run_command("tasklist")

def kill_process(pid):
    try:
        subprocess.run(f"taskkill /PID {pid} /F", shell=True)
        print(f"Killed process with PID: {pid}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_directory(name):
    try:
        os.makedirs(name, exist_ok=True)
        print(f"Created directory: {name}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def remove_directory(name):
    try:
        os.rmdir(name)
        print(f"Removed directory: {name}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_file(filename):
    try:
        with open(filename, 'w') as f:
            pass  # Create an empty file
        print(f"Created file: {filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def copy_file(source, destination):
    try:
        shutil.copy2(source, destination)
        print(f"Copied {source} to {destination}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def move_file(source, destination):
    try:
        shutil.move(source, destination)
        print(f"Moved {source} to {destination}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"Deleted file: {filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def show_current_user():
    print("Current user:", os.getlogin())

def show_ipconfig():
    run_command("ipconfig")

def shutdown_computer():
    run_command("shutdown /s /t 1")

def main():
    clear_terminal()
    display_warning()
    display_help()

    while True:
        command_input = input("CROSH> ").strip().lower()

        if command_input == "help":
            display_help()
        elif command_input == "clear":
            clear_terminal()
        elif command_input == "exit":
            print("Exiting the shell. Goodbye!")
            break
        elif command_input == "pwd":
            print_working_directory()
        elif command_input.startswith("ls"):
            run_command("dir")
        elif command_input.startswith("cd "):
            path = command_input[3:].strip()
            change_directory(path)
        elif command_input.startswith("echo "):
            text = command_input[5:]  
            echo_text(text)
        elif command_input == "getinfo":
            get_system_info()
        elif command_input.startswith("ping "):
            host = command_input[5:].strip()
            if host:
                ping_host(host)
            else:
                print("Please specify a host to ping.")
        elif command_input == "tasks":
            list_tasks()
        elif command_input.startswith("kill "):
            pid = command_input[5:].strip()
            if pid.isdigit():
                kill_process(pid)
            else:
                print("Please provide a valid PID.")
        elif command_input.startswith("mkdir "):
            name = command_input[6:].strip()
            create_directory(name)
        elif command_input.startswith("rmdir "):
            name = command_input[6:].strip()
            remove_directory(name)
        elif command_input.startswith("touch "):
            filename = command_input[6:].strip()
            create_file(filename)
        elif command_input.startswith("cp "):
            args = command_input[3:].strip().split()
            if len(args) == 2:
                copy_file(args[0], args[1])
            else:
                print("Usage: cp [source] [destination]")
        elif command_input.startswith("mv "):
            args = command_input[3:].strip().split()
            if len(args) == 2:
                move_file(args[0], args[1])
            else:
                print("Usage: mv [source] [destination]")
        elif command_input.startswith("del "):
            filename = command_input[4:].strip()
            delete_file(filename)
        elif command_input == "whoami":
            show_current_user()
        elif command_input == "ipconfig":
            show_ipconfig()
        elif command_input == "shutdown":
            shutdown_computer()
        elif command_input.startswith("run "):
            cmd = command_input[4:]
            if cmd:
                run_command(cmd)
            else:
                print("No command provided to run.")
        else:
            print(f"Unknown command: {command_input}. Type 'help' for a list of commands.")

if __name__ == "__main__":
    main()