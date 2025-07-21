import tkinter as tk
import subprocess
import sys
import os
import signal

# Center the window on the screen
def center_window(win, width=320, height=140):
    win.update_idletasks()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# Free port 8765 before starting server
def free_port_8765():
    port = "8765"
    if os.name == 'nt':
        result = subprocess.run(f'netstat -ano | findstr :{port}', shell=True, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 5:
                pid = parts[-1]
                try:
                    subprocess.run(f'taskkill /PID {pid} /F', shell=True)
                except Exception:
                    pass
    else:
        result = subprocess.run(f'lsof -ti tcp:{port}', shell=True, capture_output=True, text=True)
        for pid in result.stdout.split():
            try:
                os.kill(int(pid), signal.SIGKILL)
            except Exception:
                pass

class ServerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Codeforces Automation Server")
        center_window(master)
        master.resizable(False, False)
        font_main = ("Segoe UI", 12)
        font_status = ("Segoe UI", 11, "bold")
        pad = {'padx': 10, 'pady': 5}

        self.status_label = tk.Label(master, text="Status: Stopped", fg="#d9534f", font=font_status)
        self.status_label.pack(**pad)

        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=5)
        self.start_button = tk.Button(btn_frame, text="Start Server", command=self.start_server, width=13, font=font_main, bg="#5cb85c", fg="white", activebackground="#4cae4c")
        self.start_button.grid(row=0, column=0, padx=5)
        self.stop_button = tk.Button(btn_frame, text="Stop Server", command=self.stop_server, state=tk.DISABLED, width=13, font=font_main, bg="#d9534f", fg="white", activebackground="#c9302c")
        self.stop_button.grid(row=0, column=1, padx=5)

        self.exit_button = tk.Button(master, text="Exit", command=self.on_exit, width=30, font=font_main, bg="#0275d8", fg="white", activebackground="#025aa5")
        self.exit_button.pack(pady=(5, 10))

        self.server_process = None
        master.protocol("WM_DELETE_WINDOW", self.on_exit)

    def start_server(self):
        if not self.server_process:
            free_port_8765()
            if os.name == 'nt':
                self.server_process = subprocess.Popen([sys.executable, 'cf_receiver.py'], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
            else:
                self.server_process = subprocess.Popen([sys.executable, 'cf_receiver.py'], preexec_fn=os.setsid)
            self.status_label.config(text="Status: Running", fg="#5cb85c")
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_server(self):
        if self.server_process:
            if os.name == 'nt':
                self.server_process.terminate()
            else:
                os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)
            self.server_process = None
            self.status_label.config(text="Status: Stopped", fg="#d9534f")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def on_exit(self):
        if self.server_process:
            self.stop_server()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerGUI(root)
    root.mainloop() 