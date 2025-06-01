import subprocess
import threading
import os
import signal
import platform
import time

class ProcessRunner:
    """
    Manages running a list of steps (shell commands + working directories) in parallel,
    streaming output to a callback, and stopping all processes including child processes.
    """

    def __init__(self, steps, on_output, on_finish=None):
        """
        steps: a list of dicts, each { 'label': str, 'command': str, 'cwd': str or None }
        on_output: function(line: str) called for each stdout/stderr line
        on_finish: optional function() called when all steps finish (or are stopped)
        """
        self.steps = steps
        self.on_output = on_output
        self.on_finish = on_finish
        self.processes = []    # list of subprocess.Popen objects
        self.threads = []      # list of threads streaming each process’s stdout
        self.is_running = False
        self.current_step = 0
        self.total_steps = len(steps)

    def start(self):
        """Begin execution in a background thread."""
        if self.is_running:
            return
        self.is_running = True
        threading.Thread(target=self._run_all_steps, daemon=True).start()

    def _run_all_steps(self):
        """Internal: launch all steps in parallel, streaming output."""
        for i, step in enumerate(self.steps):
            if not self.is_running:
                break

            self.current_step = i + 1
            label = step.get("label") or step.get("command")

            # Print a header for this step
            self.on_output(f"\n{'='*80}\n")
            self.on_output(f"Step {self.current_step}/{self.total_steps}: {label}\n")
            self.on_output(f"{'='*80}\n\n")

            cmd = step.get("command")
            cwd = step.get("cwd") or None

            try:
                system = platform.system()
                if system == "Windows":
                    # CREATE_NEW_PROCESS_GROUP → child processes form a new process group
                    p = subprocess.Popen(
                        cmd,
                        shell=True,
                        cwd=cwd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                    )
                else:
                    # On Unix, preexec_fn=os.setsid → new session/process group
                    p = subprocess.Popen(
                        cmd,
                        shell=True,
                        cwd=cwd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        preexec_fn=os.setsid
                    )
                self.processes.append(p)

                # Start a thread to stream this process’s output
                t = threading.Thread(target=self._stream_output, args=(p,), daemon=True)
                t.start()
                self.threads.append(t)

                # (Optional) small delay so logs don’t interleave exactly at once
                time.sleep(0.1)

            except Exception as e:
                self.on_output(f"\n‼ Error launching step {self.current_step} '{cmd}': {e}\n")
                if self.is_running:
                    self.on_output("🛑 Stopping execution due to error.\n")
                    self.is_running = False
                break

        # Now that all steps are launched, wait until they all exit (or until stopped)
        while self.is_running and any(p.poll() is None for p in self.processes):
            time.sleep(0.1)

        # Print a final summary
        if self.is_running:
            self.on_output(f"\n{'='*80}\n")
            self.on_output("✅ All steps completed successfully\n")
        else:
            self.on_output(f"\n{'='*80}\n")
            self.on_output("🛑 Execution stopped\n")
        self.on_output(f"{'='*80}\n")

        # Mark finished
        self.is_running = False
        if self.on_finish:
            self.on_finish()

    def _stream_output(self, process):
        """
        Continuously read from process.stdout and forward to on_output.
        This runs in its own thread for each process.
        """
        for line in process.stdout:
            if not self.is_running:
                break
            # You could prefix each line with step index if desired; for now, just emit as-is
            self.on_output(line)

    def stop_all(self):
        """Terminate all running processes (including child processes)."""
        if not self.is_running:
            return
        self.is_running = False
        system = platform.system()
        for p in self.processes:
            try:
                pid = p.pid
                if pid is None:
                    continue
                if system == "Windows":
                    # /T kills entire tree, /F forces termination
                    subprocess.run(
                        ["taskkill", "/PID", str(pid), "/T", "/F"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                else:
                    # Kill the entire process group
                    os.killpg(os.getpgid(pid), signal.SIGTERM)
            except Exception:
                pass
        self.processes.clear()
