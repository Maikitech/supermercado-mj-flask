# supermercado-mj-flask
Sistema de gestão para supermercado (produtos, clientes e pedidos) desenvolvido com Flask, SQLAlchemy e PostgreSQL.


# Sistema de Gestão de Supermercado - Supermercado MJ

<p align="center">
  <img src="https://img.shields.io/badge/status-concluído-green.svg" alt="Status do Projeto: Concluído">
</p>

Este projeto é uma aplicação web completa desenvolvida para o trabalho prático da disciplina, utilizando Flask para o back-end e PostgreSQL para o banco de dados. A aplicação simula um sistema de gestão para um supermercado, permitindo o controle de produtos, clientes e pedidos.

---

## 🚀 Funcionalidades Principais

* **Gestão de Produtos:** CRUD completo (Criar, Ler, Atualizar, Deletar) para os produtos do supermercado.
* **Gestão de Clientes:** CRUD completo para a base de clientes. O sistema impede a criação de clientes com e-mails duplicados.
* **Gestão de Pedidos:** Sistema de criação e gerenciamento de pedidos, implementando os relacionamentos:
    * **1-para-N:** Cada pedido está associado a um único cliente.
    * **N-para-N:** Um pedido pode conter múltiplos produtos.
* **Interface Moderna:** Layout responsivo e amigável desenvolvido com Bootstrap, com feedback visual (mensagens de sucesso e erro) para todas as ações do usuário.
* **Regras de Negócio:**
    * Impede a exclusão de clientes ou produtos que já possuam pedidos vinculados.
    * Valida a unicidade de dados críticos como o e-mail do cliente e o número do pedido.

---

## 🛠️ Tecnologias Utilizadas

* **Back-end:** Python, Flask, Flask-SQLAlchemy
* **Banco de Dados:** PostgreSQL
* **Driver do Banco:** psycopg2-binary
* **Migrações de Banco:** Flask-Migrate (Alembic)
* **Front-end:** HTML5, CSS3, Bootstrap 5
* **Servidor de Produção:** IIS com wfastcgi

---

## 📂 Estrutura do Banco de Dados

O sistema foi modelado com três entidades principais (`Customer`, `Product`, `Order`) e uma tabela associativa (`order_product`) para gerenciar o relacionamento N-para-N.


<img width="1250" height="280" alt="READMEPNG" src="https://github.com/user-attachments/assets/9bd53a50-8e04-4973-96a2-883c176c7919" />

![Diagrama ER do Banco de Dados](nome_da_sua_imagem.png)

---

## ⚙️ Como Executar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Use o arquivo `.env.example` como modelo para preencher suas credenciais:
        ```env
        FLASK_APP=app.py
        FLASK_ENV=development
        DATABASE_URL="postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO"
        SECRET_KEY="sua-chave-secreta-aqui"
        ```

5.  **Aplique as migrações do banco de dados:**
    ```bash
    flask db upgrade
    ```

6.  **Execute a aplicação:**
    ```bash
    flask run
    ```

---

## 👨‍💻 Autor

* **Maiki Scolivi**
