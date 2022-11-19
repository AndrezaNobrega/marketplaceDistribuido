def vector_compare(vector1,vector2):
    vector = [max(value) for value in zip(vector1,vector2)]
    return vector

#para N processos dados, haverá vetor / matriz de tamanho N.
P = {1:{}, 2:{}, 3:{}} # Temos três processos

inc = 0

n1 = int(input("Insira o número de eventos no processo 1 : "))
e1 = [i for i in range(1, n1 + 1)] #a cada evento é incrementado um ao relógio lógico
P[1] = {key: [inc + key, 0, 0] for key in e1}
print('Processo 1: ', P[1])
print("\n")

n2 = int(input("Insira o número de eventos no processo 2 : "))
e2 = [i for i in range(1, n2 + 1)]
P[2] = {key: [0, inc + key, 0] for key in e2} 
print('Processo 2: ', P[2]) 
print("\n")

n3 = int(input("Número de eventos no processo 3: "))
e3 = [i for i in range(1, n3 + 1)]
P[3] = {key: [0, 0, inc + key] for key in e3}
print('Processo 3: ', P[3])
print("\n")

comm = int(input("Número de envios entre linhas : "))
print("\n")

while inc < comm:
    sent = int(input("Número do proceso que está enviando : ")) # toda vez que um processo envia uma mensagem, 
    #o valor do relógio lógico dos processos no vetor é incrementado por 1.
    recv = int(input("nº do processo que está recebendo : "))
    sent_event_no = int(input("Enter the sending event number : "))
    recv_event_no = int(input("Enter the receiving event number : "))
    if sent <= 3 and recv <= 3:
        print ("P{} --> P{}".format(sent,recv))
        new_vector = vector_compare(P[sent][sent_event_no],P[recv][recv_event_no])
        P[recv][recv_event_no] = new_vector
        print ("New vector value of \"event {}\"  in process P{} is : {} \n".format(recv_event_no,recv,P[recv][recv_event_no]))
        
        # Changing vector for next events.
        if (recv_event_no + 1) in P[recv]:
            for i in range(recv_event_no + 1, len(P[recv]) + 1):
                P[recv][i] = vector_compare(P[recv][i-1],P[recv][i])
    else:
        print ("Enter the sent/recv within existing process")
    inc += 1

print("Final vectors of the 3 process are")
print('Processo 1: ', P[1])
print('Processo 2: ', P[2])
print('Processo 3: ', P[3])