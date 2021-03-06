import pexpect
from django.conf import settings

from .exceptions import TelnetUnexpectedResponse, TelnetConnectionTimeout, TelnetLoginFailed

class TelnetConnectionMiddleware(object):

    def process_request(self, request):
        """Add a telnet connection to all request paths that start with /api/
        assuming we only need to connect for these means we avoid unecessary
        overhead on any other functionality we add, and keeps URL path clear
        for it.
        """

        if not request.path.startswith('/api/'):
            return None

        request.telnet = None

        if settings.DEBUG:
            print "settings.JASMIN_DOCKER: {}\n settings.JASMIN_K8S: {}".format(settings.JASMIN_DOCKER, settings.JASMIN_K8S)

        if settings.JASMIN_DOCKER == True:
            request.telnet_list = []
            for port in settings.JASMIN_DOCKER_PORTS:
                telnet = self.telnet_request(settings.TELNET_HOST, port, settings.TELNET_USERNAME, settings.TELNET_PW)
                try:
                    telnet.expect_exact(settings.STANDARD_PROMPT)
                except pexpect.EOF:
                    raise TelnetLoginFailed
                else:
                    if request.telnet == None:
                        request.telnet = telnet
                    else:
                        request.telnet_list.append(telnet)
            if request.telnet == None:
                raise TelnetLoginFailed
            return None

        if settings.JASMIN_K8S == True:
            request.telnet_list = []
            all_pods = self.set_telnet_list()
            print "Finding pods..."
            print "We find {} pods in k8s".format(len(all_pods))
            for host in all_pods:
                telnet = self.telnet_request(host, settings.TELNET_PORT, settings.TELNET_USERNAME, settings.TELNET_PW)
                try:
                    telnet.expect_exact(settings.STANDARD_PROMPT)
                except pexpect.EOF:
                    raise TelnetLoginFailed
                else:
                    if request.telnet == None:
                        request.telnet = telnet
                    else:
                        request.telnet_list.append(telnet)
            if request.telnet == None:
                raise TelnetLoginFailed
            print "We find {} pods if telnet connection up".format(len(request.telnet_list))
            return None

        telnet = self.telnet_request(settings.TELNET_HOST, settings.TELNET_PORT, settings.TELNET_USERNAME, settings.TELNET_PW)
        try:
            telnet.expect_exact(settings.STANDARD_PROMPT)
        except pexpect.EOF:
            raise TelnetLoginFailed
        else:
            request.telnet = telnet

        if request.telnet == None:
            raise TelnetLoginFailed

        return None

    def set_telnet_list(self):
        api_response = settings.K8S_CLIENT.list_namespaced_pod(settings.JASMIN_K8S_NAMESPACE, label_selector="jasmin")
        if settings.DEBUG:
            print "Response K8S: {}".format(len(api_response.items))
        msg = []
        for i in api_response.items:
            if hasattr(i, "status"):
                msg.append(i.status.pod_ip)

        if len(msg) == 0:
            raise TelnetLoginFailed

        return msg

    def telnet_request(self, host, port, user, pw):
        try:
            telnet = pexpect.spawn(
                "telnet %s %s" %
                (host, port),
                timeout=settings.TELNET_TIMEOUT,
            )
            telnet.expect_exact('Username: ')
            telnet.sendline(user)
            telnet.expect_exact('Password: ')
            telnet.sendline(pw)
        except pexpect.EOF:
            raise TelnetUnexpectedResponse
        except pexpect.TIMEOUT:
            raise TelnetConnectionTimeout

        return telnet

    def process_response(self, request, response):
        "Make sure telnet connection is closed when unleashing response back to client"
        if hasattr(request, 'telnet'):
            if request.telnet != None:
                try:
                    request.telnet.sendline('quit')
                except pexpect.ExceptionPexpect:
                    request.telnet.kill(9)

        if hasattr(request, 'telnet_list'):
            for telnet in request.telnet_list:
                try:
                    request.telnet.sendline('quit')
                except pexpect.ExceptionPexpect:
                    request.telnet.kill(9)

        return response
