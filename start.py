import venv_manager


if __name__ == "__main__":
    venv_manager = venv_manager.VenvManager()

    venv_manager.install_w_requirements()

    venv_manager.run_script("main")
