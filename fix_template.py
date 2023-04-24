#!/usr/bin/env python
"""Replace NAME and EMAIL with values from git configuration."""

import os
import subprocess


def get_git_config():
    """Retrieve user.name and user.email from Git configuration."""
    try:
        name_output = subprocess.check_output(
            ['git', 'config', '--global', '--get', 'user.name'])
        user_name = name_output.decode('utf-8').strip()
        email_output = subprocess.check_output(
            ['git', 'config', '--global', '--get', 'user.email'])
        user_email = email_output.decode('utf-8').strip()

        return user_name, user_email
    except subprocess.CalledProcessError:
        print("Failed to retrieve Git configuration. "
              "Make sure Git is installed and configured.")
        return None, None


def replace_tokens(name, email):
    """Replace tokens with given values in all files in current directory."""
    files = os.listdir('.')
    for file in files:
        if file == os.path.basename(__file__):  # Skip this file
            continue
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as file_handler:
                content = file_handler.read()
                content = content.replace('${NAME}',
                                          name).replace('${EMAIL}', email)
            with open(file, 'w', encoding='utf-8') as file_handler:
                file_handler.write(content)


def main():
    """Replace NAME and EMAIL with values from git configuration."""
    user_name, user_email = get_git_config()
    if user_name and user_email:
        replace_tokens(user_name, user_email)


if __name__ == '__main__':
    main()
