class Processo:
    def __init__(self, pid, tempo_execucao, tempo_chegada, deadline=0):
        self.pid = pid
        self.tempo_total = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_chegada = tempo_chegada
        self.deadline = deadline
        self.tempo_conclusao = 0
        self.turnaround = 0
        self.waiting = 0
        self.atraso = 0 
        self.concluido = False 

    def reset(self):
        self.tempo_restante = self.tempo_total
        self.tempo_conclusao = 0
        self.turnaround = 0
        self.waiting = 0
        self.concluido = False


class Escalonador:

    def menu(self):
        while True:
            print("\n====== SIMULADOR DE ESCALONAMENTO ======")
            print("1 - Interativo - Round Robin")
            print("2 - Lote - FCFS / SJF / SRTN")
            print("3 - Tempo Real - EDF (Earliest Deadline First)")
            print("0 - Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.round_robin()
            elif opcao == "2":
                self.menu_lote()
            elif opcao == "3":
                self.real_time()
            elif opcao == "0":
                print("Encerrando...")
                break
            else:
                print("Opção inválida!")

    # ================= ROUND ROBIN =================

    def round_robin(self):
        fila = []
        processos_finalizados = []
        pid = 1
        tempo_atual = 0

        try:
            quantum = int(input("\nDigite o valor do quantum (em segundos): "))
            n = int(input("Quantos processos iniciais deseja inserir? "))

            for i in range(n):
                tempo = int(input(f"Tempo de execução do processo {pid}: "))
                fila.append(Processo(pid, tempo, tempo_atual))
                pid += 1

            print("\n--- Iniciando Round Robin ---\n")

            while len(fila) > 0:

                print(f"\n[Tempo {tempo_atual}] Fila: {[p.pid for p in fila]}")
                
                opcao = input("Pressione ENTER para continuar ou 'i' para inserir novo processo: ").lower()

                if opcao == 'i':
                    pid = self.inserir_novo_processo(fila, pid, tempo_atual)

                processo = fila.pop(0)
                print(f"Executando Processo {processo.pid}")

                tempo_exec = min(quantum, processo.tempo_restante)
                print(f"Tempo executado: {tempo_exec}s")

                processo.tempo_restante -= tempo_exec
                tempo_atual += tempo_exec

                if processo.tempo_restante > 0:
                    print(f"-> Processo {processo.pid} não terminou. Voltando para fila.")
                    fila.append(processo)
                else:
                    self.finalizar_processo(processo, tempo_atual, processos_finalizados)

            self.mostrar_estatisticas(processos_finalizados)

        except ValueError:
            print("Erro: Digite apenas números inteiros.")

    def inserir_novo_processo(self, fila, pid, tempo_atual, tipo="RR"):
        try:
            tempo = int(input(f"Tempo de execução do novo processo {pid}: "))
            novo = Processo(pid, tempo, tempo_atual)
            fila.append(novo)
            print(f"+++ Processo {pid} inserido no tempo {tempo_atual} +++")
            return pid + 1
        except ValueError:
            print("Erro: Digite apenas números inteiros.")
            return pid

    # ================= SISTEMAS EM LOTE =================

    def menu_lote(self):
        processos = []
        while True:
            print("\n--- MENU SISTEMAS EM LOTE ---")
            print("1. Inserir Processos")
            print("2. Executar FCFS")
            print("3. Executar SJF (Não Preemptivo)")
            print("4. Executar SRTN (Preemptivo)")
            print("5. Limpar Lista")
            print("0. Voltar ao Menu Principal")
            
            op = input("Opção: ")

            if op == '1':
                processos = self.coletar_processos_lote()
            elif op == '2':
                if processos: self.fcfs([p for p in processos]) 
                else: print("Lista vazia!")
            elif op == '3':
                if processos: self.sjf([p for p in processos])
                else: print("Lista vazia!")
            elif op == '4':
                if processos: self.srtn([p for p in processos])
                else: print("Lista vazia!")
            elif op == '5':
                processos = []
                print("Lista limpa.")
            elif op == '0':
                break
            else:
                print("Opção inválida.")

    def coletar_processos_lote(self):
        lista = []
        try:
            n = int(input("Quantos processos deseja inserir? "))
            for i in range(1, n + 1):
                print(f"\nConfigurando Processo P{i}:")
                chegada = int(input("Tempo de Chegada: "))
                surto = int(input("Tempo de Execução (Burst): "))
                lista.append(Processo(i, surto, chegada))
        except ValueError:
            print("Erro: Digite apenas números inteiros.")
        return lista

    def fcfs(self, processos_originais):
        processos = [p for p in processos_originais]
        processos.sort(key=lambda x: x.tempo_chegada)
        for p in processos: p.reset()

        tempo_atual = 0
        finalizados = []

        print("\n--- Execução FCFS ---")
        for p in processos:
            if tempo_atual < p.tempo_chegada:
                tempo_atual = p.tempo_chegada
            
            print(f"Tempo {tempo_atual}: Executando P{p.pid}")
            tempo_atual += p.tempo_total
            self.finalizar_processo(p, tempo_atual, finalizados)

        self.mostrar_estatisticas(finalizados)

    def sjf(self, processos_originais):
        processos = [p for p in processos_originais]
        for p in processos: p.reset()
        
        tempo_atual = 0
        completados = 0
        n = len(processos)
        finalizados = []
        
        print("\n--- Execução SJF ---")
        
        while completados < n:
            disponiveis = [p for p in processos if p.tempo_chegada <= tempo_atual and not p.concluido]
            
            if not disponiveis:
                tempo_atual += 1
                continue
            
            escolhido = min(disponiveis, key=lambda x: x.tempo_total)
            tempo_atual += escolhido.tempo_total
            escolhido.concluido = True
            
            self.finalizar_processo(escolhido, tempo_atual, finalizados)
            completados += 1
            
        self.mostrar_estatisticas(finalizados)

    def srtn(self, processos_originais):
        processos = [p for p in processos_originais]
        for p in processos: p.reset()
        
        tempo_atual = 0
        completados = 0
        n = len(processos)
        finalizados = [] 
        
        print("\n--- Execução SRTN ---")
        
        while completados < n:
            disponiveis = [p for p in processos if p.tempo_chegada <= tempo_atual and p.tempo_restante > 0]
            
            if not disponiveis:
                tempo_atual += 1
                continue
            
            escolhido = min(disponiveis, key=lambda x: x.tempo_restante)
            escolhido.tempo_restante -= 1
            tempo_atual += 1
            
            if escolhido.tempo_restante == 0:
                escolhido.concluido = True
                completados += 1
                self.finalizar_processo(escolhido, tempo_atual, finalizados)
        
        self.mostrar_estatisticas(finalizados)

    # ================= EDF =================

    def real_time(self):
        fila = []
        processos_finalizados = []
        pid = 1
        tempo_atual = 0

        print("\n--- Configuração EDF ---")
        try:
            n = int(input("Quantos processos deseja inserir? "))

            for i in range(n):
                tempo = int(input(f"Tempo de execução do processo {pid}: "))
                prazo = int(input(f"Prazo (deadline) do processo {pid}: "))
                fila.append(Processo(pid, tempo, tempo_atual, deadline=(tempo_atual + prazo)))
                pid += 1

            print("\n--- Iniciando EDF ---\n")

            while len(fila) > 0:
                fila.sort(key=lambda x: x.deadline)

                processo = fila.pop(0)
                processo.tempo_restante -= 1
                tempo_atual += 1

                if processo.tempo_restante > 0:
                    fila.append(processo)
                else:
                    self.finalizar_processo(processo, tempo_atual, processos_finalizados)

            self.mostrar_estatisticas(processos_finalizados)

        except ValueError:
            print("Erro: Digite apenas números inteiros.")

    # ================= AUXILIARES =================

    def finalizar_processo(self, processo, tempo_atual, lista_finalizados):
        processo.tempo_conclusao = tempo_atual
        processo.turnaround = processo.tempo_conclusao - processo.tempo_chegada
        processo.waiting = processo.turnaround - processo.tempo_total
        print(f"*** Processo {processo.pid} FINALIZADO no tempo {tempo_atual} ***")
        if processo not in lista_finalizados:
            lista_finalizados.append(processo)

    def mostrar_estatisticas(self, processos):
        print("\n====== RESULTADO FINAL ======")
        if not processos:
            print("Nenhum processo executado.")
            return

        processos.sort(key=lambda x: x.pid) 
        
        soma_turnaround = 0
        soma_waiting = 0

        for p in processos:
            soma_turnaround += p.turnaround
            soma_waiting += p.waiting

            print(f"\nProcesso {p.pid}")
            print(f"Tempo Total: {p.tempo_total}")
            print(f"Conclusão: {p.tempo_conclusao}")
            print(f"Turnaround: {p.turnaround}")
            print(f"Waiting Time: {p.waiting}")

        print("\n--- MÉDIAS ---")
        print(f"Média Turnaround: {soma_turnaround / len(processos):.2f}")
        print(f"Média Waiting Time: {soma_waiting / len(processos):.2f}")
        print("\nTodos os processos foram finalizados!\n")


if __name__ == "__main__":
    escalonador = Escalonador()
    escalonador.menu()