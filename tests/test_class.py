import json

from framework.GistActionClass import Gist
from tests.conftest import ValueStorage
from utilities.BaseClass import BaseClass


class Test(BaseClass):

    api_token = 'f07dc08cdbd109b2952da638b97e3cbf6f96432f'
    gist = Gist(api_token)

    # Assumption is that there are already gists in the repo
    def test_list_gists(self):
        self.log = self.get_logger()
        self.gist.list_gists()

    def test_create_gist(self):
        self.log = self.get_logger()
        payload = {"description": "GIST created by python code", "public": True, "files": {"python request module": {
            "content": "Python requests has 3 parameters: 1)Request URL\n 2)Header Fields\n 3)Parameter \n4)Request body"}}}
        json_obj = json.loads(self.gist.create_gist(payload))
        ValueStorage.gist_id = json_obj['id']

        self.log.info("Gist created successfully")

    def test_edit_gist(self):
        payload = {"description": "GIST created by python code", "public": True, "files": {"module": {"content": "EDIT"}}}
        log = self.get_logger()
        json_obj = json.loads(self.gist.edit_gist(ValueStorage.gist_id, payload))
        assert json_obj['files']['module']['content'] == "EDIT", "Failed, Edit gist was a big failure"
        log.info("Success!! Editing gist revision is successful!")

    def test_get_gist_revision(self):
        log = self.get_logger()
        self.gist.get_gist(ValueStorage.gist_id)

    def test_star_gist(self):
        log = self.get_logger()
        self.gist.star_gist(ValueStorage.gist_id)
        assert self.gist.check_gist_starred(ValueStorage.gist_id),\
            log.error("Gist with id: {} should be starred and it is not".format(ValueStorage.gist_id))

    def test_delete_gist(self):
        log = self.get_logger()
        self.gist.delete_git(ValueStorage.gist_id)
        assert self.gist.get_gist(ValueStorage.gist_id) == 404, \
            log.error("Gist was supposed to be deleted with no ID but ID was found: {}".format(ValueStorage.gist_id))
