from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
app = Flask(__name__)
app.secret_key = ('chave secreta para os nao uçar')

tutores = []
pets = []
consultas = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dadospets')
def dadospets():
    return render_template('dadospets.html', pets=pets)


@app.route('/dadosconsultas', methods=['GET', 'POST'])
def dadosconsultas():
    return render_template('dadosconsultas.html', consultas=consultas)


@app.route('/dadostutor', methods=['GET', 'POST'])
def dadostutor():
    return render_template('dadostutor.html', tutores=tutores)



@app.route('/cadastrartutor', methods=['GET', 'POST'])
def cadastrartutor():
    if request.method == 'POST':
        nome = request.form.get('nomeTutor')
        telefone = request.form.get('telefoneTutor')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = (request
                           .form.get('confirmaSenha'))
        id = len(tutores)
        if confirmar_senha != senha:
            flash("As senhas não coincidem!", 'danger')
            return redirect(url_for('cadastrartutor'))

        maiuscula = any(c.isupper() for c in senha)
        minuscula = any(c.islower() for c in senha)
        numero = any(c.isdigit() for c in senha)
        especial = any(not c.isalnum() for c in senha)

        if not (maiuscula and minuscula and numero and especial):
            flash("A senha deve ter pelo menos uma letra maiúscula, minúscula, número e caractere especial.", 'danger')
            return redirect(url_for('cadastrartutor'))

        tutores.append({
            'id': id,
            'nome': nome,
            'telefone': telefone,
            'email': email,
            'senha': senha
        })

        flash('Tutor cadastrado com sucesso!', 'success')
        return redirect(url_for('login'))

    return render_template('cadastrartutor.html')


@app.route('/editarusuario/<int:id>', methods=['GET', 'POST'])
def editarusuario(id):
    if 0 <= id < len(tutores):
        if request.method == 'POST':
            tutores[id]['nome'] = request.form['nome']
            tutores[id]['telefone'] = request.form['telefone']
            tutores[id]['email'] = request.form['email']
            tutores[id]['senha'] = request.form['senha']

            flash('Dados do Usuário atualizados com sucesso!', 'success')
            return redirect(url_for('dadostutor'))

        return render_template('editarusuario.html', tutor=tutores[id], id=id)

    flash('Usuário não encontrado!', 'danger')
    return redirect(url_for('dadostutor'))


@app.route('/excluir_tutor/<int:id>')
def excluir_tutor(id):
    if 0 <= id < len(tutores):
        tutores.pop(id)
        flash('Usuário excluído com sucesso!', 'success')
    else:
        flash('Usuário não encontrado!', 'danger')
    return redirect(url_for('dadostutor'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        for tutor in tutores:
            if tutor['email'] == email and tutor['senha'] == senha:
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('dadostutor'))

        flash('Email ou senha incorretos!', 'danger')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/cadastrarpet', methods=['GET', 'POST'])
def cadastrarpet():
    if request.method == 'POST':
        id = len(pets)
        nome_pet = request.form['nome_pet']
        raca_pet = request.form['raca_pet']
        peso_pet = request.form['peso_pet']
        genero = request.form['genero']
        nome_tutor = request.form['nome_tutor']
        telefone_tutor = request.form['telefone_tutor']

        pets.append({
            'id': id,
            'nome_pet': nome_pet,
            'raca_pet': raca_pet,
            'peso_pet': peso_pet,
            'genero': genero,
            'nome_tutor': nome_tutor,
            'telefone_tutor': telefone_tutor
        })

        flash('Pet cadastrado com sucesso!', 'success')
        return redirect(url_for('dadospets'))

    return render_template('cadastrarpet.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 0 <= id < len(pets):
        if request.method == 'POST':
            pets[id]['nome_pet'] = request.form['nome']
            pets[id]['raca_pet'] = request.form['raca']
            pets[id]['peso_pet'] = request.form['peso']
            pets[id]['genero'] = request.form.get('sexo', '')
            flash('Dados do pet atualizados com sucesso!', 'success')
            return redirect(url_for('dadospets'))

        return render_template('editarpet.html', pet=pets[id], id=id)

    flash('Pet não encontrado!', 'danger')
    return redirect(url_for('dadospets'))


@app.route('/excluir/<int:id>')
def excluir(id):
    if 0 <= id < len(pets):
        pets.pop(id)
        flash('Pet excluído com sucesso!', 'success')
    else:
        flash('Pet não encontrado!', 'danger')
    return redirect(url_for('dadospets'))

@app.route('/agendamento', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        id = len(consultas)
        nome = request.form['nome']
        celular = request.form['celular']
        email = request.form['email']
        especie = request.form['especie']
        data_hora = request.form['data_hora']  # já vem no formato certo!
        nome_pet = request.form['nome_pet']

        consulta = {
            'id': id,
            'nome': nome,
            'celular': celular,
            'email': email,
            'especie': especie,
            'data_hora': data_hora,  # mantém no formato ISO
            'nome_pet': nome_pet
        }

        consultas.append(consulta)

        flash('Consulta agendada com sucesso!', 'success')
        return redirect(url_for('dadosconsultas'))

    return render_template('agendamento.html')



@app.route('/editar_agendamento/<int:id>', methods=['GET', 'POST'])
def editar_agendamento(id):
    if 0 <= id < len(consultas):
        consulta = consultas[id]

        if request.method == 'POST':
            consulta['nome'] = request.form['nome']
            consulta['celular'] = request.form['celular']
            consulta['email'] = request.form['email']
            consulta['especie'] = request.form['especie']
            consulta['data_hora'] = request.form['data_hora']  # já vem formatada corretamente
            consulta['nome_pet'] = request.form['nome_pet']

            flash('Agendamento atualizado com sucesso!', 'success')
            return redirect(url_for('dadosconsultas'))

        return render_template('editar.html', consulta=consulta, id=id)

    flash('Agendamento não encontrado!', 'danger')
    return redirect(url_for('dadosconsultas'))


@app.route('/excluir_agenda/<int:id>')
def excluir_agenda(id):
    if 0 <= id < len(consultas):
        consultas.pop(id)
        flash('Consulta exluida com sucesso!', 'success')
    else:
        flash('Consulta não encontrada!', 'danger')
    return redirect(url_for('dadosconsultas'))

@app.route('/calcularsoro', methods=['GET', 'POST'])
def calcularsoro():
    total = None
    if request.method == 'POST':
        nivel_soro = {
            'Leve' : 50,
            'Moderada': 75,
            'Grave': 100,
        }
        try:
            peso = float(request.form['peso'])
            quantidade = request.form['quantidade']
            if quantidade in nivel_soro:
                resultado = nivel_soro[quantidade] * peso
            total = (f"Quantidade de soro necessária: {resultado:.2f}ml")
        except ValueError:
            flash('Insira apenas números válidos.', 'danger')

    return render_template('calcularsoro.html', total=total)


@app.route('/calcularmedicamento', methods=['GET', 'POST'])
def calcularmedicamento():
    resultado = None
    if request.method == 'POST':
            peso = float(request.form['peso'])
            quantidades = float(request.form['quantidades'])

            if peso == '' or quantidades == '':
                flash("Erro: Preencha todos os campos.")

            elif float(peso) <= 0 or float(quantidades) <= 0:
                flash("Erro: Peso e quantidade devem ser maiores que zero.")

            else:
                total = float(peso) * float(quantidades)
                flash(f"Dosagem recomendada: {total:.2f}mg ")

    return render_template('calcularmedicamento.html', resultado=resultado)


if __name__ == '__main__':
    app.run(debug=True)
