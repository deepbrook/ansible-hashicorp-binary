import html.parser
import re
import urllib.request

version_pattern = re.compile(r"^\d+\.\d+\.\d+")


class HashiCorpReleasesPageParser(html.parser.HTMLParser):
    tools = ["vagrant", "packer", "terraform", "consul", "vault", "nomad"]

    def __init__(self, tool, version=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.releases = []
        self.RELEASE_BASE_URL = f"https://releases.hashicorp.com/{tool}/"

    def handle_data(self, data):
        if any(data.startswith(tool) for tool in self.tools):
            _, version = data.split("_", maxsplit=1)
            if version_pattern.match(version):
                self.releases.append(version)

    @property
    def latest_version(self) -> str:
        with urllib.request.urlopen(self.RELEASE_BASE_URL) as r:
            self.feed(r.read().decode())
        latest = self.releases[0]
        self.releases = []
        return latest
