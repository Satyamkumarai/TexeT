@echo off
if  not exist ./env/ (goto create_env) else (
    goto intermediate
)

:create_env
    echo ---------- creating Environment..----------
    python -m venv env
    echo ---------- Done..----------
:activate_env
    echo ---------- Activating env ----------
    call ./env/Scripts/activate.bat
    echo ---------- Done..----------
    echo ---------- Updating pip ----------
    python -m pip install --upgrade pip
    echo ---------- Done..----------
    echo ---------- Installing dependencies..----------
    pip install -r ./requirements.txt
    echo ---------- Done..----------
    echo ---------- Updating Repo..----------
    git pull
    echo ---------- Done..----------
    goto final
    exit /b 0
:intermediate
    goto activate_env
:final 
    echo run `.\env\Scripts\activate` to activate the env

    
    