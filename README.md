# marketplaceDistribuido

![image](https://user-images.githubusercontent.com/52046375/202006877-30443f0f-20ed-45ba-ad83-81370151e293.png)

- N processos -> lista = n índices 
- Cada processos está em um índice 
- Numa comunicação entre esses, os vetores serão somados
Ex:
 temos c{0, 1, 0} e b {0 , 0, 2}, portanto teremos --> {0, 1, 2}
 
 a cada evento, é incrementado +1 no índice do seu processo, ex:
 
  P1: ------------{1, 0, 0} evento 1 ----------------------------------- {2, 0, 0} evento 2---------


- Só há relação p/ eventos ligados pelo envio de mensagem ou que ocorrem no mesmo nó.
- Não mantem histórico de interação;
- Relação de causalidade;

# Comparação de dois eventos
- Se todos os valores são menores ou iguais aos respectivos valores de B, a precede B
-      a --> b, b é um efeito de a
-       Se alguns valores são maiores e outros menores ou iguais, ñ é possível ordenar

