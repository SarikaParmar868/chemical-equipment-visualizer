import requests

BASE_URL = "http://localhost:8000/api/"

class APIClient:
    def __init__(self):
        self.token = None
        self.refresh_token = None

    def login(self, username, password):
        try:
            response = requests.post(f"{BASE_URL}login/", data={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                self.token = data['access']
                self.refresh_token = data['refresh']
                return True, "Login Successful"
            else:
                return False, "Invalid Credentials"
        except requests.exceptions.ConnectionError:
            return False, "Connection refused. Is backend running?"

    def get_headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def upload_file(self, file_path):
        """
        Uploads CSV file to backend.
        Returns: (success: bool, data: dict/str)
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                # Ensure we have headers
                headers = self.get_headers()
                if not headers:
                     return False, "Authentication missing. Please login."
                
                response = requests.post(f"{BASE_URL}upload/", files=files, headers=headers)
                
            if response.status_code == 201:
                return True, response.json()
            elif response.status_code == 401:
                return False, "Session expired. Please re-login."
            else:
                try:
                    err_msg = response.json().get('error', response.text)
                except:
                    err_msg = response.text
                return False, f"Server Error: {err_msg}"
        except Exception as e:
            return False, f"Connection Error: {str(e)}"

    def get_summary(self):
        try:
            response = requests.get(f"{BASE_URL}summary/", headers=self.get_headers())
            if response.status_code == 200:
                return True, response.json()
            return False, None
        except:
             return False, None

    def get_history(self):
        try:
            response = requests.get(f"{BASE_URL}history/", headers=self.get_headers())
            if response.status_code == 200:
                return True, response.json()
            return False, []
        except:
            return False, []

    def download_report(self, save_path):
        try:
            response = requests.get(f"{BASE_URL}report/", headers=self.get_headers())
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return True, "Downloaded successfully"
            return False, "Failed to download"
        except Exception as e:
            return False, str(e)
