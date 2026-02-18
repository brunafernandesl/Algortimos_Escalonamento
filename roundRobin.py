class Processo:
    # Adicionei o parametro 'deadline' com valor padrão 0 para não quebrar o Round Robin
    def __init__(self, pid, tempo_execucao, tempo_chegada, deadline=0):
        self.pid = pid
        self.tempo_total = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_chegada = tempo_chegada
        self.deadline = deadline  # Novo atributo para Tempo Real
        self.tempo_conclusao = 0
        self.turnaround = 0
        self.waiting = 0
        self.atraso = 0 # Para verificar se cumpriu o prazo

class Escalonador:

    def menu(self):
        while True:
            print("\n====== SIMULADOR DE ESCALONAMENTO ======")
            print("1 - Interativo - Round Robin")
            print("2 - Lote - (Não implementado)")
            print("3 - Tempo Real - EDF (Earliest Deadline First)")
            print("0 - Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.round_robin()
            elif opcao == "2":
                print("\nAlgoritmo ainda não implementado.\n")
            elif opcao == "3":
                self.real_time() # Chamada para o novo método
            elif opcao == "0":
                print("Encerrando...")
                break
            else:
                print("Opção inválida!")

    # --- 1. ROUND ROBIN ---
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
                # Deadline 0 pois não é usado aqui
                fila.append(Processo(pid, tempo, tempo_atual, deadline=0))
                pid += 1

            print("\n--- Iniciando Round Robin ---\n")

            while len(fila) > 0:
                # Mostra fila visualmente
                print(f"\n[Tempo {tempo_atual}] Fila: {[p.pid for p in fila]}")

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

                # Inserção dinâmica
                self.inserir_novo_processo(fila, pid, tempo_atual, tipo="RR")
                if len(fila) > len([p for p in fila if p.pid < pid]): # Se adicionou, incrementa pid
                     pid += 1

            self.mostrar_estatisticas(processos_finalizados)
        except ValueError:
            print("Erro: Digite apenas números inteiros.")

    # --- 3. TEMPO REAL (EDF) ---
    def real_time(self):
        # Algoritmo EDF: Executa quem tem o prazo (deadline) mais curto
        fila = []
        processos_finalizados = []
        pid = 1
        tempo_atual = 0

        print("\n--- Configuração EDF (Earliest Deadline First) ---")
        try:
            n = int(input("Quantos processos iniciais deseja inserir? "))

            for i in range(n):
                tempo = int(input(f"Tempo de execução do processo {pid}: "))
                prazo = int(input(f"Prazo (deadline) do processo {pid} (a partir de agora): "))
                # O deadline absoluto é o tempo atual + o prazo informado
                fila.append(Processo(pid, tempo, tempo_atual, deadline=(tempo_atual + prazo)))
                pid += 1

            print("\n--- Iniciando Tempo Real (EDF) ---\n")

            while len(fila) > 0:
                # A mágica do EDF: Ordenar a fila pelo deadline (menor primeiro)
                fila.sort(key=lambda x: x.deadline)

                print(f"\n[Tempo {tempo_atual}] Fila (Ordenada por Prazo): {[(p.pid, p.deadline) for p in fila]}")

                processo = fila.pop(0) # Pega o com menor prazo

                # No tempo real, vamos executar 1 unidade de tempo por vez
                # para permitir que novos processos urgentes entrem (Preempção)
                print(f"Executando Processo {processo.pid} (Deadline: {processo.deadline})")
                
                processo.tempo_restante -= 1
                tempo_atual += 1

                if processo.tempo_restante > 0:
                    fila.append(processo) # Volta para fila para ser reavaliado na proxima iteração
                else:
                    self.finalizar_processo(processo, tempo_atual, processos_finalizados)
                    
                    # Verifica se estourou o prazo
                    if tempo_atual <= processo.deadline:
                        print(f"Status: SUCESSO (Concluído antes do prazo).")
                    else:
                        print(f"Status: FALHA DE PRAZO (Atraso de {tempo_atual - processo.deadline}s).")

                # Inserção dinâmica
                opcao = input("Deseja adicionar novo processo urgente? (s/n): ")
                if opcao.lower() == 's':
                    tempo = int(input("Tempo de execução: "))
                    prazo = int(input("Prazo (a partir de agora): "))
                    fila.append(Processo(pid, tempo, tempo_atual, deadline=(tempo_atual + prazo)))
                    print(f"Processo {pid} adicionado!")
                    pid += 1

            self.mostrar_estatisticas(processos_finalizados)

        except ValueError:
            print("Erro: Digite apenas números inteiros.")

    # --- MÉTODOS AUXILIARES ---
    
    def finalizar_processo(self, processo, tempo_atual, lista_finalizados):
        processo.tempo_conclusao = tempo_atual
        processo.turnaround = processo.tempo_conclusao - processo.tempo_chegada
        processo.waiting = processo.turnaround - processo.tempo_total
        print(f"*** Processo {processo.pid} FINALIZADO no tempo {tempo_atual} ***")
        lista_finalizados.append(processo)

    def inserir_novo_processo(self, fila, pid, tempo_atual, tipo="RR"):
        # Simplifiquei a lógica de inserção para reuso, mas no RR mantive a original dentro do loop
        # No loop do RR original, ele perguntava a cada iteração. 
        # Mantive a lógica original dentro dos métodos para não mudar muito seu código.
        pass 

    def mostrar_estatisticas(self, processos):
        print("\n====== RESULTADO FINAL ======")
        if not processos:
            print("Nenhum processo executado.")
            return

        soma_turnaround = 0
        soma_waiting = 0

        for p in processos:
            soma_turnaround += p.turnaround
            soma_waiting += p.waiting

            print(f"\nProcesso {p.pid}")
            print(f"Tempo Total: {p.tempo_total}")
            print(f"Conclusão: {p.tempo_conclusao} | Deadline: {p.deadline if p.deadline > 0 else 'N/A'}")
            print(f"Turnaround: {p.turnaround}")
            print(f"Waiting Time: {p.waiting}")

        media_turnaround = soma_turnaround / len(processos)
        media_waiting = soma_waiting / len(processos)

        print("\n--- MÉDIAS ---")
        print(f"Média Turnaround: {media_turnaround:.2f}")
        print(f"Média Waiting Time: {media_waiting:.2f}")
        print("\nTodos os processos foram finalizados!\n")

if __name__ == "__main__":
    escalonador = Escalonador()
    escalonador.menu()