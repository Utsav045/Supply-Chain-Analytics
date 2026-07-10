@echo off

:: ------------------------------------------------------------
:: One‑time setup script for Git hooks
:: ------------------------------------------------------------

rem Ensure we are running from the repository root
pushd %~dp0

rem 1. Create the .githooks directory if it does not exist
if not exist ".githooks" (
    echo Creating .githooks directory... 
    mkdir .githooks
) else (
    echo .githooks directory already exists.
)

rem 2. Verify that the pre‑commit hook script is present
if not exist ".githooks\pre-commit" (
    echo ERROR: Pre‑commit hook script ".githooks\\pre-commit" not found.
    echo Please place the script in the .githooks folder before running this setup.
    popd
    exit /b 1
) else (
    echo Pre‑commit hook script found.
)

rem 3. Configure Git to use the custom hooks path
git config core.hooksPath .githooks
if errorlevel 1 (
    echo FAILED to set core.hooksPath.
    popd
    exit /b 1
) else (
    echo Git configured to use .githooks as hooks directory.
)

rem 4. Make the pre‑commit script executable (required for *nix‑style shells; harmless on Windows)
rem Git for Windows ships with a Bash environment that respects the executable bit.
rem This command is ignored if the repository is used only from PowerShell/CMD.
git update-index --add --chmod=+x .githooks/pre-commit 2>nul

echo.
echo ------------------------------------------------------------
echo Git hooks have been set up successfully.\r
echo You can now commit; the pre‑commit hook will block commits that fail any check.
echo ------------------------------------------------------------

popd
exit /b 0
