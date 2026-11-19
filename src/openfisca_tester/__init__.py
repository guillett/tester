import requests
import subprocess
import yaml


def main() -> None:
    with open('config.yaml') as file:
        config = yaml.safe_load(file)

    statuses = []
    for s in config["sources"]:
        name = s['name']
        repo = s['repository']

        check_repo_url = requests.get(repo)
        if check_repo_url.status_code == 404:
            s["check_status"] = "REPO NOT FOUND"
            continue

        cmd = s['check_command']
        #cmd = "echo test"
        command = f"./script.sh \"{name}\" \"{repo}\" \"{cmd}\""

        if 'no_uv' in s:
            command += " no_uv"

        result = subprocess.run(command, shell=True, timeout=120)
        s["check_status"] = "OK"

    for source in config["sources"]:
        print(source["name"])
        print(source["check_status"])
        print()
