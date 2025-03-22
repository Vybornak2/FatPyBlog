# PowerShell script for common Django commands

param (
    [Parameter(Mandatory=$true)]
    [string]$Command
)

$projectRoot = Split-Path -Parent $PSScriptRoot

switch ($Command) {
    "makemigrations" {
        Write-Host "Making migrations..." -ForegroundColor Green
        python $projectRoot\manage.py makemigrations
    }
    "migrate" {
        Write-Host "Applying migrations..." -ForegroundColor Green
        python $projectRoot\manage.py migrate
    }
    "runserver" {
        Write-Host "Starting development server..." -ForegroundColor Green
        python $projectRoot\manage.py runserver
    }
    "shell" {
        Write-Host "Starting Django shell..." -ForegroundColor Green
        python $projectRoot\manage.py shell
    }
    "createsuperuser" {
        Write-Host "Creating superuser..." -ForegroundColor Green
        python $projectRoot\manage.py createsuperuser
    }
    "collectstatic" {
        Write-Host "Collecting static files..." -ForegroundColor Green
        python $projectRoot\manage.py collectstatic
    }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Available commands: makemigrations, migrate, runserver, shell, createsuperuser, collectstatic" -ForegroundColor Yellow
    }
}
