# Aprovatempo

![Logo Aprovatempo](/src/static/img/logo.png)

## Sobre o Projeto

Aprovatempo é uma plataforma web responsiva para auxiliar candidatos a concursos públicos, com foco inicial no concurso para Agente da Polícia Federal. A plataforma permite que os usuários criem cronogramas de estudo personalizados com base no tempo disponível e nas disciplinas prioritárias do edital.

## Funcionalidades Principais

- **Sistema de Autenticação**: Cadastro, login e gerenciamento de perfil
- **Cronograma Personalizado**: Geração automática baseada no tempo disponível e prioridades do edital
- **Dashboard Interativo**: Acompanhamento visual do progresso de estudos
- **Calendário de Estudos**: Visualização semanal e mensal das tarefas
- **Marcação de Progresso**: Sistema para registrar atividades concluídas
- **Design Responsivo**: Funciona em dispositivos móveis e desktop

## Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: MySQL/PostgreSQL
- **Autenticação**: Flask-Login
- **Hospedagem**: Serviços de hospedagem Python (Heroku, PythonAnywhere, etc.)

## Instalação e Configuração

### Requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- MySQL ou PostgreSQL

### Instalação Local

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/aprovatempo.git
   cd aprovatempo
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente para o banco de dados:
   ```
   export DB_USERNAME=seu_usuario
   export DB_PASSWORD=sua_senha
   export DB_HOST=seu_host
   export DB_PORT=3306
   export DB_NAME=aprovatempo
   ```

5. Execute a aplicação:
   ```
   python src/main.py
   ```

6. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

## Configuração do Banco de Dados

### MySQL

1. Crie um banco de dados MySQL:
   ```sql
   CREATE DATABASE aprovatempo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. Crie um usuário e conceda privilégios:
   ```sql
   CREATE USER 'aprovatempo_user'@'localhost' IDENTIFIED BY 'sua_senha';
   GRANT ALL PRIVILEGES ON aprovatempo.* TO 'aprovatempo_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. Descomente e configure a linha de conexão MySQL no arquivo `src/main.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'aprovatempo')}"
   ```

### PostgreSQL

1. Crie um banco de dados PostgreSQL:
   ```sql
   CREATE DATABASE aprovatempo;
   ```

2. Crie um usuário e conceda privilégios:
   ```sql
   CREATE USER aprovatempo_user WITH PASSWORD 'sua_senha';
   GRANT ALL PRIVILEGES ON DATABASE aprovatempo TO aprovatempo_user;
   ```

3. Configure a conexão PostgreSQL no arquivo `src/main.py`:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USERNAME', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'aprovatempo')}"
   ```

## Deploy em Produção

### Heroku

1. Crie um arquivo `Procfile` na raiz do projeto:
   ```
   web: gunicorn --chdir src main:app
   ```

2. Adicione o gunicorn às dependências:
   ```
   pip install gunicorn
   pip freeze > requirements.txt
   ```

3. Configure as variáveis de ambiente no Heroku:
   ```
   heroku config:set DB_USERNAME=seu_usuario
   heroku config:set DB_PASSWORD=sua_senha
   heroku config:set DB_HOST=seu_host
   heroku config:set DB_PORT=3306
   heroku config:set DB_NAME=aprovatempo
   ```

4. Faça o deploy:
   ```
   git push heroku main
   ```

### PythonAnywhere

1. Crie uma conta no PythonAnywhere
2. Configure um Web App com Flask
3. Configure as variáveis de ambiente
4. Configure o banco de dados MySQL (disponível no PythonAnywhere)
5. Faça upload do código via Git ou manualmente

## Estrutura do Projeto

```
aprovatempo/
├── venv/                      # Ambiente virtual Python
├── src/                       # Código-fonte da aplicação
│   ├── main.py                # Ponto de entrada da aplicação
│   ├── static/                # Arquivos estáticos
│   │   ├── css/               # Folhas de estilo
│   │   │   └── style.css      # Estilo principal
│   │   ├── js/                # Scripts JavaScript
│   │   │   └── main.js        # Script principal
│   │   └── img/               # Imagens
│   │       └── logo.png       # Logo do Aprovatempo
│   └── templates/             # Templates HTML
│       ├── base.html          # Template base
│       ├── index.html         # Página inicial
│       ├── login.html         # Página de login
│       ├── register.html      # Página de cadastro
│       ├── dashboard.html     # Dashboard do usuário
│       ├── cronograma.html    # Visualização do cronograma
│       └── perfil.html        # Perfil do usuário
├── .gitignore                 # Arquivos ignorados pelo Git
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
└── documentacao.md            # Documentação detalhada
```

## Expansão Futura

- Adição de outros concursos
- Sistema de simulados
- Comunidade e recursos compartilhados
- Integração com materiais de estudo
- Personalização por IA
- Gamificação
- Análise avançada de dados
- Aplicativo móvel
- Integração com calendários externos
- Assistente virtual de estudos

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

## Contato

Para suporte ou dúvidas, entre em contato através do email: contato@aprovatempo.com.br
