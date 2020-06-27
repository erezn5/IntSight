import json
import requests

from utilities.BaseClass import BaseClass


class Gist(BaseClass):
    GITHUB_API = "https://api.github.com"
    url = GITHUB_API + "/gists"

    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': 'token %s' % self.token}
        self.params = {'scope': 'gist'}

    def list_gists(self):
        log = self.get_logger()
        log.info("Listing gist for the authenticated user:")
        res = self.get_request(self.url)
        # res = requests.get(self.url, headers=self.headers)
        log.info("List of gists are {}".format(res.text))
        j = json.loads(res.text)
        assert len(j) != 0, log.error("List should contain some gist")
        for gist in range(len(j)):
            log.info("Gist URL : %s" % gist)

    def create_gist(self, payload="{default payload for creation of gist}"):
        log = self.get_logger()
        res = requests.post(self.url, headers=self.headers, params=self.params, data=json.dumps(payload))
        j = json.loads(res.text)
        if res.status_code == 201:
            log.info("Gist Created Successfully with gist id: {}".format(j['id']))
        else:
            log.error("Gist failed to be created")
        log.info(res.status_code)
        return res.text

    def edit_gist(self, gist_id, payload=None):
        log = self.get_logger()
        log.info("Requested url is {}".format(self.url))
        print("Requested url is {}".format(self.url))
        res = requests.patch(self.url + "/{}".format(gist_id), headers=self.headers, params=self.params,
                             data=json.dumps(payload))
        if res.status_code != 200:
            log.error("Patch (update) request failed, response code is: {}".format(res.status_code))
            return None
        return res.text

    def get_gist(self, gist_id):
        log = self.get_logger()
        url_req = self.url + "/{}".format(gist_id)
        res = self.get_request(url_req)
        # res = requests.get(self.url + "/{}".format(gist_id), headers=self.headers, params=self.params)
        if res.status_code == 200:
            return res.text
        else:
            return res.status_code

    def star_gist(self, gist_id):
        log = self.get_logger()
        url_req = self.url + "/{}/star".format(gist_id)
        log.info("URL put request is: {}".format(url_req))
        res = requests.put(url_req, headers=self.headers)
        if res.status_code == 204:
            log.info("Gist starred successfully!")
        elif res.status_code != 204:
            log.error("Gist did not starred as expected")

    def check_gist_starred(self, gist_id):
        log = self.get_logger()
        url_req = self.url + "/{}/star".format(gist_id)
        res = self.get_request(url_req)
        # res = requests.get(url_req, headers=self.headers)
        if res.status_code == 204:
            log.info("Gist is starred!")
            return True
        elif res.status_code == 404:
            log.error("Gist is not starred!")
            return False

    def delete_git(self, gist_id):
        log = self.get_logger()
        url = self.url + "/{}".format(gist_id)
        res = requests.delete(url, headers=self.headers, params=self.params)
        if res.status_code != 204:
            log.error("Expected status code 204, instead we got status code: {}".format(res.status_code))
        else:
            log.info("Gist with gist ID: {} deleted successfully".format(gist_id))

    def get_request(self, url_req):
        return requests.get(url_req, headers=self.headers, params=self.params)