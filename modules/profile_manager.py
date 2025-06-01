import os
import json
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

def get_config_dir():
    """Get the user's config directory for FluxPilot."""
    if os.name == 'nt':
        config_dir = Path(os.getenv('APPDATA')) / 'FluxPilot'
    elif os.name == 'posix':
        if 'darwin' in os.sys.platform:
            config_dir = Path.home() / 'Library' / 'Application Support' / 'FluxPilot'
        else:
            config_dir = Path.home() / '.config' / 'FluxPilot'
    else:
        config_dir = Path.home() / '.fluxpilot'
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

CONFIG_FILE = get_config_dir() / "profiles.json"


def load_profiles():
    """
    Load profiles from CONFIG_FILE (JSON). Returns a list of profile dicts.
    """
    if not os.path.isfile(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"profiles": []}, f, indent=2)
        return []
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    return data.get("profiles", [])


def save_profiles(profiles):
    """
    Save list of profile dicts to CONFIG_FILE.
    """
    with open(CONFIG_FILE, "w") as f:
        json.dump({"profiles": profiles}, f, indent=2)


class ProfileDialog(ctk.CTkToplevel):
    """
    Dialog for adding/editing a profile. Each profile has a name and a list of steps.
    Step: { 'label': str, 'command': str, 'cwd': str or None }
    """
    def __init__(self, master, profile=None, on_save=None):
        super().__init__(master)
        self.title("Add / Edit Profile")
        self.resizable(False, False)
        self.on_save = on_save  # callback with new profile dict

        # If editing an existing profile, clone it; else start blank
        self.original = profile.copy() if profile else {"name": "", "steps": []}

        # Configure grid
        self.grid_columnconfigure(1, weight=1)

        # Profile name
        ctk.CTkLabel(
            self,
            text="Profile Name:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.name_var = ctk.StringVar(value=self.original["name"])
        ctk.CTkEntry(
            self,
            textvariable=self.name_var,
            width=300
        ).grid(row=0, column=1, columnspan=3, padx=10, pady=(10, 0), sticky="ew")

        # Frame for step rows
        self.rows_frame = ctk.CTkScrollableFrame(self, width=600, height=300)
        self.rows_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")
        self.rows_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Headers
        ctk.CTkLabel(
            self.rows_frame,
            text="Label",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(
            self.rows_frame,
            text="Command",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(
            self.rows_frame,
            text="Working Dir",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=2, padx=5, pady=5, sticky="w")

        self.step_vars = []  # list of (labelVar, commandVar, cwdVar, [widgets])

        # Populate existing steps
        for step in self.original.get("steps", []):
            self._add_step_row(step.get("label", ""), step.get("command", ""), step.get("cwd", ""))
        if not self.step_vars:
            self._add_step_row()

        # Buttons to add/remove rows
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(0, 10))
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            btn_frame,
            text="Add Step",
            width=120,
            command=self._add_step_row
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Remove Last Step",
            width=120,
            command=self._remove_last_step
        ).grid(row=0, column=1, padx=5)

        # Save/Cancel
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=3, column=0, columnspan=4, pady=(0, 10))
        action_frame.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(
            action_frame,
            text="Save",
            width=120,
            command=self._on_save
        ).grid(row=0, column=0, padx=5)
        
        ctk.CTkButton(
            action_frame,
            text="Cancel",
            width=120,
            command=self.destroy
        ).grid(row=0, column=1, padx=5)

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _add_step_row(self, label_text="", cmd_text="", cwd_text=""):
        """Add a row of entries for label, command, and cwd."""
        row = len(self.step_vars) + 1
        lbl_var = ctk.StringVar(value=label_text)
        cmd_var = ctk.StringVar(value=cmd_text)
        cwd_var = ctk.StringVar(value=cwd_text)

        e1 = ctk.CTkEntry(self.rows_frame, textvariable=lbl_var, width=150)
        e1.grid(row=row, column=0, padx=5, pady=5, sticky="ew")

        e2 = ctk.CTkEntry(self.rows_frame, textvariable=cmd_var, width=300)
        e2.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        cwd_entry = ctk.CTkEntry(self.rows_frame, textvariable=cwd_var, width=200)
        cwd_entry.grid(row=row, column=2, padx=5, pady=5, sticky="ew")
        
        browse_btn = ctk.CTkButton(
            self.rows_frame,
            text="...",
            width=30,
            command=lambda var=cwd_var: self._browse_dir(var)
        )
        browse_btn.grid(row=row, column=3, padx=5, pady=5)

        self.step_vars.append((lbl_var, cmd_var, cwd_var, [e1, e2, cwd_entry, browse_btn]))

    def _remove_last_step(self):
        """Remove the last added step row."""
        if not self.step_vars:
            return
        lbl_var, cmd_var, cwd_var, widgets = self.step_vars.pop()
        for w in widgets:
            w.destroy()

    def _browse_dir(self, var):
        """Open a directory selection dialog."""
        d = filedialog.askdirectory(title="Select Working Directory")
        if d:
            var.set(d)

    def _on_save(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Profile name cannot be empty.")
            return

        steps = []
        for lbl_var, cmd_var, cwd_var, _ in self.step_vars:
            cmd = cmd_var.get().strip()
            if not cmd:
                continue
            step = {
                "label": lbl_var.get().strip(),
                "command": cmd,
                "cwd": cwd_var.get().strip() or None
            }
            steps.append(step)

        if not steps:
            messagebox.showerror("Error", "You must specify at least one command.")
            return

        new_profile = {"name": name, "steps": steps}
        if self.on_save:
            self.on_save(new_profile)
        self.destroy()