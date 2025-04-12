def read_config(file_path):
    """Reads configuration values from a config.txt file."""
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            # Skip empty lines and comments
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                config[key.strip()] = value.strip()
    if "MOVIES_FOLDERS" in config:
        # Split and filter out empty strings
        config["MOVIES_FOLDERS"] = [folder.strip().replace('"', '').lower() for folder in config["MOVIES_FOLDERS"].split(",") if folder.strip()]
    if "SERIES_FOLDERS" in config:
        # Split and filter out empty strings
        config["SERIES_FOLDERS"] = [folder.strip().replace('"', '').lower() for folder in config["SERIES_FOLDERS"].split(",") if folder.strip()]
    return config

def generate_docker_compose(config):

    server_name = config.get("SERVER_NAME").replace('"', '').lower()
    tailscale_user_key = config.get("TAILSCALE_USER_KEY").replace('"', '').lower()
    domain = f"{server_name}.{tailscale_user_key}.ts.net"
    tailscale_auth_key = config.get("TAILSCALE_AUTH_KEY").replace('"', '')

    movie_volumes = [
        f"{folder}:/movies{index + 1}" 
        for index, folder in enumerate(config.get("MOVIES_FOLDERS", []))
    ]

    series_volumes = [
        f"{folder}:/series{index + 1}" 
        for index, folder in enumerate(config.get("SERIES_FOLDERS", []))
    ]

    docker_compose = {
        "services": {
            "tailscale-jellyfin": {
                "image": "tailscale/tailscale:v1.82.0",
                "container_name": "tailscale-jellyfin",
                "hostname": f"{server_name}",
                "cap_add": ["NET_ADMIN"],
                "environment": {
                    "TS_AUTHKEY": f"{tailscale_auth_key}",
                    "TS_STATE_DIR": "/var/lib/tailscale",
                    "TS_SERVE_CONFIG": "/config/funnel.json",
                    "TS_USERSPACE": "false",
                },
                "restart": "unless-stopped",
                "volumes": [
                    "./.tailscale/state:/var/lib/tailscale",
                    "./.tailscale/config:/config",
                ],
                "devices": ["/dev/net/tun:/dev/net/tun"],
                "ports": [
                    "8096:8096",
                    "8920:8920",
                    "1900:1900/udp",
                    "7359:7359/udp",
                ],
            },
            "jellyfin": {
                "image": "jellyfin/jellyfin",
                "container_name": "jellyfin",
                "volumes": [
                    "./.jellyfin/config:/config",
                    "./.jellyfin/cache:/cache",
                    *movie_volumes,
                    *series_volumes,
                ],
                "restart": "unless-stopped",
                "environment": {
                    "JELLYFIN_PublishedServerUrl": f"https://{domain}",
                },
                "depends_on": ["tailscale-jellyfin"],
                "network_mode": "service:tailscale-jellyfin",
            },
        },
    }

    # Write to docker-compose.yml
    with open("docker-compose-test.yml", "w") as file:
        yaml.dump(docker_compose, file, default_flow_style=False)

    print("docker-compose.yml has been generated successfully!\nNow you can run `docker-compose up -d` to start the containers.")

def generate_funnel_json(config):
    """Generates the funnel.json file."""
    server_name = config.get("SERVER_NAME")
    tailscale_user_key = config.get("TAILSCALE_USER_KEY")
    domain = f"{server_name}.{tailscale_user_key}.ts.net"
    tailscale_funnel = config.get("TAILSCALE_FUNNEL", "false").lower() == "false"

    funnel_config = {
        "TCP": {
            "443": {
                "HTTPS": True
            }
        },
        "Web": {
            f"{domain}:443": {
                "Handlers": {
                    "/": {
                        "Proxy": "http://localhost:8096"
                    }
                }
            }
        },
        "AllowFunnel": {
            f"{domain}:443": tailscale_funnel
        }
    }

    # Write to funnel.json
    with open(".tailscale/config/funnel.json", "w") as file:
        json.dump(funnel_config, file, indent=4)

    print("funnel.json has been generated successfully!")

if __name__ == "__main__":
    # Check and install dependencies
    try:
        import yaml
        import os
        import json
    except ImportError as e:
        print(f"Missing dependency: {e.name}. Please install it using pip. Hint: pip install pyyaml")
        exit(1)
    # Read configuration from config.txt
    config = read_config("config.txt")
    os.makedirs(".tailscale", exist_ok=True)
    os.makedirs(".tailscale/config", exist_ok=True)
    os.makedirs(".tailscale/state", exist_ok=True)
    # Generate funnel.json
    generate_funnel_json(config)
    # Generate docker-compose.yml
    generate_docker_compose(config)