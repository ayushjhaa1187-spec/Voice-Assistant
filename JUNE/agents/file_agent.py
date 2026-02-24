import os
import shutil

class FileAgent:
    def execute(self, action: str, **kwargs):
        if action == "read":
            return self.read_file(kwargs.get("path"))
        elif action == "write":
            return self.write_file(kwargs.get("path"), kwargs.get("content"))
        elif action == "list":
            return self.list_files(kwargs.get("path", "."))
        elif action == "delete":
            return self.delete_file(kwargs.get("path"))
        return "Unknown action"

    def read_file(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return f"File not found: {path}"
        except Exception as e:
            return f"Error reading file: {e}"

    def write_file(self, path: str, content: str):
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"File written to {path}"
        except Exception as e:
            return f"Error writing file: {e}"

    def list_files(self, path: str):
        try:
            files = []
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    files.append(os.path.join(root, filename))
                if len(files) > 100: # Limit list size for LLM context
                    break
            return "\n".join(files[:100])
        except Exception as e:
            return f"Error listing files: {e}"

    def delete_file(self, path: str):
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return f"Deleted {path}"
        except Exception as e:
            return f"Error deleting file: {e}"
