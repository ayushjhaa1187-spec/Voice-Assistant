import subprocess
import platform
import os

class SystemAgent:
    def execute(self, action: str, **kwargs):
        if action == "open_app":
            return self.open_app(kwargs.get("app_name"))
        elif action == "run_command":
            return self.run_command(kwargs.get("command"))
        elif action == "shutdown":
            return self.shutdown()
        elif action == "restart":
            return self.restart()
        return "Unknown action"

    def open_app(self, app_name: str):
        system = platform.system()
        try:
            if system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", app_name])
            elif system == "Windows":
                subprocess.Popen(["start", app_name], shell=True)
            elif system == "Linux":
                subprocess.Popen([app_name]) # Try direct execution
            return f"Opened {app_name}"
        except Exception as e:
            return f"Failed to open {app_name}: {e}"

    def run_command(self, command: str):
        try:
            result = subprocess.check_output(command, shell=True, text=True)
            return f"Command output:\n{result}"
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e.output}"
        except Exception as e:
            return f"Error running command: {e}"

    def shutdown(self):
        system = platform.system()
        if system == "Windows":
            subprocess.call(["shutdown", "/s", "/t", "1"])
        else:
            subprocess.call(["sudo", "shutdown", "-h", "now"])
        return "Shutting down..."

    def restart(self):
        system = platform.system()
        if system == "Windows":
            subprocess.call(["shutdown", "/r", "/t", "1"])
        else:
            subprocess.call(["sudo", "shutdown", "-r", "now"])
        return "Restarting..."
