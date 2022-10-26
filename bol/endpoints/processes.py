from .base import APIEndpoint

from bol.models.processes import ProcessStatus

class ProcessMethods(APIEndpoint):

    def __init__(self, api):
        super(ProcessMethods, self).__init__(api, "process-status")

    def get(self, id):

        if self.api.demo: id = '2'

        url = '{sharedUrl}/{endpoint}/{id}'.format(sharedUrl=self.api.sharedUrl, endpoint=self.endpoint, id=id)
        data = None

        status, headers, respContent = self.api.get(url, data, overwriteURL=True)
        if status == 400: return ProcessStatus().parseError(respContent)

        return ProcessStatus().parse(respContent)