# marketplaceDistribuido

\### requisitos:

- [x] cadastra o produto em apenas um dos marketplaces
 há uma tela de cadastro de produtos para cada marketplace, nele é cadastrado diretamente em sua própria base de dados.
 
- [x] Cada marketplace possui sua própria base de dados 
 cada marketplace possui uma base de dados em JSON. Nele é possível adicionar novos produtos individualmente.

- [ ] A loja informa a cada marketplacce os produtos disponíveis 
Foi adotada a solução de que o marketplace possui um arquivo como "galeria", nele, temos listados todos os produtos que estão presentes em todos os bancos de dados da rede 
  dos marketplaces. Portanto, a cada produto que é enviado. As galerias são comunicadas, nisso é add um novo produto nela.

- [x] A loja informa o número disponível no estoque
  No banco de dados está disponível o número de camisas disponíveis no estoque, bem como, é possível visualizar também na interface web.

- [x] cada marketplace mantem seu próprio servidor
  O servidor do marketplace foi desenvolvido utilizando o framework flask. 
  
- [ ] realizar transações atômicas:
  Os produtos são adicionados ao carrinho, ele funciona agrupando todos esses produtos. 
  - os items podem ter sido cadastrados em qualquer servidor

- [ ] as lojas não devem vender mais produtos do que a quantidade existente

- [ ] comunicação entre os servidores: implementada através de um protocolo baseado em uma API Rest

- [x] foi dito em sala que devia ser possível pesquisar um produto

- [x] Interface web
