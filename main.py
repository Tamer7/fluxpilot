import customtkinter as ctk
from tkinter import messagebox
from modules.profile_manager import load_profiles, save_profiles, ProfileDialog
from modules.process_runner import ProcessRunner
from modules.ports_checker import gather_port_entries, PortsPopup


class LauncherApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("FluxPilot")
        self.geometry("1000x700")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Load profiles
        self.profiles = load_profiles()

        # Create main container
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === Left frame: Profile list + buttons ===
        left_frame = ctk.CTkFrame(self, width=250)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left_frame.grid_rowconfigure(3, weight=1)  # Make listbox expandable

        # Title
        ctk.CTkLabel(
            left_frame, text="Profiles", font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Profile list
        self.profile_frame = ctk.CTkScrollableFrame(left_frame, width=230, height=300)
        self.profile_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self.profile_buttons = {}  # name -> button
        self._refresh_profile_list()

        # Buttons frame
        btn_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=10, pady=(5, 0), sticky="ew")
        btn_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Add/Edit/Delete buttons
        ctk.CTkButton(btn_frame, text="Add", width=70, command=self._add_profile).grid(
            row=0, column=0, padx=2
        )

        ctk.CTkButton(
            btn_frame, text="Edit", width=70, command=self._edit_profile
        ).grid(row=0, column=1, padx=2)

        ctk.CTkButton(
            btn_frame, text="Delete", width=70, command=self._delete_profile
        ).grid(row=0, column=2, padx=2)

        # Run button
        self.run_button = ctk.CTkButton(
            left_frame,
            text="Run Selected",
            width=230,
            command=self._run_selected_profile,
            state="disabled",
        )
        self.run_button.grid(row=3, column=0, padx=10, pady=(5, 0), sticky="ew")

        # Show Ports button
        ctk.CTkButton(
            left_frame,
            text="Show Ports",
            width=230,
            fg_color=["#3B8ED0", "#1F6AA5"],  # Original blue color
            hover_color=["#2B7FD9", "#1A5F9C"],  # Original hover color
            command=self._show_ports,
        ).grid(row=4, column=0, padx=10, pady=(5, 5), sticky="ew")

        # === Right frame: Notebook for multiple consoles ===
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            right_frame,
            text="Running Profiles",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Notebook frame
        notebook_frame = ctk.CTkFrame(right_frame)
        notebook_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        notebook_frame.grid_columnconfigure(0, weight=1)
        notebook_frame.grid_rowconfigure(0, weight=1)

        # Create notebook
        self.notebook = ctk.CTkTabview(notebook_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        # Placeholder message when no profiles are running
        self.placeholder_frame = ctk.CTkFrame(notebook_frame)
        self.placeholder_frame.grid(row=0, column=0, sticky="nsew")
        self.placeholder_frame.grid_columnconfigure(0, weight=1)
        self.placeholder_frame.grid_rowconfigure(0, weight=1)

        placeholder_content = ctk.CTkFrame(
            self.placeholder_frame, fg_color="transparent"
        )
        placeholder_content.grid(row=0, column=0)

        ctk.CTkLabel(placeholder_content, text="💻", font=ctk.CTkFont(size=48)).grid(
            row=0, column=0, pady=(0, 10)
        )

        ctk.CTkLabel(
            placeholder_content,
            text="No running processes yet",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=1, column=0, pady=(0, 5))

        ctk.CTkLabel(
            placeholder_content,
            text="Select a profile from the left and click 'Run Selected' to start",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        ).grid(row=2, column=0)

        # Track runners and their tabs
        self.runners = {}  # run_id -> ProcessRunner
        self.run_tabs = {}  # run_id -> frame
        self.run_counter = 0
        self.selected_profile = None

        # Initially show placeholder
        self._update_console_view()

    def _refresh_profile_list(self):
        # Clear existing buttons
        for button in self.profile_buttons.values():
            button.destroy()
        self.profile_buttons.clear()

        # Create new buttons
        for i, profile in enumerate(self.profiles):
            btn = ctk.CTkButton(
                self.profile_frame,
                text=profile["name"],
                width=200,
                fg_color=("gray75", "gray30"),  # Default unselected color
                hover_color=("gray65", "gray40"),  # Hover color
                command=lambda p=profile: self._select_profile(p),
            )
            btn.grid(row=i, column=0, padx=5, pady=2, sticky="ew")
            self.profile_buttons[profile["name"]] = btn

    def _select_profile(self, profile):
        # Deselect all buttons
        for btn in self.profile_buttons.values():
            btn.configure(fg_color=("gray75", "gray30"))  # Default unselected color

        # Select the clicked button
        btn = self.profile_buttons[profile["name"]]
        btn.configure(fg_color=("gray65", "gray40"))  # Selected color

        self.selected_profile = profile
        self._update_run_button_state()

    def _add_profile(self):
        def save_callback(new_profile):
            existing = [p["name"] for p in self.profiles]
            if new_profile["name"] in existing:
                idx = existing.index(new_profile["name"])
                if messagebox.askyesno(
                    "Overwrite?",
                    f"A profile named '{new_profile['name']}' already exists. Overwrite?",
                ):
                    self.profiles[idx] = new_profile
                else:
                    return
            else:
                self.profiles.append(new_profile)
            save_profiles(self.profiles)
            self._refresh_profile_list()

        ProfileDialog(self, profile=None, on_save=save_callback)

    def _edit_profile(self):
        if not self.selected_profile:
            messagebox.showinfo("Info", "Please select a profile to edit.")
            return

        def save_callback(edited_profile):
            # Update the profile in the list
            for i, p in enumerate(self.profiles):
                if p["name"] == self.selected_profile["name"]:
                    self.profiles[i] = edited_profile
                    break
            save_profiles(self.profiles)
            self._refresh_profile_list()
            # Reselect the edited profile
            self._select_profile(edited_profile)

        ProfileDialog(self, profile=self.selected_profile, on_save=save_callback)

    def _delete_profile(self):
        if not self.selected_profile:
            messagebox.showinfo("Info", "Please select a profile to delete.")
            return

        profile_name = self.selected_profile["name"]
        if messagebox.askyesno("Confirm Delete", f"Delete profile '{profile_name}'?"):
            self.profiles = [p for p in self.profiles if p["name"] != profile_name]
            save_profiles(self.profiles)
            self._refresh_profile_list()
            self.selected_profile = None
            self._update_run_button_state()

    def _run_selected_profile(self):
        if not self.selected_profile:
            messagebox.showinfo("Info", "Please select a profile to run.")
            return

        profile = self.selected_profile
        profile_name = profile["name"]

        # Check if this profile is already running
        for runner in self.runners.values():
            if runner.profile_name == profile_name and runner.is_running:
                messagebox.showinfo(
                    "Info", f"Profile '{profile_name}' is already running."
                )
                return

        run_id = f"run_{self.run_counter}"
        self.run_counter += 1

        # Create a new tab
        tab = self.notebook.add(f"{profile['name']} ({run_id})")

        # Create console frame
        console_frame = ctk.CTkFrame(tab)
        console_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Create console
        console = ctk.CTkTextbox(
            console_frame, wrap="none", font=ctk.CTkFont(family="Consolas", size=12)
        )
        console.pack(fill="both", expand=True, padx=5, pady=5)

        # Create stop button
        stop_btn = ctk.CTkButton(
            console_frame,
            text="Stop",
            fg_color="#d9534f",
            hover_color="#c9302c",
            command=lambda rid=run_id: self._stop_run(rid),
        )
        stop_btn.pack(side="right", padx=5, pady=5)

        self.run_tabs[run_id] = tab

        # Callbacks for ProcessRunner
        def on_output(line, rid=run_id):
            console.configure(state="normal")
            console.insert("end", line)
            console.see("end")
            console.configure(state="disabled")

        def on_finish(rid=run_id):
            console.configure(state="normal")
            console.insert("end", "\n✅ All steps completed or stopped.\n")
            console.see("end")
            console.configure(state="disabled")
            self._update_run_button_state()

        runner = ProcessRunner(profile["steps"], on_output, on_finish)
        runner.profile_name = profile_name
        self.runners[run_id] = runner

        # Initial banner
        on_output(f"🔹 Running profile: {profile['name']}\n")
        runner.start()
        self._update_run_button_state()
        self._update_console_view()  # Update view to show notebook

        # Switch to the new tab
        self.notebook.set(f"{profile['name']} ({run_id})")

    def _update_run_button_state(self):
        if not self.selected_profile:
            self.run_button.configure(state="disabled")
            return

        # Check if this profile is already running
        is_running = any(
            runner.profile_name == self.selected_profile["name"] and runner.is_running
            for runner in self.runners.values()
        )

        self.run_button.configure(state="disabled" if is_running else "normal")

    def _stop_run(self, run_id):
        runner = self.runners.get(run_id)
        if not runner or not runner.is_running:
            return
        if messagebox.askyesno(
            "Stop", "Are you sure you want to stop this profile run?"
        ):
            runner.stop_all()
            self._update_run_button_state()

    def _close_tab(self, run_id):
        runner = self.runners.get(run_id)
        if runner and runner.is_running:
            if not messagebox.askyesno(
                "Close Tab", "This will stop all running processes. Continue?"
            ):
                return
            runner.stop_all()

        # Remove the tab
        tab = self.run_tabs.get(run_id)
        if tab:
            self.notebook.delete(tab)
            del self.run_tabs[run_id]
            del self.runners[run_id]
            self._update_run_button_state()
            self._update_console_view()  # Update view to show placeholder if no tabs

    def _show_ports(self):
        entries = gather_port_entries()
        PortsPopup(self, entries)

    def _on_close(self):
        # If any runners still active, confirm and stop them
        active = [rid for rid, runner in self.runners.items() if runner.is_running]
        if active:
            if not messagebox.askyesno(
                "Exit", "One or more profiles are still running. Exit anyway?"
            ):
                return
            for rid in active:
                self.runners[rid].stop_all()
        self.destroy()

    def _update_console_view(self):
        """Show placeholder or notebook based on whether there are running processes."""
        if len(self.run_tabs) == 0:
            # Show placeholder
            self.notebook.grid_remove()
            self.placeholder_frame.grid(row=0, column=0, sticky="nsew")
        else:
            # Show notebook
            self.placeholder_frame.grid_remove()
            self.notebook.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    app = LauncherApp()
    app.mainloop()
