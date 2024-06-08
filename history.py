import os


class LocalVisitedOffers:
    def __init__(self):
        self.file_name = "visited.txt"
        self.init_visited()

    def init_visited(self):
        if not os.path.exists(f"{self.file_name}"):
            with open(f"{self.file_name}", "w") as f:
                f.write("")

    def add_url_to_file(self, url: str):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, self.file_name)
        with open(config_path, "a") as file:
            file.write(url + "\n")

    def check_if_url_exist(self, url: str) -> bool:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, self.file_name)
        with open(config_path, "r") as file:
            for line in file:
                if url in line:
                    return True
        return False
