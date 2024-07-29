from pathlib import Path

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup

_DIR = Path(__file__).parent
_SPEEX_DIR = _DIR / "speex"

__version__ = "1.0.0"

flags = ["-DFLOATING_POINT", "-DUSE_KISS_FFT"]
sources = list(_SPEEX_DIR.glob("*.c"))


ext_modules = [
    Pybind11Extension(
        name="speex_noise_cpp",
        language="c++",
        sources=[str(p) for p in sources] + [str(_DIR / "python.cpp")],
        extra_compile_args=flags,
        define_macros=[("VERSION_INFO", __version__)],
        include_dirs=[str(_SPEEX_DIR)],
    ),
]


setup(
    name="pyspeex_noise",
    version=__version__,
    author="Michael Hansen",
    author_email="mike@rhasspy.org",
    url="https://github.com/rhasspy/speex-noise",
    description="Noise suppression and automatic gain with speex",
    long_description="",
    packages=["pyspeex_noise"],
    ext_modules=ext_modules,
    zip_safe=False,
    python_requires=">=3.7",
    classifiers=["License :: OSI Approved :: MIT License"],
)
