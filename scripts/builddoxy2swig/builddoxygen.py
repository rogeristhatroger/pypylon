import os
import shutil
import subprocess
import sys
import warnings
from pathlib import Path


def ensure_environment() -> Path:
    print("Checking PYLON_DEV_DIR...")
    pylon_dev_dir = os.environ.get("PYLON_DEV_DIR")
    if not pylon_dev_dir:
        raise EnvironmentError("PYLON_DEV_DIR is not set")

    pylon_include_dir = Path(pylon_dev_dir) / "include"
    if not pylon_include_dir.is_dir():
        raise EnvironmentError(f"Expected include directory not found: {pylon_include_dir}")
    return pylon_include_dir


def check_doxygen() -> str:
    print("Checking Doxygen...")
    doxygen_path = shutil.which("doxygen")
    if not doxygen_path:
        raise EnvironmentError("Doxygen executable not found in PATH")

    version = subprocess.check_output([doxygen_path, "--version"], text=True).strip()
    print(f"Version: {version}")
    if version != "1.5.9":
        warnings.warn(
            "Only tested with Doxygen 1.5.9; other versions may produce different output.",
            stacklevel=2,
        )
    return doxygen_path


def run_doxygen(
    doxygen_path: str,
    doxyfile: Path,
    script_dir: Path,
    include_dir: Path,
) -> Path:
    xml_dir = script_dir / "xml"
    shutil.rmtree(xml_dir, ignore_errors=True)

    config = doxyfile.read_text(encoding="utf-8")
    overrides = (
        f'\nINPUT = "{include_dir}"\n'
        f'OUTPUT_DIRECTORY = "{script_dir}"\n'
    )
    subprocess.run(
        [doxygen_path, "-"],
        input=config + overrides,
        text=True,
        check=True,
    )

    index_xml = xml_dir / "index.xml"
    if not index_xml.is_file():
        raise RuntimeError(f"Doxygen did not generate expected file: {index_xml}")
    return index_xml


def run_doxy2swig(doxy2swig_script: Path, index_xml: Path, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(doxy2swig_script), str(index_xml), str(output_file)],
        check=True,
    )


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent

    doxyfile = script_dir / "Doxyfile"
    doxy2swig_script = script_dir / "doxy2swig" / "doxy2swig.py"

    pylon_include_dir = ensure_environment()
    doxygen_path = check_doxygen()

    jobs = [
        ("GenApi", repo_root / "src" / "genicam" / "DoxyGenApi.i"),
        ("pylon", repo_root / "src" / "pylon" / "DoxyPylon.i"),
        (
            "pylondataprocessing",
            repo_root / "src" / "pylondataprocessing" / "DoxyPylonDataProcessing.i",
        ),
    ]

    for include_subdir, output_file in jobs:
        include_dir = pylon_include_dir / include_subdir
        if not include_dir.is_dir():
            raise FileNotFoundError(f"Include path does not exist: {include_dir}")

        print(f"Generating {output_file.name} from {include_dir}...")
        index_xml = run_doxygen(doxygen_path, doxyfile, script_dir, include_dir)
        run_doxy2swig(doxy2swig_script, index_xml, output_file)

    shutil.rmtree(script_dir / "xml", ignore_errors=True)

    print(
        "Successfully generated src/pylon/DoxyPylon.i, src/genicam/DoxyGenApi.i and "
        "src/pylondataprocessing/DoxyPylonDataProcessing.i"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
