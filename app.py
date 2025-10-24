# Y:\FlaskMedabil\web2\app.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from extensions import db
from models import Product, Customer, Order
from sqlalchemy.exc import IntegrityError

web2_bp = Blueprint('web2', __name__, template_folder='templates')

@web2_bp.route('/')
def index():
    return render_template('index.html')

# --- Rotas para Produtos ---
# (As rotas de produtos estão corretas)
@web2_bp.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@web2_bp.route('/create_product', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        # ... (código existente)
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        new_product = Product(name=name, description=description, price=price)
        db.session.add(new_product)
        db.session.commit()
        flash(f'Produto "{new_product.name}" criado com sucesso!', 'success')
        return redirect(url_for('web2.products'))
    return render_template('create_product.html')

@web2_bp.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    product = Product.query.get_or_44(id)
    if request.method == 'POST':
        # ... (código existente)
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        db.session.commit()
        flash(f'Produto "{product.name}" atualizado com sucesso!', 'success')
        return redirect(url_for('web2.products'))
    return render_template('update_product.html', product=product)

@web2_bp.route('/delete_product/<int:id>')
def delete_product(id):
    # ... (código existente)
    product = Product.query.get_or_404(id)
    if product.orders:
        flash(f'O produto "{product.name}" não pode ser excluído, pois está associado a um ou mais pedidos.', 'danger')
        return redirect(url_for('web2.products'))
    db.session.delete(product)
    db.session.commit()
    flash(f'Produto "{product.name}" excluído com sucesso!', 'success')
    return redirect(url_for('web2.products'))


# --- Rotas para Clientes ---
# (As rotas de clientes estão corretas)
@web2_bp.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@web2_bp.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        try:
            # ... (código existente)
            name = request.form['name']
            email = request.form['email']
            new_customer = Customer(name=name, email=email)
            db.session.add(new_customer)
            db.session.commit()
            flash(f'Cliente "{new_customer.name}" criado com sucesso!', 'success')
            return redirect(url_for('web2.customers'))
        except IntegrityError:
            db.session.rollback()
            flash('ERRO: O email fornecido já está cadastrado.', 'danger')
            return render_template('create_customer.html')
    return render_template('create_customer.html')

@web2_bp.route('/update_customer/<int:id>', methods=['GET', 'POST'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        try:
            # ... (código existente)
            customer.name = request.form['name']
            customer.email = request.form['email']
            db.session.commit()
            flash(f'Cliente "{customer.name}" atualizado com sucesso!', 'success')
            return redirect(url_for('web2.customers'))
        except IntegrityError:
            db.session.rollback()
            flash('ERRO: O email fornecido já pertence a outro cliente.', 'danger')
            return render_template('update_customer.html', customer=customer)
    return render_template('update_customer.html', customer=customer)

@web2_bp.route('/delete_customer/<int:id>')
def delete_customer(id):
    # ... (código existente)
    customer = Customer.query.get_or_404(id)
    if customer.orders:
        flash(f'O cliente "{customer.name}" não pode ser excluído, pois possui pedidos associados.', 'danger')
        return redirect(url_for('web2.customers'))
    db.session.delete(customer)
    db.session.commit()
    flash(f'Cliente "{customer.name}" excluído com sucesso!', 'success')
    return redirect(url_for('web2.customers'))


# --- Rotas para Pedidos ---
@web2_bp.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

@web2_bp.route('/create_order', methods=['GET', 'POST'])
def create_order():
    # O bloco try agora começa antes mesmo de ler o formulário
    try:
        if request.method == 'POST':
            order_number = request.form.get('order_number')
            customer_id_str = request.form.get('customer') # Usamos .get() que é mais seguro
            products_ids = request.form.getlist('products')

            # Validação: Verifica se os campos essenciais foram preenchidos
            if not order_number or not customer_id_str or not products_ids:
                flash('ERRO: Todos os campos são obrigatórios. Por favor, preencha o número do pedido, selecione um cliente e pelo menos um produto.', 'danger')
                # Recarrega a página com os dados para o usuário não perder o que já preencheu
                customers = Customer.query.all()
                products = Product.query.all()
                return render_template('create_order.html', customers=customers, products=products)

            # Conversão segura para número
            customer_id = int(customer_id_str)

            # Lógica de criação do pedido
            new_order = Order(order_number=order_number, customer_id=customer_id)
            for product_id in products_ids:
                product = Product.query.get(product_id)
                if product:
                    new_order.products.append(product)
            
            db.session.add(new_order)
            db.session.commit()
            flash(f'Pedido nº "{new_order.order_number}" criado com sucesso!', 'success')
            return redirect(url_for('web2.orders'))

    except IntegrityError:
        db.session.rollback()
        flash('ERRO: O número do pedido já existe. Por favor, use um número diferente.', 'danger')
    
    # ESTE É O BLOCO MAIS IMPORTANTE: ele captura QUALQUER outro erro
    except Exception as e:
        db.session.rollback()
        # Mostra na tela qual foi o erro exato que aconteceu!
        flash(f'Ocorreu um erro inesperado: {e}', 'danger')

    # Este bloco executa tanto para a primeira visita (GET) quanto se ocorrer um erro
    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('create_order.html', customers=customers, products=products)

    # Este bloco executa tanto para GET quanto se o TRY falhar
    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('create_order.html', customers=customers, products=products)


@web2_bp.route('/update_order/<int:id>', methods=['GET', 'POST'])
def update_order(id):
    order = Order.query.get_or_404(id)
    if request.method == 'POST':
        try:
            order.order_number = request.form['order_number']
            # ✅ CORREÇÃO APLICADA AQUI TAMBÉM
            order.customer_id = int(request.form['customer']) 
            order.products.clear()
            
            products_ids = request.form.getlist('products')
            for product_id in products_ids:
                product = Product.query.get(product_id)
                if product:
                    order.products.append(product)
            
            db.session.commit()
            flash(f'Pedido nº "{order.order_number}" atualizado com sucesso!', 'success')
            return redirect(url_for('web2.orders'))
        except IntegrityError:
            db.session.rollback()
            flash('ERRO: O número do pedido fornecido já pertence a outro pedido.', 'danger')
        except (ValueError, TypeError):
            db.session.rollback()
            flash('ERRO: Dados inválidos recebidos do formulário.', 'danger')

    # Carrega os dados para a página de edição
    customers = Customer.query.all()
    products = Product.query.all()
    return render_template('update_order.html', order=order, customers=customers, products=products)


@web2_bp.route('/delete_order/<int:id>')
def delete_order(id):
    order = Order.query.get_or_404(id)
    order_num = order.order_number
    db.session.delete(order)
    db.session.commit()
    flash(f'Pedido nº "{order_num}" excluído com sucesso!', 'success')
    return redirect(url_for('web2.orders'))