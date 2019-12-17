from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/xinyufeifei/test_driven_dev_w_python.git"


def deploy():
    site_folder = f"/home/{env.user}/sites/{env.host}"
    source_folder = site_folder + "/source"
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ("database", "static", "virtualenv", "source"):
        run(f"mkdir -p {site_folder}/{subfolder}")


def _get_latest_source(source_folder):
    if exists(source_folder + "/.git"):
        run(f"cd {source_folder} && git fetch")
    else:
        run(f"git clone {REPO_URL} {source_folder}")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"cd {source_folder} && git reset --hard {current_commit}")


def _update_settings(source_folder, site_name):
    setting_path = source_folder + "/superlists/settings.py"
    sed(setting_path, "DEBUG = True", "DEBUG = False")
    sed(setting_path, "ALLOWED_HOST = .+$", f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = source_folder + "/superlists/secret_key.py"
    if not exists(secret_key_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f"SECRET_KEY = '{key}'")
    append(setting_path, "\n from .secret_key import SECRET_KEY")


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + "/../virtualenv"
    if not exists(virtualenv_folder + "/bin/pip"):
        run(f"python3.7 -m venv {virtualenv_folder}")
    run(
        f"source {virtualenv_folder}/bin/activate"
        f"&& pip install poetry"
        f"&& cd {source_folder} && poetry install && deactivate"
    )


def _update_static_files(source_folder):
    run(
        f"cd {source_folder}"
        " && ../virtualenv/bin/python manage.py collectstatic --noinput"
    )


def _update_database(source_folder):
    run(
        f"cd {source_folder}" " && ../virtualenv/bin/python manage.py migrate --noinput"
    )