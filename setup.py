from pathlib import Path

# Available at setup time due to pyproject.toml
from setuptools import setup, Extension

_DIR = Path(__file__).parent
_SPEEX_DIR = _DIR / "speex"

version = "2.0.1"

flags = ["-DFLOATING_POINT", "-DUSE_KISS_FFT"]
sources = list(_SPEEX_DIR.glob("*.cc"))

ext_modules = [
    Extension(
        name="speex_noise_cpp",
        language="c++",
        py_limited_api=True,
        extra_compile_args=flags,
        sources=sorted(
            [str(p) for p in sources] + [str(_DIR / "src" / "speex_noise.cpp")]
        ),
        define_macros=[
            ("Py_LIMITED_API", "0x03090000"),
            ("VERSION_INFO", f'"{version}"'),
        ],
        include_dirs=[str(_SPEEX_DIR)],
    ),
]

setup(
    version=version,
    ext_modules=ext_modules,
    extras_require={
        "dev": [
            "black",
            "flake8",
            "isort",
            "mypy",
            "pylint",
            "pytest",
            "build",
        ]
    },
)
