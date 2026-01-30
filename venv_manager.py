import logging
import platform
import os
import sys
import subprocess
import os.path
import json


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        from logging import INFO, DEBUG, WARNING, ERROR, CRITICAL

        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            DEBUG: self.grey + self.fmt + self.reset,
            INFO: self.blue + self.fmt + self.reset,
            WARNING: self.yellow + self.fmt + self.reset,
            ERROR: self.red + self.fmt + self.reset,
            CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record):
        log_format = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


class VenvManager:
    os_name: str = ""
    venv_foldername = ""
    log_filename = ""
    curr_work_dir = ""
    paths = {}
    paths_filename = ""
    logger: logging.Logger

    def __init__(
        self, env_foldername: str = "venv", logger_level: int = logging.INFO
    ) -> None:
        self.venv_foldername = env_foldername
        self.os_name = platform.system()
        self.paths = {}
        self.curr_work_dir = os.getcwd()
        self.log_filename = "venv_log.txt"
        self.paths_filename = "paths.json"

        self.set_logger(logger_level)
        self.set_paths()
        self.save_paths()

        self.logger.debug(self.paths)

        file = open(self.log_filename, "w")
        file.close()

        self.logger.info(f"{self.log_filename} is created")

        self.check_python()

        if os.path.exists(self.venv_foldername):
            self.logger.info(f"Using {self.venv_foldername} virtual environment folder")
        else:
            self.logger.info(f"Creating {self.venv_foldername} folder")
            self.check_command(
                self.run_command("python -m venv venv"),
                f"{self.venv_foldername} is created",
                "Cannot create the virtual environment folder",
            )

    def set_logger(self, logger_level: int) -> None:
        self.logger = logging.getLogger()
        self.logger.setLevel(logger_level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logger_level)

        log_format = "[%(asctime)s] /_\\ %(levelname)-8s /_\\ %(message)s"

        if self.os_name == "Windows":
            formatter = logging.Formatter(log_format)
        else:
            formatter = CustomFormatter(log_format)

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def check_python(self) -> None:
        streamdata, does_exist = self.run_command("python --version")

        if does_exist:
            self.logger.info(f"Using {streamdata}")
        else:
            self.logger.error("Python does not exist")
            exit(1)

    def set_paths(self) -> None:
        if os.path.exists(self.paths_filename):
            with open(self.paths_filename, "r") as path_file:
                self.paths = json.load(path_file)

            if "os_name" in self.paths:
                if self.paths["os_name"] == self.os_name:
                    return

        win_path = os.path.join(self.curr_work_dir, self.venv_foldername, "Scripts")

        self.paths["os_name"] = self.os_name

        if self.os_name == "Windows":
            self.paths["python"] = f"{win_path}\\python.exe"
            self.paths["pip"] = f"{win_path}\\pip.exe"
            self.paths["activate"] = f"{win_path}\\activate.bat"
            self.paths["deactivate"] = f"{win_path}\\deactivate.bat"
        else:
            self.paths["activate"] = (
                f"source {os.path.join(self.curr_work_dir, self.venv_foldername)}/bin/activate"
            )
            self.paths["python"] = f"{self.paths['activate']} && python3"
            self.paths["pip"] = f"{self.paths['activate']} && pip3"
            self.paths["deactivate"] = ""

    def save_paths(self) -> None:
        with open(self.paths_filename, "w") as file:
            json_obj = json.dumps(self.paths, indent=1)
            file.write(json_obj)

    def create_req_file(self) -> None:
        command = f"{self.paths['pip']} freeze > requirements.txt"
        self.check_command(
            self.run_command(command),
            "Requirements file is updated",
            "Cannot create the requirements file",
        )

    def check_packages(self, filename: str) -> tuple[set[str], bool]:
        temp_req_filename = "temp_requirements.txt"

        self.logger.info("Checking Packages")
        command = f"{self.paths['pip']} freeze > {temp_req_filename}"
        self.run_command(command)

        env_packages = set()
        with open(temp_req_filename, "r") as file:
            env_packages = set(file.readlines())

        os.remove(temp_req_filename)

        wanted_packages = set()
        with open(filename, "r") as file:
            wanted_packages = set(file.readlines())

        return (wanted_packages - env_packages, wanted_packages.issubset(env_packages))

    def install_w_requirements(self, filename: str = "requirements.txt") -> None:
        to_download, does_contain = self.check_packages(filename)

        if does_contain:
            self.logger.info("Requirements are already installed")
            return

        for package in to_download:
            package = package.strip()
            command = f"{self.paths['pip']} install {package}"

            self.logger.info(f"Installing {package}")
            self.run_command(command)

        self.create_req_file()

    """
    Running Functions
    """

    def check_command(
        self, terminal_data: tuple[str, bool], success_msg: str, failure_msg: str
    ) -> None:
        _, is_success = terminal_data

        if is_success:
            self.logger.info(success_msg)
        else:
            self.logger.error(failure_msg)
            self.logger.error(f"ERROR OCCURED!!! Check {self.log_filename} file")
            exit(1)

    def run_script(self, filename: str, args: str = "") -> None:
        self.logger.info(
            f"Running {filename}.py with [{', '.join(args.split(' '))}] args"
        )
        command = f"{self.paths['python']} {filename}.py {args}"
        process = subprocess.run(command, shell=True, check=True)

        if process.returncode == 0:
            self.logger.info(f"{filename}.py run successfully")
        else:
            self.logger.error(f"Cant run {filename}.py file")

    def run_command(self, command: str, do_check: bool = True) -> tuple[str, bool]:
        process = subprocess.run(
            command, shell=True, check=do_check, capture_output=True
        )

        streamdata = process.stdout
        streamdata = streamdata.decode("UTF-8")
        streamdata = streamdata.strip()

        with open(self.log_filename, "a") as file:
            if streamdata != "":
                file.write(f"{'-' * 200}\n")
                file.write(f"Command : {command}\n")
                file.write(f"Output  :\n{streamdata}\n")

        return (streamdata, process.returncode == 0)
