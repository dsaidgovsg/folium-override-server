# Folium Override Server

Webserver to re-generate uploaded folium map to use custom URLs.

## What does this do

This webservice allows any generate `folium` map done via `.save()` and `._repr_html_()` to have all
its external resource URLs replaced with custom URLs, so that the HTML file is transformed to point
to custom hosts to load all its external resources. This is useful for hosting and showing maps
within non-Internet zone for example.

These URLs to be replaced are split into two sets:

- JS and CSS resource URLs required to display the elements which can be replaced
- Tileserver URL to use custom `tileserver-gl` map tiles

Simply go to the root path of the service and submit your `folium` HTML file to

## Local demo set-ups

### `python3` + `venv` set-up

You will need at least Python 3.6 with `venv` and `pip` modules installed.

See
<https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv>
for more details on the installation on `venv`.

Assuming the virtual environment directory to save into is `~/.fover`,
run the command to create the above directory:

```bash
python3 -m venv ~/.fover
```

Then go into your environment by running `source`:

```bash
source ~/.fover/bin/activate
```

Then run the following to install the requirements:

```bash
python3 -m pip install -r requirements.txt
```

Finally, you will need to set the required env vars in `.env` file. The page will still work but the
generated HTML file will not make sense with the default env var values.

Finally simply do

```bash
gunicorn app:app
```

In your web browser, go to <http://localhost:8000>.

If you want to customize the port, binding address or the number of workers to run with, look at the
official documentation for more details: <https://docs.gunicorn.org/en/stable/run.html>.

### `docker-compose` set-up

You will need `docker` and `docker-compose`.

Simply run

```bash
docker-compose up --build
```

In your web browser, go to <http://localhost:8000>.

## Versioning

The tag release system here follows this format `vX.Y.Z_folium-v0.10.1`. The`vX.Y.Z` part is the
semver for this repository, while the `folium-v0.10.1` part is to match the resources that was
extracted from `folium` `v0.10.1`.

## Updating external JSON

The external JSON files required for URL replacement is extracted from
<https://github.com/dsaidgovsg/folium-resource-server>.

The `folium` version tagged in this repo will fetch the corresponding matching `folium` version in
the above repository.

For convenience, a script to download and update the external JSON files is created at
`update-external.sh`. If the `folium` version changes for this repository, the script should also be
updated accordingly.
