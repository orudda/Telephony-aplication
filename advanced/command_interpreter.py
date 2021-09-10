
from twisted.internet import reactor, protocol
from twisted.internet import stdio
from twisted.protocols import basic
import cmd, json , sys
# from os import linesep as delimiter



class Cmd(cmd.Cmd):

    def do_call(self, arg):
        call_id = arg.split()[0]
        print('aqui')
        request = json.dumps({'command': 'call', 'id': call_id})
        return request

    def do_answer(self, arg):
        operator = arg.split()[0]
        request =  json.dumps({'command': 'answer', 'id': operator})
        return request

    def do_reject(self, arg):
        operator = arg.split()[0]
        request = json.dumps({'command': 'reject', 'id': operator})
        return request

    def do_hangup(self, arg):
        call=arg.split()[0]
        request = json.dumps({'command': 'hangup', 'id': call})
        return request

    def default(self, arg):
        args=arg.split()[0]
        if(args!='#'):
            print ('*** Unknown syntax: ' + str(args))
        return False

    def emptyline(self):
        return False

    def do_exit(self,arg):
        return 'exit'

class CommandInterpreter(protocol.Protocol):

    def dataReceived(self, data):
        print (data)
        sys.stdout.write('>>> ')
        sys.stdout.flush()

    def sendRequest(self, request):
        if request == 'exit':
            self.transport.loseConnection()
            return
        self.transport.write(request)

class CommandInterpreterFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        global myCommandInterpreter
        myCommandInterpreter = CommandInterpreter()
        return myCommandInterpreter

    def clientConnectionFailed(self, connector, reason):
        print ("Connection Failed " + str(reason))
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        reactor.stop()

class InputReader(basic.LineReceiver):
    from os import linesep as delimiter
    # basic.LineReceived = basic.LineReceived.encode('ascii')

    def connectionMade(self):
        # print('ola')
        self.transport.write('\'exit\' to exit\n>>> '.encode('ascii'))

    def lineReceived(self, line):
        # print('oi')
        
        request = Cmd.onecmd(line)
        # print(request)
        if not request:
            self.transport.write('>>> ')
        if request:
            # print(request)
            myCommandInterpreter.sendRequest(request)


myCommandInterpreter = None
Cmd=Cmd()
reactor.connectTCP("localhost", 5678, CommandInterpreterFactory())
stdio.StandardIO(InputReader())
reactor.run()