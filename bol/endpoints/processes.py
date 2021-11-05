from .base import APIEndpoint

from bol.models.processes import ProcessStatus

class ProcessMethods(APIEndpoint):

    def __init__(self, api):
        super(ProcessMethods, self).__init__(api, "process-status")

    def get(self, id):

        if self.api.demo: id = 'c628ba4f-f31a-4fac-a6a0-062326d0dbbd'

        url = '{endpoint}/{id}'.format(endpoint=self.endpoint, id=id)
        data = None

        status, headers, respContent = self.api.get(url, data)
        if status == 400: return ProcessStatus().parseError(respContent)

        return ProcessStatus().parse(respContent)