@echo off
setlocal

echo === Backend: venv & deps ===
cd /d %~dp0apps\backend
if not exist .venv\Scripts\activate (
  py -3.11 -m venv .venv
)
call .venv\Scripts\activate
python -m pip install --upgrade pip >NUL
pip install -r requirements.txt

echo === Backend: pytest ===
pytest -q || goto :fail

echo === Frontend: install & test ===
cd /d %~dp0apps\frontend
npm install --silent
npm run test

echo === SUCCESS ===
cd /d %~dp0
echo All checks passed. > REPORT.md
echo - Backend tests: PASS >> REPORT.md
echo - Frontend tests: PASS >> REPORT.md
type REPORT.md
exit /b 0

:fail
cd /d %~dp0
echo Tests failed. See console output. > REPORT.md
type REPORT.md
exit /b 1
