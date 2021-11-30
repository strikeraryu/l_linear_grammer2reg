class llg2reg():
    def __init__(self, grammer):
        self.grammer = grammer
        self.prod_rules = list(map(lambda x : x.strip(), grammer.split(",")))
        self.trans = {}
        self.rev_trans = {}
        self.graph = {}
        self.rev_graph = {}
        self.intial_state = ''
        self.states = set()
        self.reg = ""

    def create_data(self):
        self.trans = {}
        self.rev_trans = {}
        self.graph = {}
        self.rev_graph = {}
        self.intial_state = ''
        self.states = set()

        for i, rule in enumerate(self.prod_rules):
            start_symbol, exps = list(map(lambda x : x.strip(" "), rule.split("->")))
            if i == 0: self.intial_state = start_symbol

            if "/" in exps: exps = list(map(lambda x : x.strip(" "), exps.split("/")))
            else: exps = [exps]
            
            for exp in exps:
                n_terminal = list(filter(lambda x : x.isupper(), exp))
                ind = len(exp)
                
                for i, c in enumerate(exp):
                    if not c.isupper() : ind = i; break
                    
                if len(n_terminal) == 0: n_terminal.append("ff")

                if ind != -1: terminal = [exp[ind:]]
                else: terminal = []

                for t in n_terminal:
                    self.trans[start_symbol] = self.trans.get(start_symbol, [])
                    self.trans[start_symbol].append({"transition": terminal, "node": t})

        self.trans["ss"] = [{'transition': ['e'], 'node': self.intial_state}]

        for state in self.trans:
            for eq in self.trans[state]:
                self.rev_trans[eq["node"]] = self.rev_trans.get(eq["node"], [])
                self.rev_trans[eq["node"]].append({"transition": eq["transition"], "node": state})

        for key in self.trans:
            self.states.add(key)
        for key in self.rev_trans:
            self.states.add(key)


        self.graph = {key:{key:[] for key in self.states} for key in self.states}

        for nd in self.trans:
            for tn in self.trans[nd]:
                self.graph[nd][tn['node']].extend(tn["transition"])



    def log_data(self, full=False):
        print("------- Graph -------")
        for nd in self.graph:
            for tn in self.graph[nd]:
                if len(self.graph[nd][tn]) != 0 or full: 
                    print(f"{nd} -> {tn} ==" + str(self.graph[nd][tn]))
        print("\n\n")
        print("------- Reverse Graph -------")
        for nd in self.rev_graph:
            for tn in self.rev_graph[nd]:
                if len(self.rev_graph[nd][tn]) != 0 or full: 
                    print(f"{nd} -> {tn} ==" + str(self.rev_graph[nd][tn]))

    def create_reg(self):
        self.create_data()
        print(self.states)
        for nd in self.states:
            if nd in ["ss", "ff"]: continue
            
            if len(self.graph[nd][nd]) == 0: re_m = ""
            else: re_m = "(" + "+".join(self.graph[nd][nd]) + ")*"
            
            self.graph[nd][nd] = []
            
            nexts = set([x for x in self.graph[nd] if len(self.graph[nd][x]) > 0])
            prevs = set()

            for i in self.graph:
                for j in self.graph[i]:
                    if len(self.graph[i][j])>0 and j==nd: prevs.add(i)
            
            for pr in prevs:
                for nx in nexts:
                    if pr == nd or nx == nd: continue
                    print(pr, nx, nd)
                    if len(self.graph[pr][nd]) == 0:re_p = ""
                    else: re_p = "(" + "+".join(self.graph[pr][nd]) + ")"
                    if len(self.graph[nd][nx]) == 0: re_n = ""
                    else: re_n = "(" + "+".join(self.graph[nd][nx]) + ")"
                    
                    self.graph[nd][nx] = []
                    
                    if len(re_p + re_m + re_n) != 0:
                        self.graph[pr][nx].append("(" + re_p + re_m + re_n + ")")

                self.graph[pr][nd] = []
            print(self.graph)

        self.reg = self.graph["ss"]["ff"]

        return self.reg


# eg 
# S -> B00/S11, B -> B0/B1/0/1
# B->Aa/Ba/Bb, A->
