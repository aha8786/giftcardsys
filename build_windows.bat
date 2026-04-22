@echo off
chcp 65001 > nul
echo [기프트카드 관리 시스템] Windows EXE 빌드 시작

:: 가상환경 활성화 (있으면)
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: 의존성 설치
echo 패키지 설치 중...
pip install -r requirements.txt pyinstaller

:: 빌드 실행
echo 빌드 중...
python scripts/build_release.py

if %ERRORLEVEL% == 0 (
    echo.
    echo 빌드 성공!
    echo 실행 파일 위치: dist\GiftCardSys\GiftCardSys.exe
    echo 배포용 ZIP:    dist\release\GiftCardSys-windows.zip
) else (
    echo.
    echo 빌드 실패. 위 오류 메시지를 확인하세요.
)

pause
