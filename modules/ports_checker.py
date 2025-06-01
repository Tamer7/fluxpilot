import subprocess
import platform
import os
import signal
import customtkinter as ctk
from tkinter import ttk, messagebox

def gather_port_entries():
    """
    Returns a list of dicts for listening ports:
      { 'pid': str, 'proto': str, 'local_address': str,
        'foreign_address': str, 'state': str, 'program': str }
    """
    entries = []
    system = platform.system()
    try:
        if system == "Windows":
            cmd = ["netstat", "-ano"]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = proc.communicate(timeout=5)
            if proc.returncode != 0:
                return entries

            lines = out.splitlines()
            # Find header row beginning with "Proto"
            start_idx = 0
            for i, line in enumerate(lines):
                if line.strip().startswith("Proto"):
                    start_idx = i + 1
                    break

            for line in lines[start_idx:]:
                parts = line.split()
                if len(parts) < 5:
                    continue
                proto = parts[0]
                local = parts[1]
                foreign = parts[2]
                state = parts[3] if proto.upper().startswith("TCP") else ""
                pid = parts[-1]
                # Only list TCP entries in LISTENING state
                if proto.upper().startswith("TCP") and state.upper() != "LISTENING":
                    continue
                entries.append({
                    "pid": pid,
                    "proto": proto,
                    "local_address": local,
                    "foreign_address": foreign,
                    "state": state,
                    "program": ""
                })

        elif system in ("Linux", "Darwin"):
            # Try `netstat -tunlp`
            cmd = ["netstat", "-tunlp"]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            out, err = proc.communicate(timeout=5)
            if proc.returncode == 0:
                lines = out.splitlines()
                # Find header row beginning with "Proto"
                start_idx = 0
                for i, line in enumerate(lines):
                    if line.strip().startswith("Proto"):
                        start_idx = i + 1
                        break

                for line in lines[start_idx:]:
                    parts = line.split()
                    if len(parts) < 7:
                        continue
                    proto = parts[0]
                    local = parts[3]
                    foreign = parts[4]
                    state = parts[5]
                    prog = parts[6]   # format = "pid/program"
                    pid = prog.split("/")[0] if "/" in prog else prog
                    if state.upper() not in ("LISTEN", "LISTENING"):
                        continue
                    entries.append({
                        "pid": pid,
                        "proto": proto,
                        "local_address": local,
                        "foreign_address": foreign,
                        "state": state,
                        "program": prog
                    })
            else:
                # Fallback to `lsof -i -P -n | grep LISTEN`
                cmd = ["lsof", "-i", "-P", "-n"]
                proc2 = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                out2, err2 = proc2.communicate(timeout=5)
                if proc2.returncode == 0:
                    for line in out2.splitlines():
                        if "LISTEN" not in line:
                            continue
                        parts = line.split()
                        if len(parts) < 9:
                            continue
                        pid = parts[1]
                        proto = parts[7]
                        local = parts[8] if "(LISTEN)" in parts else ""
                        state = "LISTEN"
                        prog = parts[0]
                        entries.append({
                            "pid": pid,
                            "proto": proto,
                            "local_address": local,
                            "foreign_address": "",
                            "state": state,
                            "program": prog
                        })
    except Exception:
        pass

    return entries


class PortsPopup(ctk.CTkToplevel):
    """
    Pop-up window showing listening ports/PIDs with ability to kill processes.
    """
    def __init__(self, master, port_entries):
        super().__init__(master)
        self.title("Open / Listening Ports")
        self.geometry("750x450")
        self.resizable(True, True)
        self.port_entries = port_entries

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Title
        ctk.CTkLabel(
            self,
            text="Listening Ports and PIDs:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, sticky="nw", padx=10, pady=(10, 5))

        # Main frame for treeview
        frame = ctk.CTkFrame(self)
        frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        # Create treeview with modern style
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme as base for better customization
        style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            fieldbackground="#2b2b2b",
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#1a1a1a",
            foreground="#ffffff",
            relief="flat",
            borderwidth=1,
            font=("Segoe UI", 9, "bold")
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#2a2a2a")],
            foreground=[("active", "#ffffff")]
        )
        style.map(
            "Treeview",
            background=[("selected", "#3b3b3b")],
            foreground=[("selected", "white")]
        )

        columns = ("pid", "proto", "local_address", "foreign_address", "state", "program")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="extended", style="Treeview")
        for col, width, heading in zip(
            columns,
            [60, 60, 180, 180, 100, 140],
            ["PID", "Proto", "Local Address", "Foreign Address", "State", "Program"]
        ):
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, anchor="center" if col in ("pid", "proto", "state") else "w")

        # Scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # Populate rows
        self._load_entries(port_entries)

        # Button frame
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, pady=10)
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Buttons
        ctk.CTkButton(
            btn_frame,
            text="Kill Selected",
            width=120,
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=self._kill_selected
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Refresh",
            width=120,
            command=self._on_refresh
        ).grid(row=0, column=1, padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Close",
            width=120,
            command=self.destroy
        ).grid(row=0, column=2, padx=5)

    def _load_entries(self, entries):
        """Clear and insert entries into the tree."""
        self.tree.delete(*self.tree.get_children())
        for entry in entries:
            pid = entry.get("pid", "")
            proto = entry.get("proto", "")
            local = entry.get("local_address", "")
            foreign = entry.get("foreign_address", "")
            state = entry.get("state", "")
            prog = entry.get("program", "")
            self.tree.insert("", "end", values=(pid, proto, local, foreign, state, prog))

    def _on_refresh(self):
        """Refresh entries by re-gathering. Assumes master has a gather_port_entries method."""
        new_entries = self.master._gather_port_entries()
        self._load_entries(new_entries)

    def _kill_selected(self):
        """Kill the selected PIDs."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Info", "Please select one or more rows to kill.")
            return
        if not messagebox.askyesno("Confirm Kill", "Kill all selected processes?"):
            return
        system = platform.system()
        for item in selected:
            vals = self.tree.item(item, "values")
            pid = vals[0]
            if not pid.isdigit():
                continue
            try:
                if system == "Windows":
                    subprocess.run(
                        ["taskkill", "/PID", pid, "/T", "/F"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                else:
                    os.killpg(os.getpgid(int(pid)), signal.SIGKILL)
            except Exception as e:
                messagebox.showwarning("Warning", f"Failed to kill PID {pid}: {e}")
        # Refresh after kill
        self._on_refresh()
