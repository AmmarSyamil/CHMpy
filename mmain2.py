import subprocess

result = subprocess.run(
    ["powershell", "-Command", "tree"],
    capture_output=True, text=True
)

print("Command output:")
print(result.stdout)
