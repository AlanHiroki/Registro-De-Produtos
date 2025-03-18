from cx_Freeze import setup, Executable

# Definindo o executável e utilizando a base correta "Win32GUI"
executables = [
    Executable("main.py", base="Win32GUI")
]

# Configuração do setup
setup(
    name="RegistroDeProdutos",
    version="1.0",
    description="Um programa para registrar produtos em um banco de dados local",
    executables=executables
)