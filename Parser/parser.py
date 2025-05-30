from Tokenizer.tokenizer import Token, tokenize



class Node:
    def __init__(self,head,arr = None):
        self.head = head
        self.child = []
        if arr != None:
            for i in range(len(arr)):
                if(arr[i]!=None):
                    self.child.append(arr[i])
    
    def trav(self,n):
        if(type(self.head)==Token):
            st = f"<{self.head.getType()}:{self.head.getValue()}>"
        else:
            st = self.head
        print(f"{'.' * n} {st}")
        if self.child != []:
            for i in self.child:
                i.trav(n+1)

    def getChild(self, index):
        if index < len(self.child):
            return self.child[index]
        else:
            raise IndexError("Child index out of range")
    
    def clearAllChildren(self):
        self.child = []

    def changeHead(self, newHead):
        self.head = newHead

    def addChild(self, child):
        if isinstance(child, Node):
            self.child.append(child)
        else:
            raise TypeError("Child must be an instance of Node")


class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos = 0

    def gettoken(self):
        if self.pos<len(self.tokens):
            return self.tokens[self.pos]
        else:
            raise SyntaxError(f"index out of range")
    def movenext(self):
        if self.pos < len(self.tokens):
            self.pos += 1
        else:
            raise SyntaxError(f"Cannot move past end of tokens")
        
    def matchtype(self, value):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos].type == value
        return False
    
    def match(self, value):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos].value == value
        return False
        

        

    def E(self):
        if self.match("let"):
            self.movenext()
            l1 = self.D()
            if self.match("in"):
                self.movenext()
            else:
                print(self.gettoken().value)
                raise SyntaxError("syntax error")
            l2 = self.E()
            #print("E -> let D in E ")
            return Node("let",[l1,l2])
            
        elif self.match("fn"):
            self.movenext()
            li = []
            li.append(self.Vb())
            n = 1
            while self.pos < len(self.tokens) and (self.matchtype("ID") or self.match("(")):
                li.append(self.Vb())
                n+=1
            if self.match("."):
                self.movenext()
                li.append(self.E())
                #print (f"E -> fn {"Vb " * n}. E")
                return Node("lambda",li)
            else:
                raise SyntaxError("func E")
        else:
            l1 = self.Ew()
            #print("E -> Ew")
            return l1

    def Ew(self):
        l1 = self.T()
        if self.match("where"):
            self.movenext()
            l2 = self.Dr()
            #print("Ew -> T where Dr")
            return Node("where",[l1,l2])
        else:
            #print("Ew -> T")
            return l1
    
    def T(self):
        li = []
        li.append(self.Ta())
        if self.match(","):
            n = 1
            while self.match(","):
                self.movenext()
                li.append(self.Ta())
                n += 1
            #print(f"T -> {(n+1) * 'Ta '}")
            return Node("tau",li)
        else:
            #print("T -> Ta")
            return li[0]
    
    def Ta(self):
        l1 = self.Tc()
        flag = False
        while self.match("aug"):
            self.movenext()
            l2 = self.Tc()
            #print("Ta -> Ta aug Tc")
            flag = True
            l1 = Node("aug",[l1,l2])
        if not flag:
            #print("Ta -> Tc")
            pass
        return l1

    def Tc(self):
        l1 = self.B()
        if self.match("->"):
            self.movenext()
            l2 = self.Tc()
            if self.match("|"):
                self.movenext()
            else:
                raise SyntaxError(" | missing")
            l3 = self.Tc()
            #print("Tc -> B -> Tc | Tc")
            return Node("->",[l1,l2,l3])

        else:
            #print("Tc -> B")
            pass
        return l1

    def B(self):
        l1 = self.Bt()
        while self.match("or"):
            self.movenext()
            l2 = self.Bt()
            #print("B -> B or Bt")
            l1 =  Node("or",[l1,l2])
        #print("B-> Bt")
        return l1
    def Bt(self):
        l1 = self.Bs()
        while self.match("&"):
            self.movenext()
            l2 = self.Bs()
            #print("Bt -> Bt & Bs")
            l1 = Node("&",[l1,l2])
        #print("Bt-> Bs")
        return l1
    def Bs(self):
        if self.match("not"):
            self.movenext()
            l1 = self.Bp()
            #print("Bs -> not Bp")
            return Node("not",[l1])
        else:
            #print("Bs -> Bp")
            return self.Bp()
           

    def Bp(self):
        l1 = self.A()
        if self.pos < len(self.tokens):
            if self.match("gr") or self.match(">"):
                self.movenext()
                l2 = self.A()
                #print("Bp -> A gr A")
                return Node("gr",[l1,l2])
            elif self.match("ge") or self.match(">="):
                self.movenext()
                l2 = self.A()
                #print("Bp -> A ge A")
                return Node("ge",[l1,l2])
            elif self.match("ls") or self.match("<"):
                self.movenext()
                l2 = self.A()
                #print("Bp -> A ls A")
                return Node("ls",[l1,l2])
            elif self.match("le") or self.match("<="):
                self.movenext()
                l2 = self.A()
                #print("Bp -> A le A")
                return Node("le",[l1,l2])
            # elif self.match("gr") or self.match(">"):
            #     self.movenext()
            #     l2 = self.A()
            #     print("Bp -> A gr A")
            #     return Node("gr",[l1,l2])
            # elif self.match("ge") or self.match(">="):
            #     self.movenext()
            #     l2 = self.A()
            #     print("Bp -> A ge A")
            #     return Node("ge",[l1,l2])
            elif self.match("eq"):
                self.movenext()
                l2 = self.A()
                #print("Bp -> A eq A")
                return Node("eq",[l1,l2])
            elif self.match("ne"):
                self.movenext()
                l2 = self.A()
               # print("Bp -> A ne A")
                return Node("ne",[l1,l2])
            else:
                #print("Bp -> A ")
                pass
        else:
            #print("Bp -> A")
            pass
        return l1


    def A(self):
        if self.match("+"):
            self.movenext()
            l1 = self.At()
            #print("A -> + At")
            return l1
        elif self.match("-"):
            self.movenext()
            l1 = self.At()
            #print("A -> - At")
            return Node("neg",[l1])
        else:
            l2 = self.At()
            while self.pos < len(self.tokens):
                if self.match("+"):
                    self.movenext()
                    l3 = self.At()
                    #print("A -> A + At")
                    l2 = Node("+",[l2,l3])
                elif self.match("-"):
                    self.movenext()
                    l3 = self.At()
                    #print("A -> A - At")
                    l2 =  Node("-",[l2,l3])
                else:
                    break
            #print("A -> At")
            return l2
           

    def At(self):
        l1 = self.Af()
        while self.pos < len(self.tokens) and (self.match("*") or self.match("/")):
            if self.match("*"):
                self.movenext()
                l2 = self.Af()
                #print("At -> At * Af")
                l1 = Node("*",[l1,l2])
            elif self.match("/"):
                self.movenext()
                l2 = self.Af()
                #print("At -> At / Af")
                l1 = Node("/",[l1,l2])
            
        #print("At -> Af")
        return l1
    
    def Af(self):
        l1 = self.Ap()
        if self.match("**"):
            self.movenext()
            l2 = self.Af()
            #print("Af -> Ap ** Af")
            return Node("**",[l1,l2])
        else:
            #print("Af -> Ap")
            pass
        return l1

    def Ap(self):

        l1 = self.R()
        while self.match("@"):
            
            self.movenext()
            if self.matchtype("ID"):
                l2 = Node(self.gettoken())
                self.movenext()
            else:
                raise SyntaxError(" ID missing")
            l3 = self.R()
            #print(" Ap -> Ap @ <ID> R")
            
            l1 =  Node("@",[l1,l2,l3])
        
            
        
        #print("Ap -> R")
        return l1
    
    def can_start(self):
        if self.pos >= len(self.tokens):
            return False
        return (self.matchtype("ID") or 
                self.matchtype("INT") or 
                self.matchtype("STRING") or
                self.match("true") or 
                self.match("false") or 
                self.match("nil") or
                self.match("(") or 
                self.match("dummy"))
    
    def R(self):
        l1 = self.Rn()
        while self.pos < len(self.tokens) and self.can_start():
            l2 = self.Rn()
            #print("R -> R Rn")
            l1= Node ("gamma",[l1,l2])
        #print("R -> Rn")
        return l1
    
    def Rn(self):
        l2 = None
        if self.matchtype("ID"):
            l2 = Node(self.gettoken())
            self.movenext()
            #print( "Rn -> <ID>")
        elif self.matchtype("INT"):
            l2 = Node(self.gettoken())
            self.movenext()
            #print( "Rn -> <INT>")
        elif self.matchtype("STRING"):
            l2 = Node(self.gettoken())
            self.movenext()
            #print( "Rn -> <STRING>")
        elif self.match("true"):
            l2 = Node("true")
            self.movenext()
            #print( "Rn -> true")
        elif self.match("false"):
            l2 = Node("false")
            self.movenext()
            #print( "Rn -> false")
        elif self.match("nil"):
            l2 = Node("nil")
            self.movenext()
            #print( "Rn -> nil")
        elif self.match("("):
            self.movenext()
            l2 = self.E()
            if self.match(")"):
                self.movenext()
                #print( "Rn -> ( E )")
            else:
                raise TypeError(") missing")
        
        elif self.matchtype("dummy"):
            l2 = Node("dummy")
            self.movenext()
            #print( "Rn -> dummy")

        else:
            raise TypeError(f"errored {self.gettoken().value}")
        return l2

    def D(self):
        l1 = self.Da()
        if self.match("within"):
            self.movenext()
            l2 = self.D()
            #print("D -> Da within D")
            return Node("within",[l1,l2])
        else:
            #print("D -> Da")
            pass
        return l1
    
    def Da(self):
        li = []
        li.append(self.Dr())
        n= 0
        while self.match("and"):
            self.movenext()
            li.append(self.Dr())
            n+=1
        if n>0:
            #print(f"Da -> Dr {n* 'and Dr '}")
            return Node("and",li)
        else:
            #print("Da -> Dr")
            pass
        return li[0]
        
    
    def Dr(self):
        if self.match("rec"):
            self.movenext()
            l1 = self.Db()
            #print("Dr -> rec Db")
            return Node("rec",[l1])
        else:
            #print("Dr -> Db")
            return self.Db()
           
    
    def checkvl(self):
        if self.gettoken().type == "ID" and (self.pos + 1 < len(self.tokens)):
            return self.tokens[self.pos + 1].value == "," or self.tokens[self.pos + 1].value == "="
        return False
    def list_form_finder(self):
        if not self.matchtype("ID"):
            return False
        
        saved_pos = self.pos
        try:
            self.movenext()
            result = self.match("=") or self.match(",")
            self.pos = saved_pos
            return result
        except:
            self.pos = saved_pos
            return False

    def Db(self):
        if self.checkvl():
            l1 = self.Vl()
            if self.match("="):
                self.movenext()
            else:
                raise TypeError("= missing")
            l2 = self.E()
            #print("Db -> Vl = E")
            return Node("=",[l1,l2])
        elif self.matchtype("ID"):
            li = []
            l1 = Node(self.gettoken())
            li.append(l1)
            self.movenext()
            li.append(self.Vb())
            n = 1
            while self.pos < len(self.tokens) and (self.matchtype("ID") or self.match("(")):
                li.append(self.Vb())
                n+=1
            if self.match("="):
                self.movenext()
                li.append(self.E())
                #print(f"Db -> <ID> {n*"Vb "} = E")
                return Node("fcn_form",li)
            else:
                raise TypeError("== missing")
            return l1
        elif self.match("("):
            self.movenext()
            l1 = self.D()
            if self.match(")"):
                self.movenext()
                #print("Db -> ( E )")
                return l1
            else:
                raise TypeError(")missing")
            return l1
        else:
            raise TypeError("final")
    
    def Vb(self):
        if self.matchtype("ID"):
            l1 = Node(self.gettoken())
            self.movenext()
            #print("Vb -> <ID>")
            return l1
        elif self.match("("):
            self.movenext()
            if self.match(")"):
                self.movenext()
                #print("Vb -> ( )")
                return Node("()",[Node("("),Node(")")])
            else:
                l1 = self.Vl()
                if self.match(")"):
                    self.movenext()
                    #print("Vb -> ( Vl )")
                    return l1
                else:
                    raise SyntaxError(" Vb prob")
        else:
            raise SyntaxError(" Vb prob")


    def Vl(self):
        n = 0
        li = []
        if self.matchtype("ID"):
            li.append(Node(self.gettoken()))
            self.movenext()
            n+=1
        else:
            raise SyntaxError(f"Vl error")
        
        while self.match(","):
            self.movenext()
            if self.matchtype("ID"):
                li.append(Node(self.gettoken()))
                self.movenext()
                n+=1
            else:
                raise SyntaxError(f"Vl 2 error")
        #print(f"Vl -> {n* "<ID>"}")
        if(n>1):
            return Node(",",li)
        else:
            return li[0]


            

        
with open("test", 'r') as file:
        #try:
            lines = file.readlines()
            tokens = tokenize(lines)
            print("Tokens: ")
            # for token in tokens:
            #     print(f'<{token.type}>: <{token.value}>')
            par = Parser(tokens)
            ast = par.E()
            print("*************************************************AST*************************************************")
            ast.trav(0)


            



    
