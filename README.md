# nanods
> nanogram darkweb scraper

A simple dark web parser that has a small and simple cache system
to avoid re-downloading the same page multiple times.

### Installation

1. Create a Python3 virtual environment and install dependencies written in `requirements.txt`.
2. Install `tor` daemon and enable it via `systemctl`.

```
sudo apt-get update
sudo apt-get install tor -y
sudo systemctl start tor
```
3. If `tor` started successfully, then go to the configuration file(`/etc/tor/torrc`)
   and configure the following line. After that, restart the `tor` daemon. If everything works well,
   you're ready to run the project.
```
SOCKSPort 9050
ControlPort 9051
CookieAuthentication 1
MaxCircuitDirtiness 60
```

### Run it

```
python main.py http://<onion>.onion/path?asdf=asdf
python main.py http://<onion>.onion/path?asdf=asdf --out page.html
python main.py http://<onion>.onion/path?asdf=asdf --no-cache
```
