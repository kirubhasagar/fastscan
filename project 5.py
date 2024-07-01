import tkinter as tk
from tkinter import messagebox, filedialog
import socket
import json
import threading
import time

class FastScanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FastScan")

        # Scan history
        self.history = []

        # Control variables for pause and resume
        self.is_paused = False
        self.is_scanning = False
        self.current_scan_thread = None

        # IP Address input
        tk.Label(root, text="IP Address:").grid(row=0, column=0)
        self.ip_entry = tk.Entry(root)
        self.ip_entry.grid(row=0, column=1)

        # Port range input
        tk.Label(root, text="Port Range:").grid(row=1, column=0)
        self.port_entry = tk.Entry(root)
        self.port_entry.grid(row=1, column=1)

        # Scan button
        self.scan_button = tk.Button(root, text="Scan", command=self.run_scan)
        self.scan_button.grid(row=2, column=0, columnspan=2)

        # Pause/Resume button
        self.pause_resume_button = tk.Button(root, text="Pause", command=self.pause_resume_scan, state=tk.DISABLED)
        self.pause_resume_button.grid(row=2, column=2, columnspan=2)

        # Output text box
        self.output_text = tk.Text(root, height=15, width=50)
        self.output_text.grid(row=3, column=0, columnspan=2)

        # History text box
        self.history_text = tk.Text(root, height=15, width=50)
        self.history_text.grid(row=4, column=0, columnspan=2)

        # Buttons for history management
        self.save_button = tk.Button(root, text="Save History", command=self.save_history)
        self.save_button.grid(row=5, column=0)

        self.load_button = tk.Button(root, text="Load History", command=self.load_history)
        self.load_button.grid(row=5, column=1)

        self.clear_button = tk.Button(root, text="Clear History", command=self.clear_history)
        self.clear_button.grid(row=6, column=0, columnspan=2)

    def run_scan(self):
        if self.is_scanning:
            messagebox.showinfo("Scan in Progress", "A scan is already in progress.")
            return

        ip = self.ip_entry.get()
        port_range = self.port_entry.get()

        if not ip or not port_range:
            messagebox.showwarning("Input Error", "Please provide both IP address and port range.")
            return

        # Parse the port range
        try:
            start_port, end_port = map(int, port_range.split('-'))
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid port range. Please enter in the format 'start-end'.")
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Scanning {ip} for open ports from {start_port} to {end_port}...\n")

        # Get host information
        try:
            host_name = socket.gethostbyaddr(ip)[0]
        except socket.herror:
            host_name = "Unknown"

        self.output_text.insert(tk.END, f"Host: {host_name}\n\n")

        self.is_scanning = True
        self.scan_button.config(state=tk.DISABLED)
        self.pause_resume_button.config(state=tk.NORMAL)

        self.current_scan_thread = threading.Thread(target=self.perform_scan, args=(ip, start_port, end_port))
        self.current_scan_thread.start()

    def perform_scan(self, ip, start_port, end_port):
        scan_results = []
        for port in range(start_port, end_port + 1):
            while self.is_paused:
                time.sleep(0.1)
            result = self.scan_port(ip, port)
            service_name = socket.getservbyport(port) if result else "Unknown"
            if result:
                self.output_text.insert(tk.END, f"Port {port} ({service_name}) is open\n")
                scan_results.append((port, service_name, 'open'))
            else:
                self.output_text.insert(tk.END, f"Port {port} ({service_name}) is closed\n")
                scan_results.append((port, service_name, 'closed'))
            self.output_text.update_idletasks()

        self.history.append((ip, start_port, end_port, scan_results))
        self.update_history_text()

        self.is_scanning = False
        self.scan_button.config(state=tk.NORMAL)
        self.pause_resume_button.config(state=tk.DISABLED)

    def pause_resume_scan(self):
        if self.is_scanning:
            if self.is_paused:
                self.is_paused = False
                self.pause_resume_button.config(text="Pause")
            else:
                self.is_paused = True
                self.pause_resume_button.config(text="Resume")

    def scan_port(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0

    def update_history_text(self):
        self.history_text.delete(1.0, tk.END)
        for entry in self.history:
            ip, start_port, end_port, results = entry
            self.history_text.insert(tk.END, f"Scan of {ip} from port {start_port} to {end_port}:\n")
            for port, service_name, status in results:
                self.history_text.insert(tk.END, f"  Port {port} ({service_name}): {status}\n")
            self.history_text.insert(tk.END, "\n")
        self.history_text.update_idletasks()

    def save_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        with open(file_path, 'w') as file:
            json.dump(self.history, file)

    def load_history(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
            return
        with open(file_path, 'r') as file:
            self.history = json.load(file)
        self.update_history_text()

    def clear_history(self):
        self.history = []
        self.update_history_text()

if __name__ == "__main__":
    root = tk.Tk()
    app = FastScanApp(root)
    root.mainloop()
