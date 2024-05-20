import ftplib
import subprocess

# List of IP addresses
ip_addresses = [
    "192.168.1.1",
    "192.168.1.2",
    # Add more IP addresses as needed
]

# FTP credentials
ftp_username = "your_username"
ftp_password = "your_password"
remote_file_path = "/path/to/remote/file.txt"
local_file_path = "local_file.txt"

# Function to connect to an FTP server and download a file
def download_file(ip, remote_path, local_path):
    try:
        ftp = ftplib.FTP(ip)
        ftp.login(ftp_username, ftp_password)
        with open(local_path, 'wb') as local_file:
            ftp.retrbinary('RETR ' + remote_path, local_file.write)
        ftp.quit()
        print(f"Downloaded file from {ip} successfully.")
        return True
    except ftplib.all_errors as e:
        print(f"Failed to download file from {ip}: {e}")
        return False

# Function to search for the answer in the downloaded file
def search_for_answer(file_path, search_term):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if search_term in line:
                    print(f"Found answer: {line.strip()}")
                    return line.strip()
        print(f"Answer not found in {file_path}.")
        return None
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None

# Function to submit the answer using a command
def submit_answer(answer):
    try:
        result = subprocess.run(['echo', answer], capture_output=True, text=True)
        print(f"Command output: {result.stdout}")
    except Exception as e:
        print(f"Failed to submit answer: {e}")

# Main script logic
search_term = "desired_search_term"

for ip in ip_addresses:
    if download_file(ip, remote_file_path, local_file_path):
        answer = search_for_answer(local_file_path, search_term)
        if answer:
            submit_answer(answer)
