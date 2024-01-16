import sys,os,socket
import subprocess
from venv import EnvBuilder
from pathlib import Path

ipaddress  = socket.gethostbyname(socket.gethostname())
port = 3003

curr_dir = os.getcwd()

def run_server(daphne_path):
    python_path = curr_dir+"\\venv\\Scripts\\python.exe"
    print("URI  "+ipaddress+":"+port )
    print("Here is server URI to connect the machine with server.")
    subprocess.run([python_path,daphne_path, '-b',ipaddress,'-p',str(port),"CIO_MACHINE_SERVER.asgi:application"], check=True)    

class CustomEnvBuilder(EnvBuilder):
    """
    Subclass of venv.EnvBuilder to customize the virtual environment creation process.
    """

    def create(self, env_dir):
        """
        Override the create method to install additional packages after the default virtual environment is created.
        """
        super().create(env_dir)

        # Additional packages to install in the virtual environment
        requirement_file = curr_dir + "\\requirements.txt"
        pip_path = curr_dir+"\\venv\\Scripts\\pip.exe"
        # Install additional packages using pip
        subprocess.run([pip_path, 'install',"-r",requirement_file], check=True)
        daphne_path = curr_dir+"\\venv\\Scripts\\daphne.exe"
        run_server(daphne_path)

if __name__ == "__main__":
    # Specify the virtual environment directory
    venv_dir = curr_dir + "\\venv"
    venv_path = Path(sys.prefix) / venv_dir
    
    # Check if the virtual environment already exists
    if not (venv_path).is_dir():
        print("instlling depencdencies...")
        # Use CustomEnvBuilder to customize the virtual environment creation process
        builder = CustomEnvBuilder(with_pip=True)
        builder.create(venv_dir)
        print("installed.")
    else:
        print("Virtual environment already exists.")
        daphne_path = curr_dir+"\\venv\\Scripts\\daphne.exe"
        run_server(daphne_path)