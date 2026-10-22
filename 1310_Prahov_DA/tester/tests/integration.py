import requests
import tempfile
from log_filter import log_filter

class IntegrationTests:
    def __init__(self):
        self.host = 'app'
        self.port = '5000'
        self.base_url = f"http://{self.host}:{self.port}"
        
        self.test_number_value = 27
        self.extension_allowed = ".txt"
        self.extension_forbidden = ".env"
        self.filename = "file"
        self.file_content = "Nothing!"
        self.isSuccessful = True

    def test_get_index(self):
        try:
            response = requests.get(f"{self.base_url}/")
            if response.ok:
                log_filter.info(f"GET / - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"GET / - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"GET / - Error: {str(e)}")
            self.isSuccessful = False

    def test_get_upload(self):
        try:
            response = requests.get(f"{self.base_url}/upload")
            if response.ok:
                log_filter.info(f"GET /upload - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"GET /upload - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"GET /upload - Error: {str(e)}")
            self.isSuccessful = False
    
    def test_post_upload_forbidden(self):
        try:
            with tempfile.NamedTemporaryFile(suffix=self.extension_forbidden) as tmp_file:
                tmp_file.write(self.file_content.encode('utf-8'))
                tmp_file.seek(0)
                files = {'file': (self.filename + self.extension_forbidden, tmp_file)}
                response = requests.post(
                    f"{self.base_url}/upload",
                    files=files
                )
                if response.ok:
                    log_filter.info(f"POST /upload (forbidden) - Expected success (Status: {response.status_code})")
                else:
                    log_filter.error(f"POST /upload (forbidden) - Failed (Status: {response.status_code})")
                    self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"POST /upload (forbidden) - Error: {str(e)}")
            self.isSuccessful = False

    def test_post_upload_allowed(self):
        try:
            with tempfile.NamedTemporaryFile(suffix=self.extension_allowed) as tmp_file:
                tmp_file.write(self.file_content.encode('utf-8'))
                tmp_file.seek(0)
                files = {'file': (self.filename + self.extension_allowed, tmp_file)}
                response = requests.post(
                    f"{self.base_url}/upload",
                    files=files
                )
                if response.ok:
                    log_filter.info(f"POST /upload (allowed) - Success (Status: {response.status_code})")
                else:
                    log_filter.error(f"POST /upload (allowed) - Failed (Status: {response.status_code})")
                    self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"POST /upload (allowed) - Error: {str(e)}")
            self.isSuccessful = False

    def test_get_download(self):
        try:
            response = requests.get(f"{self.base_url}/download/{self.filename + self.extension_allowed}")
            if response.ok:
                log_filter.info(f"GET /download - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"GET /download - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"GET /download - Error: {str(e)}")
            self.isSuccessful = False

    def test_get_files(self):
        try:
            response = requests.get(f"{self.base_url}/files")
            if response.ok:
                log_filter.info(f"GET /files - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"GET /files - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"GET /files - Error: {str(e)}")
            self.isSuccessful = False

    def test_get_to_files(self):
        try:
            response = requests.get(f"{self.base_url}/to_files")
            if response.ok:
                log_filter.info(f"GET /to_files - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"GET /to_files - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"GET /to_files - Error: {str(e)}")
            self.isSuccessful = False

    def test_get_increment(self):
        try:
            response = requests.get(f"{self.base_url}/increment/{self.test_number_value}")
            if response.ok:
                log_filter.info(f"GET /increment - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"GET /increment - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"GET /increment - Error: {str(e)}")
            self.isSuccessful = False

    def test_get_check_even(self):
        try:
            response = requests.get(f"{self.base_url}/check_even/{self.test_number_value}")
            if response.ok:
                log_filter.info(f"GET /check_even - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"GET /check_even - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"GET /check_even - Error: {str(e)}")
            self.isSuccessful = False

    def test_post_login_valid(self):
        try:
            response = requests.post(f"{self.base_url}/login",
                                   data={'name': 'admin', 'password': 'password'})
            if response.ok:
                log_filter.info(f"POST /login (valid data) - Success (Status: {response.status_code})")
            else:
                log_filter.error(f"POST /login (valid data) - Failed (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"POST /login | (valid data) - Error: {str(e)}")
            self.isSuccessful = False

    def test_post_login_invalid(self):
        try:
            response = requests.post(f"{self.base_url}/login",
                                   data={'name': 'admin', 'password': 'wrong'})
            if response.status_code == 401:
                log_filter.info(f"POST /login (invalid data) - Expected failure (Status: {response.status_code})")
            else:
                log_filter.error(f"POST /login (invalid data) - Unexpected response (Status: {response.status_code})")
                self.isSuccessful = False
        except Exception as e:
            log_filter.error(f"POST /login (invalid data) - Error: {str(e)}")
            self.isSuccessful = False

    def run_all_tests(self):
        log_filter.info("Starting integration tests")
        self.test_get_index()
        self.test_get_upload()
        self.test_post_upload_forbidden()
        self.test_post_upload_allowed()
        self.test_get_download()
        self.test_get_files()
        self.test_get_increment()
        self.test_get_check_even()
        self.test_get_to_files()
        self.test_post_login_valid()
        self.test_post_login_invalid()
        
        if not self.isSuccessful:
            log_filter.error("Some integration tests failed")
        else:
            log_filter.info("All integration tests completed successfully")
            
        [handler.flush() for handler in log_filter.handlers]