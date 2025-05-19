import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Configuração do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))

# Configuração do Banco de Dados
# SQLite (desenvolvimento)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aprovatempo.db'

# MySQL (produção)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'aprovatempo')}"

# PostgreSQL (alternativa para produção)
# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'aprovatempo')}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db = SQLAlchemy(app)

# Configuração do Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos de Banco de Dados
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    daily_study_time = db.Column(db.Integer, default=180)  # em minutos
    cronogramas = db.relationship('Cronograma', backref='user', lazy=True)

class Concurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_prova = db.Column(db.DateTime, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    disciplinas = db.relationship('Disciplina', backref='concurso', lazy=True)
    cronogramas = db.relationship('Cronograma', backref='concurso', lazy=True)

class Disciplina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concurso_id = db.Column(db.Integer, db.ForeignKey('concurso.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    peso = db.Column(db.Integer, default=1)
    bloco = db.Column(db.Integer, default=1)
    conteudos = db.relationship('Conteudo', backref='disciplina', lazy=True)

class Conteudo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplina.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    prioridade = db.Column(db.Integer, default=3)  # 1-5
    tempo_estimado = db.Column(db.Integer, default=60)  # em minutos
    cronograma_itens = db.relationship('CronogramaItem', backref='conteudo', lazy=True)

class Cronograma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    concurso_id = db.Column(db.Integer, db.ForeignKey('concurso.id'), nullable=False)
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime, nullable=True)
    tempo_diario = db.Column(db.Integer, default=180)  # em minutos
    ativo = db.Column(db.Boolean, default=True)
    itens = db.relationship('CronogramaItem', backref='cronograma', lazy=True)

class CronogramaItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cronograma_id = db.Column(db.Integer, db.ForeignKey('cronograma.id'), nullable=False)
    conteudo_id = db.Column(db.Integer, db.ForeignKey('conteudo.id'), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    tempo_alocado = db.Column(db.Integer, default=60)  # em minutos
    concluido = db.Column(db.Boolean, default=False)
    nota_desempenho = db.Column(db.Integer, nullable=True)  # opcional, 1-5

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Por favor, verifique suas credenciais e tente novamente.', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=remember)
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email já cadastrado.', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method='sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Aqui buscaríamos os dados do usuário, cronograma ativo e progresso
    return render_template('dashboard.html')

@app.route('/cronograma')
@login_required
def cronograma():
    # Aqui buscaríamos os dados do cronograma ativo do usuário
    return render_template('cronograma.html')

@app.route('/configurar-cronograma', methods=['GET', 'POST'])
@login_required
def configurar_cronograma():
    if request.method == 'POST':
        tempo_diario = int(request.form.get('tempo_diario', 180))
        concurso_id = int(request.form.get('concurso_id', 1))  # Padrão: Agente PF
        data_prova = request.form.get('data_prova')
        
        # Atualizar tempo de estudo do usuário
        current_user.daily_study_time = tempo_diario
        
        # Criar ou atualizar cronograma
        cronograma_ativo = Cronograma.query.filter_by(user_id=current_user.id, ativo=True).first()
        
        if cronograma_ativo:
            cronograma_ativo.tempo_diario = tempo_diario
            cronograma_ativo.concurso_id = concurso_id
            if data_prova:
                cronograma_ativo.data_fim = datetime.strptime(data_prova, '%Y-%m-%d')
        else:
            novo_cronograma = Cronograma(
                user_id=current_user.id,
                concurso_id=concurso_id,
                tempo_diario=tempo_diario
            )
            if data_prova:
                novo_cronograma.data_fim = datetime.strptime(data_prova, '%Y-%m-%d')
            db.session.add(novo_cronograma)
        
        db.session.commit()
        
        # Gerar itens do cronograma
        gerar_cronograma(cronograma_ativo.id if cronograma_ativo else novo_cronograma.id)
        
        flash('Cronograma configurado com sucesso!', 'success')
        return redirect(url_for('cronograma'))
    
    concursos = Concurso.query.filter_by(ativo=True).all()
    return render_template('configurar_cronograma.html', concursos=concursos)

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verificar se o email já existe para outro usuário
        user_check = User.query.filter_by(email=email).first()
        if user_check and user_check.id != current_user.id:
            flash('Este email já está em uso por outro usuário.', 'danger')
            return redirect(url_for('perfil'))
        
        # Atualizar nome e email
        current_user.name = name
        current_user.email = email
        
        # Atualizar senha se fornecida
        if current_password and new_password and confirm_password:
            if not check_password_hash(current_user.password, current_password):
                flash('Senha atual incorreta.', 'danger')
                return redirect(url_for('perfil'))
            
            if new_password != confirm_password:
                flash('As novas senhas não coincidem.', 'danger')
                return redirect(url_for('perfil'))
            
            current_user.password = generate_password_hash(new_password, method='sha256')
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('perfil'))
    
    return render_template('perfil.html')

# Função para gerar cronograma
def gerar_cronograma(cronograma_id):
    cronograma = Cronograma.query.get(cronograma_id)
    if not cronograma:
        return False
    
    # Limpar itens existentes
    CronogramaItem.query.filter_by(cronograma_id=cronograma_id).delete()
    
    # Buscar conteúdos do concurso
    concurso = Concurso.query.get(cronograma.concurso_id)
    disciplinas = Disciplina.query.filter_by(concurso_id=concurso.id).all()
    
    # Definir período do cronograma
    data_inicio = cronograma.data_inicio
    data_fim = cronograma.data_fim or (data_inicio + timedelta(days=90))  # Padrão: 3 meses
    
    # Calcular dias de estudo
    dias_estudo = []
    data_atual = data_inicio
    while data_atual <= data_fim:
        # Considerar apenas dias úteis (seg-sáb)
        if data_atual.weekday() < 6:  # 0-5 = seg-sáb, 6 = dom
            dias_estudo.append(data_atual)
        data_atual += timedelta(days=1)
    
    # Distribuir conteúdos pelos dias
    dia_index = 0
    for disciplina in disciplinas:
        conteudos = Conteudo.query.filter_by(disciplina_id=disciplina.id).order_by(Conteudo.prioridade.desc()).all()
        
        for conteudo in conteudos:
            # Verificar se ainda há dias disponíveis
            if dia_index >= len(dias_estudo):
                dia_index = 0  # Voltar ao início se necessário
            
            # Criar item de cronograma
            item = CronogramaItem(
                cronograma_id=cronograma_id,
                conteudo_id=conteudo.id,
                data=dias_estudo[dia_index],
                tempo_alocado=min(conteudo.tempo_estimado, cronograma.tempo_diario // 2)  # Máximo de metade do tempo diário
            )
            db.session.add(item)
            
            dia_index += 1
    
    db.session.commit()
    return True

# Inicialização do banco de dados e dados iniciais
def init_db():
    with app.app_context():
        db.create_all()
        
        # Verificar se já existem dados
        if Concurso.query.first() is None:
            # Criar concurso da PF
            concurso_pf = Concurso(
                nome="Agente de Polícia Federal",
                descricao="Concurso para o cargo de Agente da Polícia Federal",
                data_prova=datetime(2026, 3, 21),
                ativo=True
            )
            db.session.add(concurso_pf)
            db.session.commit()
            
            # Criar disciplinas
            disciplinas = [
                {"nome": "Língua Portuguesa", "bloco": 1, "peso": 5},
                {"nome": "Noções de Direito Administrativo", "bloco": 1, "peso": 5},
                {"nome": "Noções de Direito Constitucional", "bloco": 1, "peso": 5},
                {"nome": "Noções de Direito Penal e Processual Penal", "bloco": 1, "peso": 5},
                {"nome": "Legislação Especial", "bloco": 1, "peso": 4},
                {"nome": "Estatística", "bloco": 1, "peso": 3},
                {"nome": "Raciocínio Lógico", "bloco": 1, "peso": 4},
                {"nome": "Informática", "bloco": 2, "peso": 4},
                {"nome": "Contabilidade Geral", "bloco": 3, "peso": 3}
            ]
            
            for disc in disciplinas:
                disciplina = Disciplina(
                    concurso_id=concurso_pf.id,
                    nome=disc["nome"],
                    bloco=disc["bloco"],
                    peso=disc["peso"]
                )
                db.session.add(disciplina)
            
            db.session.commit()
            
            # Adicionar alguns conteúdos de exemplo para cada disciplina
            disciplinas_db = Disciplina.query.all()
            
            for disciplina in disciplinas_db:
                # Adicionar 3-5 conteúdos por disciplina
                num_conteudos = min(5, disciplina.peso + 1)
                
                for i in range(num_conteudos):
                    prioridade = 5 - (i % 3)  # Variar prioridade: 5, 4, 3, 5, 4
                    tempo = 45 + (i * 15)  # Variar tempo: 45, 60, 75, 90, 105 minutos
                    
                    conteudo = Conteudo(
                        disciplina_id=disciplina.id,
                        titulo=f"Tópico {i+1} de {disciplina.nome}",
                        descricao=f"Descrição do tópico {i+1} da disciplina {disciplina.nome}",
                        prioridade=prioridade,
                        tempo_estimado=tempo
                    )
                    db.session.add(conteudo)
            
            db.session.commit()
            print("Banco de dados inicializado com dados de exemplo.")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
