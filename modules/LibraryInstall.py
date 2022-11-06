import subprocess
import sys

def install(package: str) -> None:
    """
        function that installs modules
        with ImportError exception
    """

    print (f'{package} no encontrada! Instalando\n')
    subprocess.check_call(
        [ sys.executable, "-m", "pip", "install", package ]
    )