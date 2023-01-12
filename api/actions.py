import os
import shutil


def collect_client(y=False):
    import api.client as client

    if not y:
        y = (
            input("This will overwrite existing files, continue? (Y/N): ").lower()
            == "y"
        )
    if y:
        client_src_path = f"{client.__path__[0]}/public_html/"
        # client_dest_path = './public_html/'
        shutil.copytree(client_src_path, "./public_html/", dirs_exist_ok=True)
        print('CreatorPortal Client copied to "./public_html/"')
    else:
        print("Aborting.")


def collect_env():
    import api.env as env

    env_src_path = f"{env.__path__[0]}/CreatorPortal/"
    shutil.copytree(env_src_path, "./CreatorPortal/")


def configure_env():
    # TODO: Implement env.yaml setup
    pass
