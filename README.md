<p align="center">
 <img width="100px" src="https://icons.veryicon.com/png/o/system/inspur-cloud-icon/distributed-database.png" align="center" alt="GitHub Readme Stats" />
 <h2 align="center">Marketplace distribuído: Protótipo de loja de vendas de camisetas esportivas num estudo de sistemas distribuídos</h2>
 <p align="center">Sistema distribuído de marketplaces que traz a implementação do algortimo de Lamport.</p>
</p>
<p align="center">
<img src="http://img.shields.io/static/v1?label=STATUS&message=Concluido&color=GREEN&style=for-the-badge"/>
</p>

\### requisitos:

- [x] cadastra o produto em apenas um dos marketplaces:
 Há uma tela de cadastro de produtos para cada marketplace, nele é cadastrado diretamente em sua própria base de dados.
 
- [x] Cada marketplace possui sua própria base de dados:
 Cada marketplace possui uma base de dados em JSON. Nele é possível adicionar novos produtos individualmente.

- [x] A loja informa a cada marketplacce os produtos disponíveis:
Foi adotada a solução de que o marketplace possui um arquivo como "galeria", nele, temos listados todos os produtos que estão presentes em todos os bancos de dados da rede 
  dos marketplaces. Portanto, a cada produto que é enviado. As galerias são comunicadas, nisso é add um novo produto nela.

- [x] A loja informa o número disponível no estoque:
  No banco de dados está disponível o número de camisas disponíveis no estoque, bem como, é possível visualizar também na interface web.

- [x] cada marketplace mantem seu próprio servidor:
  O servidor do marketplace foi desenvolvido utilizando o framework flask. 
  
- [ ] realizar transações atômicas:
  Os produtos são adicionados ao carrinho, ele funciona agrupando todos esses produtos. As funções foram implementadas, mas devido à falha no algoritmo implementado, ele não chega a essa etapa.
  - os items podem ter sido cadastrados em qualquer servidor

- [ ] as lojas não devem vender mais produtos do que a quantidade existente:
  Apesar de implementado, o algoritmo não está cumprindo com a sua funcionalidade corretamente, o que acaba fazendo todas as compras serem rejeitadas.

- [x] comunicação entre os servidores: implementada através de um protocolo baseado em uma API Rest flask.

- [x] foi dito em sala que devia ser possível pesquisar um produto:
É pesquisado na "galeria", o que faz com que apareçamm itens de todos os marketplaces.

- [x] Interface web:
Interace desenvolvida utilizando bootstrap.
