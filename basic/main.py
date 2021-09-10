import cmd


class operator():
    def __init__(self, id):
        self.id = id.upper() #aceitando letras minusculas como entrada
        self.available = True
        self.ring = None
        self.busy = False


class Cmd(cmd.Cmd):
    def do_test(self,arg):
        print (arg)
        return 
    
    
    def do_call(self, arg):
        print ('Call ' + arg + ' received')
        for i in list_:
            if (i.available == True): # verifica se o operador na posicao i esta livre
                print ('Call ' + arg + ' ringing for operator ' + i.id)
                i.ring = arg
                i.available = False
                return 
            
        print('Call ' + arg + ' waiting in queue')#caso onde A e B estao ocupados
        queue.append(arg) #adiciona arg na lista de execuçao 

    def do_answer(self,arg):
        arg = arg.upper()
        for i in list_:
            if(i.id == arg):
                print ('Call ' + i.ring +' answered by operator ' + arg)
                i.busy = True
                return
    
    def do_hangup (self,arg):
        for i in list_:
            if(i.busy == False and i.ring == arg): # caso que esta chamando
                print('Call ' + arg + ' missed')
                i.available = True
                i.ring = None
                break


            elif(i.ring == arg and i.busy == True): # caso que chamada foi aceita
                print ('Call ' + i.ring +' finished and operator ' + i.id + ' available')
                i.ring = None
                i.available = True
                i.busy = False
                break
            
            elif(i.busy == False and i.ring != arg and i.available == False): # caso que esta na fila de espera
                print('Call ' + arg + ' missed')
                index = queue.index(arg)
                queue.pop(index)
                break
            
        check_queue()
        
    
    def do_reject(self, arg):
        arg = arg.upper()
        for i in list_:    
            if(i.id == arg):
                print ('Call ' + i.ring +' rejected by operator ' + arg)
                print ('Call ' + i.ring +' ringing for operator ' + arg)
             

    def do_exit(self, arg):
        # self.close()
        return True



def check_queue():
    if (len(queue) == 0):
        # print('aqui')
        return
    else:
        for i in list_:
            if (i.available == True): # verifica se o operador na posicao i esta livre
                print ('Call ' + queue[0] + ' ringing for operator ' + i.id)
                i.ring = queue[0]
                i.available = False
                queue.pop(0)
                return

def set_operators():
    a = operator('a')
    b = operator('b')
    list_ = [a,b]
    return list_ 



list_ = set_operators() #global list with operators 
queue = []

if __name__ == "__main__":    
    Cmd=Cmd()
    Cmd.prompt = '(telephony) '
    Cmd.cmdloop()