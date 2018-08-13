import os
import re
import zipfile
import wget
import urllib2
import logging
from git import Repo

class Downloader(object):
    """Constructor for Downloader_request."""
    def __init__(self, url, dir):
        super(Downloader, self).__init__()
        self.url = url
        self.dir = dir
        self.logger = logging.getLogger('analyser.namelist.NameListing')
        self.logger.info('creating an instance of NameListing')

    # FIXME: next step is to move to PyGithub API
    def download_github(self):
        repository = re.findall(r'/(\w+)', self.url)[-1]
        print("We would like to download {0:s}".format(repository))
        git_directory = self.dir + "/" + repository
        if not os.path.exists(git_directory):
            Repo.clone_from(self.url, git_directory)
            self.logger("Cloning from github {0:s}".format(self.url))

    # FIXME: add better checks
    def download_zip(self):
        filename = wget.download(self.url, self.dir)
        self.logger("Downloading from http %s", self.url)
        if filename.endswith('.zip'):
            try:
                zip_file = zipfile.ZipFile(filename)
            except zipfile.BadZipfile as ex:
                self.logger("%s no a zip file" % file)

    def resolving_download(self):
        request = urllib2.Request(self.url)
        request.get_method = lambda: 'HEAD'
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            return False
        # check if we have github link
        if re.search('github.com', self.url):
            self.download_github()
        elif re.search('.zip', self.url):
            self.download_zip()
        else:
            self.logger(" We work only with github repositories and zip files ")
