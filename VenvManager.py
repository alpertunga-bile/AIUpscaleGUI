from subprocess import run
from platform import system
from sys import stdout
from os import remove, mkdir, getcwd
from re import compile
from os.path import join, exists
from logging import getLogger, Logger, StreamHandler, Formatter, INFO
from json import load, dumps

# For coloring log outputs
class CustomFormatter(Formatter):
    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        from logging import DEBUG, WARNING, ERROR, CRITICAL
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            DEBUG: self.grey + self.fmt + self.reset,
            INFO: self.blue + self.fmt + self.reset,
            WARNING: self.yellow + self.fmt + self.reset,
            ERROR: self.red + self.fmt + self.reset,
            CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        logFormat = self.FORMATS.get(record.levelno)
        formatter = Formatter(logFormat)
        return formatter.format(record)

class VenvManager:
    opsys : str = ""
    venvName : str = ""
    currentDir : str = ""
    paths : dict = {}
    logger : Logger

    def __init__(self, envName : str ="venv", loggerLevel=INFO):
        self.venvName = envName
        self.opsys = system()
        self.paths = {}
        self.currentDir = getcwd()
        self.SetLogger(loggerLevel)
        self.SetPaths(envName)
        self.SavePaths()

        self.logger.debug(self.paths)

        file = open("venvLog.txt", "w")
        file.close()
        self.logger.info("VenvLog file is created")

        # Check python and its version
        self.CheckPython()

        if exists(envName):
            self.logger.info(f"Using {envName} virtual environment")
        else:
            self.logger.info(f"Creating {envName}")
            self.CheckCommand(self.RunCommand("python -m venv venv"), f"{envName} is created", "Cant create virtual environment")

    """
    Class functionalities
    """

    def SetLogger(self, loggerLevel) -> None:
        self.logger = getLogger()
        self.logger.setLevel(loggerLevel)
        handler = StreamHandler(stdout)
        handler.setLevel(INFO)
        logFormat = '[%(asctime)s] /_\ %(levelname)-8s /_\ %(message)s'
        if self.opsys == "Windows":
            formatter = Formatter(logFormat)
        else:
            formatter = CustomFormatter(logFormat)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def IsEnvironmentExists(self) -> bool:
        return exists(self.venvName)

    def CheckPython(self) -> None:
        streamdata, isExist = self.RunCommand("python --version")

        if isExist:
            self.logger.info(f"Using {streamdata}")
        else:
            self.logger.error("Python is not exists")
            exit(1)

    def SetPaths(self, envName : str) -> None:
        if exists("paths.json"):
            with open('paths.json', "r") as pathFile:
                self.paths = load(pathFile)
        else:
            winPath = f"{envName}\\Scripts"

            if self.opsys == "Windows":
                self.paths["python"] = f"{winPath}\\python.exe"
                self.paths["pip"] = f"{winPath}\\pip.exe"
                self.paths["activate"] = f"{winPath}\\activate.bat"
                self.paths["deactivate"] = f"{winPath}\\deactivate.bat"
            elif self.opsys == "Linux":
                self.paths["activate"] = f"source {envName}/bin/activate"
                self.paths["python"] = f"{self.paths['activate']} && python3"
                self.paths["pip"] = f"{self.paths['activate']} && pip3"
                self.paths["deactivate"] = ""

    def SavePaths(self) -> None:
        with open("paths.json", "w") as file:
            jsonObject = dumps(self.paths, indent=1)
            file.write(jsonObject)

    """
    Installation Functions
    """

    def CreateRequirementsFile(self) -> None:
        command = f"{self.paths['pip']} freeze > requirements.txt"
        self.CheckCommand(self.RunCommand(command), "requirements file is updated", "Cant create requirements file")

    def CheckPackages(self, filename : str) -> tuple:
        self.logger.info("Checking Packages")
        command = f"{self.paths['pip']} freeze > temp_requirements.txt"
        self.RunCommand(command)

        envPackages = []
        with open("temp_requirements.txt", "r") as envFile:
            envPackages = set(envFile.readlines())

        remove("temp_requirements.txt")

        wantedPackages = []
        with open(filename, "r") as wantedFile:
            wantedPackages = set(wantedFile.readlines())

        notIncludedPackages = wantedPackages - envPackages

        return (notIncludedPackages, wantedPackages.issubset(envPackages))

    def InstallWRequirements(self, filename : str="requirements.txt") -> None:
        needToDownload, isContains = self.CheckPackages(filename)
        if isContains:
            self.logger.info("Requirements are already installed")
            return

        for package in needToDownload:
            package = package.strip()
            command = f"{self.paths['pip']} install {package}"
            self.logger.info(f"Installing {package}")
            self.RunCommand(command)

        self.CreateRequirementsFile()

    """
    Git Functions
    """
    def CheckGit(self) -> bool:
        streamdata, isExist = self.RunCommand("git --version")
        
        if isExist:
            self.logger.info(f"Using {streamdata}")
        else:
            self.logger.error("Cant found git")

        return isExist

    def GetRepositoryName(self, repoLink : str) -> str:
        regexPattern = "([^/]+)\\.git$"
        pattern = compile(regexPattern)
        matcher = pattern.search(repoLink)
        return matcher.group(1)

    def CloneRepository(self, repoLink : str, repoKey : str, parentFolder : str="") -> None:
        if self.CheckGit() is False:
            self.logger.error("Cannot detect git")
            return

        repoName = self.GetRepositoryName(repoLink)
        realRepoKey = repoKey + "-repo"

        if realRepoKey in self.paths.keys():
            self.logger.info(f"{repoName} is exists")
            return

        self.paths[realRepoKey] = join(parentFolder, repoName)
        self.SavePaths()

        if exists(join(self.currentDir, parentFolder)) is False:
            mkdir(join(self.currentDir, parentFolder))

        if parentFolder == "":
            command = f"git clone --recursive {repoLink}"
        else:
            command = f"cd {parentFolder} && git clone --recursive {repoLink} && cd {self.currentDir}"
        
        self.logger.info(f"Cloning {repoLink}")
        self.RunCommand(command)

    def UpdateRepository(self, repoKey : str) -> None:
        if self.CheckGit() is False:
            self.logger.error("Cannot detect git")
            return

        realRepoKey = repoKey + "-repo"

        if realRepoKey not in self.paths.keys():
            self.logger.info(f"{repoKey} is not exists")
            return

        command = f"cd {self.paths[realRepoKey]} && git pull && cd {self.currentDir}"
        
        self.logger.info(f"Updating {repoKey}")
        self.RunCommand(command)

    def UpdateAllRepositories(self) -> None:
        if self.CheckGit() is False:
            self.logger.error("Cannot detect git")
            return

        for key in self.paths.keys():
            if "-repo" not in key:
                continue
            
            self.UpdateRepository(key[:-5])

    def RunScriptInsideRepository(self, repoKey : str, repoCommand : str) -> None:
        realRepoKey = repoKey + "-repo"

        if realRepoKey not in self.paths.keys():
            self.logger.info(f"{repoKey} is not exists")
            return

        command = ""
        if self.opsys == "Windows":
            command = f"cd {self.paths[realRepoKey]} && {join(self.currentDir, self.paths['python'])} {repoCommand} && cd {self.currentDir}"
        elif self.opsys == "Linux":
            command = f"{self.paths['activate']} && cd {self.paths[realRepoKey]} && python3 {repoCommand} && cd {self.currentDir}"

        self.logger.info(f"Running {repoCommand}")
        self.RunCommand(command)

    def InstallRequirementsFromRepository(self, repoKey : str, file : str = "requirements.txt") -> None:
        realRepoKey = repoKey + "-repo"

        if realRepoKey not in self.paths.keys():
            self.logger.info(f"{repoKey} is not exists")
            return

        self.InstallWRequirements(join(self.paths[realRepoKey], file))

    def InstallRequirementsFromAllRepositories(self) -> None:
        if self.CheckGit() is False:
            self.logger.error("Cannot detect git")
            return

        for key in self.paths.keys():
            if "-repo" not in key:
                continue
            
            self.InstallRequirementsFromRepository(key[:-5])

    """
    Running Functions
    """

    def CheckCommand(self, terminalData : tuple, successMsg : str, failureMsg : str) -> None:
        _, isSuccess = terminalData

        if isSuccess:
            self.logger.info(successMsg)
        else:
            self.logger.error(failureMsg)
            self.logger.error("ERROR OCCURED!!! Check venvLog file")
            exit(1)

    def RunScript(self, filename : str, args : str="") -> None:
        self.logger.info(f"Running {filename}.py with [{', '.join(args.split(' '))}] args")
        command = f"{self.paths['python']} {filename}.py {args}"

        process = run(command, shell=True, check=True)

        if process.returncode == 0:
            self.logger.info(f"{filename}.py run successfully")
        else:
            self.logger.error(f"Cant run {filename}.py file")

    def RunCommand(self, command : str, isCheck : bool = True) -> tuple:
        process = run(command, shell=True, check=isCheck, capture_output=True)
        
        streamdata = process.stdout
        streamdata = streamdata.decode('UTF-8')
        streamdata = streamdata.strip()

        with open("venvLog.txt", "a") as file:
            if streamdata != "":
                file.write(f"{'-'*200}\n")
                file.write(f"Command : {command}\n")
                file.write(f"Output  :\n{streamdata}\n")

        return (streamdata, True) if process.returncode == 0 else (streamdata, False)