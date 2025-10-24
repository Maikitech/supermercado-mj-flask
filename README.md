# Trabalho Prático: Aplicativo Web - Supermercado MJ

Este projeto é uma aplicação web desenvolvida com Flask e PostgreSQL para gerenciar as operações de um supermercado, incluindo o cadastro de produtos, clientes e a criação de pedidos.

---

## 1. Descrição das Entidades

O sistema foi modelado com as três entidades principais a seguir:

1.  **Product (Produto):** Representa um item à venda no supermercado.
    * **Atributos:** `id` (PK), `name`, `description`, `price`.

2.  **Customer (Cliente):** Representa um cliente cadastrado que realiza compras.
    * **Atributos:** `id` (PK), `name`, `email` (unique).

3.  **Order (Pedido):** Representa uma compra realizada por um cliente, podendo conter múltiplos produtos.
    * **Atributos:** `id` (PK), `order_number` (unique), `customer_id` (FK).

---

## 2. Relacionamentos Implementados e Justificativa das Chaves Estrangeiras

O sistema implementa dois tipos de relacionamentos fundamentais:

### a) Relacionamento 1-para-N: Customer e Order

* **Descrição Lógica:** Um **Cliente** (`Customer`) pode ter vários **Pedidos** (`Orders`), mas um **Pedido** pertence a apenas um **Cliente**.
* **Implementação Técnica:** A tabela `orders` contém uma coluna `customer_id` que é uma **Chave Estrangeira (ForeignKey)**, fazendo referência à chave primária `id` da tabela `customers`.
* **Justificativa da FK:** O uso da chave estrangeira `customer_id` é essencial para garantir a **integridade referencial** do banco de dados. Isso impede a criação de um pedido para um cliente que não existe e previne a exclusão de um cliente que já tenha pedidos associados, evitando que existam "pedidos órfãos" sem um dono no sistema.

### b) Relacionamento N-para-N: Order e Product

* **Descrição Lógica:** Um **Pedido** (`Order`) pode conter vários **Produtos** (`Products`), e um mesmo **Produto** pode estar presente em vários **Pedidos** diferentes.
* **Implementação Técnica:** Para resolver este relacionamento, foi criada uma **tabela associativa** (também conhecida como tabela de junção) chamada `order_product`.
* **Estrutura da Tabela Associativa:**
    * `order_id`: Chave Estrangeira (FK) que referencia `orders.id`.
    * `product_id`: Chave Estrangeira (FK) que referencia `products.id`.
    * A Chave Primária da tabela `order_product` é uma **chave composta** formada por (`order_id`, `product_id`). Isso garante que um mesmo produto não possa ser adicionado mais de uma vez ao mesmo pedido.

---

## 3. Comportamento de Exclusão

Para proteger a integridade dos dados, a aplicação impede a exclusão de registros que estão vinculados a outros:
* Não é possível excluir um **Cliente** se ele possuir **Pedidos** associados.
* Não é possível excluir um **Produto** se ele estiver incluído em algum **Pedido**.
O usuário é notificado com uma mensagem de erro na interface caso tente realizar uma dessas operações.