import os
import requests  # noqa We are just importing this to prove the dependency installed correctly
import utils


def main():
    my_input = os.environ["INPUT_MYINPUT"]

    env_vars = {key: value for key, value in os.environ.items() if key}

    for key, value in env_vars.items():
        print(f"{key}: {value}")

    my_output = f'Hello {my_input}'

    utils.set_github_action_output('myOutput', my_output)


if __name__ == "__main__":
    main()
