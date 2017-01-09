import os

from spyne import ServiceBase, File, rpc, Application, Unicode, ValidationError
from spyne.protocol.http import HttpRpc
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# RUN
# curl http://localhost:8000/get_file?path=http_soap_file.py


# When dealing with files, always have a designated file repository -- ie.
# a well-known directory where you store user-generated files.
#
# Here we're using os.getcwd() only because it's convenient. You must have a
# site-dependent absolute path that you preferably read from a config file
# here.
FILE_REPO = os.getcwd()
print(FILE_REPO)

class FileServices(ServiceBase):
    @rpc(Unicode, _returns=File)
    def get_file(ctx, path):
        # protect against file name injection attacks
        # note that this doesn't protect against symlinks. depending on the kind
        # of write access your clients have, this may or may not be a problem.
        if not os.path.abspath(path).startswith(FILE_REPO):
            raise ValidationError(path)
        print(path)
        return File.Value(path=path)


application = Application([FileServices], 'spyne.examples.file.soap',
                          in_protocol=HttpRpc(),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()