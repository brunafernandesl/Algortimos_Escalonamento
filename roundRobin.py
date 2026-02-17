class Processo:
    def __init__(self, pid, tempo_execucao, tempo_chegada):
        self.pid = pid
        self.tempo_total = tempo_execucao
        self.tempo_restante = tempo_execucao
        self.tempo_chegada = tempo_chegada
        self.tempo_conclusao = 0
        self.turnaround = 0
        self.waiting = 0


class Escalonador:

    def menu(self):
        while True:
            print("\n====== SIMULADOR DE ESCALONAMENTO ======")
            print("1 - Interativo - Round Robin")
            print("2 - Lote - ")
            print("3 - Tempo Real - ")
            print("0 - Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.round_robin()
            elif opcao == "2":
                print("\nAlgoritmo ainda não implementado.\n")
            elif opcao == "3":
                print("\nAlgoritmo ainda não implementado.\n")
            elif opcao == "0":
                print("Encerrando...")
                break
            else:
                print("Opção inválida!")


    # ROUND ROBIN
    def round_robin(self):
        fila = []
        processos_finalizados = []
        pid = 1
        tempo_atual = 0

        quantum = int(input("\nDigite o valor do quantum (em segundos): "))
        n = int(input("Quantos processos iniciais deseja inserir? "))

        # Inserção inicial
        for i in range(n):
            tempo = int(input(f"Tempo de execução do processo {pid}: "))
            fila.append(Processo(pid, tempo, tempo_atual))
            pid += 1

        print("\n--- Iniciando Round Robin ---\n")

        while len(fila) > 0:

            print("\nFila atual: ", [p.pid for p in fila])

            processo = fila.pop(0)

            print(f"\nExecutando Processo {processo.pid}")

            tempo_exec = min(quantum, processo.tempo_restante)

            print(f"Tempo executado: {tempo_exec}")

            processo.tempo_restante -= tempo_exec
            tempo_atual += tempo_exec

            if processo.tempo_restante > 0:
                print(f"Processo {processo.pid} não terminou. Voltando para fila.")
                fila.append(processo)
            else:
                processo.tempo_conclusao = tempo_atual
                processo.turnaround = processo.tempo_conclusao - processo.tempo_chegada
                processo.waiting = processo.turnaround - processo.tempo_total

                print(f"Processo {processo.pid} FINALIZADO no tempo {tempo_atual}")
                processos_finalizados.append(processo)

            # Inserção dinâmica
            opcao = input("\nDeseja adicionar novo processo? (s/n): ")

            if opcao.lower() == 's':
                tempo = int(input("Tempo de execução do novo processo: "))
                fila.append(Processo(pid, tempo, tempo_atual))
                print(f"Processo {pid} adicionado no tempo {tempo_atual}")
                pid += 1

        self.mostrar_estatisticas(processos_finalizados)

    def mostrar_estatisticas(self, processos):
        print("\n====== RESULTADO FINAL ======")

        soma_turnaround = 0
        soma_waiting = 0

        for p in processos:
            soma_turnaround += p.turnaround
            soma_waiting += p.waiting

            print(f"\nProcesso {p.pid}")
            print(f"Tempo Total: {p.tempo_total}")
            print(f"Tempo de Chegada: {p.tempo_chegada}")
            print(f"Tempo de Conclusão: {p.tempo_conclusao}")
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