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
        print(f"Checking for {name}")

        check_repo_url = requests.get(repo)
        if check_repo_url.status_code == 404:
            s["check_status"] = "REPO NOT FOUND"
            continue

        cmd = s['check_command']
        command = f"./script.sh \"{name}\" \"{repo}\" \"{cmd}\""

        if 'no_uv' in s:
            command += " no_uv"

        try:
            result = subprocess.run(command, shell=True, timeout=120)
        except subprocess.TimeoutExpired as e:
            s["check_status"] = "TIMEOUT"
        else:
            s["check_status"] = "OK"

        print(s["check_status"])
        print()


    print()
    print("Summary")
    for source in config["sources"]:
        print(source["name"])
        print(source["check_status"])
        print()
