# jellyfin-with-tailscale
Dockerized Jellyfin with Tailscale container creation files

# Usage

Fill up the config.txt.
Then,

```bash
python docker_yml_creator.py
```


# Add this to Access Controls in Tailscale if you want to use funnel

```bash
# Funnel policy, which lets tailnet members control Funnel
# for their own devices.
# Learn more at https://tailscale.com/kb/1223/tailscale-funnel/

nodeAttrs=(
  '{"target": ["autogroup:member"], "attr": ["funnel"]}'
)
```

