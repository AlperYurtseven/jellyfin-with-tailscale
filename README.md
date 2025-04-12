# Jellyfin (media server) with Tailscale
Dockerized Jellyfin server with Tailscale automatic creation files

# Step by step guide

* Go to [text](https://tailscale.com/)
* Create or login your existing account
* Go to [text](https://login.tailscale.com/admin/settings/keys)
* Click Generate auth key… button
* Add key to config file in: TAILSCALE_AUTH_KEY variable
* Go to [text](https://login.tailscale.com/admin/dns)
* Find your Tailnet username (starts with tail...)
* Add Tailnet username to config file in: TAILSCALE_USER_KEY variable
* (Optional) set TAILSCALE_FUNNEL variable in config file to true if you want to make your server accessible outside the tailscale network (i.e. open to public internet)
* Set your SERVER_NAME (e.g. wolfgangflix). Caution, this name will be visible in your server's url, choose wisely
* Set your movies or series folder with full paths in your pc, you can give as much as you want
* Everything is set, you can continue to usage step

# Usage
Fill up the config.txt.
Then,

```bash
python docker_yml_creator.py
```

# Add this to Access Controls in Tailscale if you want to use funnel i.e. open your server to public internet

```bash
# Funnel policy, which lets tailnet members control Funnel
# for their own devices.
# Learn more at https://tailscale.com/kb/1223/tailscale-funnel/

nodeAttrs=(
  '{"target": ["autogroup:member"], "attr": ["funnel"]}'
)
```

