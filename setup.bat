@echo off
echo ===============================
echo   TRADESAGE - Setup Inicial
echo ===============================

:: Crear entorno virtual
echo [1/4] Creando entorno virtual...
python -m venv venv

:: Activar entorno virtual
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate

:: Instalar dependencias
echo [3/4] Instalando paquetes requeridos...
pip install --upgrade pip
pip install dash dash-bootstrap-components yfinance pandas plotly

:: Crear requirements.txt
echo [4/4] Guardando dependencias...
pip freeze > requirements.txt

echo.
echo ✅ Setup completado correctamente.
echo Para iniciar, ejecuta:
echo.
echo     venv\Scripts\activate
echo     python src\app.py
echo.
pause
