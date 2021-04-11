from cx_Freeze import setup, Executable

executables = [
    Executable(script="main.py", icon="2048.ico", base="Win32GUI")
]

buildOptions = dict(
    include_files=["2048.ico"]
)

setup(
    version="1.0",
    name="2048",
    description="Jeu de 2048",
    author="Simon ZOU",
    options=dict(build_exe=buildOptions),
    executables=executables
)

