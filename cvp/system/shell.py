# -*- coding: utf-8 -*-

import os
import platform
import shutil


def get_default_shell_path() -> str:
    system = platform.system()
    if system == "Windows":
        if comspec_path := os.environ.get("COMSPEC"):
            return comspec_path

        if powershell_path := shutil.which("powershell.exe"):
            return powershell_path

        if pwsh_path := shutil.which("pwsh.exe"):
            return pwsh_path

        if cmd_path := shutil.which("cmd.exe"):
            return cmd_path

        return r"C:\Windows\System32\cmd.exe"
    elif system in ("Linux", "Darwin"):
        try:
            from pwd import getpwuid

            return getpwuid(os.getuid()).pw_shell
        except:  # noqa
            if shell_path := os.environ.get("SHELL"):
                return shell_path

            if system == "Darwin":
                if zsh_path := shutil.which("zsh"):
                    return zsh_path

            if sh_path := shutil.which("bash"):
                return sh_path

            if sh_path := shutil.which("sh"):
                return sh_path

            return "/bin/sh"
    else:
        raise NotImplementedError(f"Unsupported platform: '{system}'")
