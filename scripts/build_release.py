#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


APP_NAME = "GiftCardSys"
ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
PYI_CONFIG_DIR = ROOT / ".pyinstaller"


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, cwd=ROOT)


def clean() -> None:
    for path in (DIST_DIR, BUILD_DIR):
        if path.exists():
            shutil.rmtree(path)
    PYI_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def pyinstaller_build() -> None:
    system = platform.system().lower()
    data_sep = ";" if system == "windows" else ":"
    os.environ["PYINSTALLER_CONFIG_DIR"] = str(PYI_CONFIG_DIR)

    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--clean",
        "--windowed",
        "--name",
        APP_NAME,
        "--add-data",
        f"img{data_sep}img",
        "main.py",
    ]
    run(cmd)


def package_output() -> None:
    system = platform.system().lower()
    release_dir = DIST_DIR / "release"
    release_dir.mkdir(parents=True, exist_ok=True)

    if system == "darwin":
        app_bundle = DIST_DIR / f"{APP_NAME}.app"
        if not app_bundle.exists():
            raise RuntimeError(f"앱 번들을 찾을 수 없습니다: {app_bundle}")
        dmg_path = DIST_DIR / f"{APP_NAME}-installer.dmg"
        dmg_staging = DIST_DIR / "dmg"
        if dmg_staging.exists():
            shutil.rmtree(dmg_staging)
        dmg_staging.mkdir(parents=True, exist_ok=True)
        shutil.copytree(app_bundle, dmg_staging / app_bundle.name, dirs_exist_ok=True)
        app_link = dmg_staging / "Applications"
        if app_link.exists() or app_link.is_symlink():
            app_link.unlink()
        app_link.symlink_to("/Applications")

        try:
            run(
                [
                    "hdiutil",
                    "create",
                    "-volname",
                    APP_NAME,
                    "-srcfolder",
                    str(dmg_staging),
                    "-ov",
                    "-format",
                    "UDZO",
                    str(dmg_path),
                ]
            )
            print(f"설치 파일 생성: {dmg_path}")
        except Exception:
            print("DMG 생성에 실패했습니다. .app 번들은 정상 생성되었습니다.")
        return

    if system == "windows":
        target = DIST_DIR / APP_NAME
        if not target.exists():
            raise RuntimeError(f"실행 폴더를 찾을 수 없습니다: {target}")
        archive = release_dir / f"{APP_NAME}-windows"
        shutil.make_archive(str(archive), "zip", root_dir=target.parent, base_dir=target.name)
        print(f"설치용 zip 생성: {archive}.zip")
        return

    # linux
    target = DIST_DIR / APP_NAME
    if not target.exists():
        raise RuntimeError(f"실행 폴더를 찾을 수 없습니다: {target}")
    archive = release_dir / f"{APP_NAME}-linux.tar.gz"
    run(["tar", "-czf", str(archive), "-C", str(target.parent), target.name])
    print(f"배포 파일 생성: {archive}")


def main() -> None:
    clean()
    pyinstaller_build()
    package_output()
    print("완료: dist 폴더를 확인하세요.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"빌드 실패: {exc}")
        sys.exit(1)
