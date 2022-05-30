import os
from distutils.core import setup, Extension
from shutil import copyfile

from Cython.Distutils import build_ext

os.chdir("..")


def clear():
    [os.remove(i.replace(".py", ".c")) for i in src]

    def remove(dir, is_first=True):
        for i in os.listdir(dir):
            file = f"{dir}\\{i}"
            if os.path.isdir(file):
                remove(file, is_first=False)
                os.rmdir(file)
            elif os.path.isfile(file):
                os.remove(file)
        if is_first:
            os.rmdir(dir)

    remove("build")


def finish():
    try:
        os.mkdir("dist")
    except FileExistsError:
        pass
    os.chdir("dist")
    for i in os.listdir(".."):
        if ".pyd" not in i:
            continue
        splinted_filename = i.split(".")
        final_filename = f"{splinted_filename[0]}.{splinted_filename[2]}"
        copyfile(f"..\\{i}", final_filename)


src: list[os.PathLike | str] = [i for i in os.listdir() if ".py" in i and ".pyd" not in i if os.path.isfile(i)]

ext_modules = [Extension(
    i.replace(".py", "") if i != "__init__.py" else "shape", [i]) for i in src
]

setup(
    name="ShapeEngine",
    version="1.0",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext}
)

clear()
finish()
