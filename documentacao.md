# Documentação do ConcursoPrep

## Visão Geral
ConcursoPrep é uma plataforma web responsiva para auxiliar candidatos a concursos públicos, com foco inicial no concurso para Agente da Polícia Federal. A plataforma permite que os usuários criem cronogramas de estudo personalizados com base no tempo disponível e nas disciplinas prioritárias do edital.

## Tecnologias Utilizadas
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento), MySQL (produção)
- **Autenticação**: Flask-Login
- **Hospedagem**: GitHub Pages (frontend), Serviço de hospedagem Python (backend)

## Funcionalidades Principais

### 1. Sistema de Autenticação
- Cadastro de novos usuários
- Login/logout
- Recuperação de senha
- Perfil do usuário com configurações pessoais

### 2. Configuração de Estudo
- Seleção do concurso (inicialmente apenas Agente PF)
- Definição do tempo disponível para estudo diário
- Seleção de prioridades (opcional)
- Data-alvo (data da prova ou prazo pessoal)

### 3. Geração de Cronograma
- Algoritmo que distribui o tempo disponível entre as disciplinas
- Priorização baseada na importância dos conteúdos no edital
- Balanceamento entre disciplinas de diferentes blocos
- Visualização em formato de calendário semanal/mensal

### 4. Dashboard de Acompanhamento
- Visão geral do progresso por disciplina
- Gráficos de desempenho e tempo dedicado
- Lista de tarefas do dia atual
- Histórico de estudos realizados
- Sistema de marcação de progresso manual

## Estrutura do Projeto

```
concurso-pf-site/
├── venv/                      # Ambiente virtual Python
├── src/                       # Código-fonte da aplicação
│   ├── main.py                # Ponto de entrada da aplicação
│   ├── static/                # Arquivos estáticos
│   │   ├── css/               # Folhas de estilo
│   │   │   └── style.css      # Estilo principal
│   │   ├── js/                # Scripts JavaScript
│   │   │   └── main.js        # Script principal
│   │   └── img/               # Imagens
│   └── templates/             # Templates HTML
│       ├── base.html          # Template base
│       ├── index.html         # Página inicial
│       ├── login.html         # Página de login
│       ├── register.html      # Página de cadastro
│       ├── dashboard.html     # Dashboard do usuário
│       ├── cronograma.html    # Visualização do cronograma
│       └── perfil.html        # Perfil do usuário
└── requirements.txt           # Dependências Python
```

## Modelos de Dados

### User (Usuário)
- id: Identificador único
- name: Nome completo
- email: Email (único)
- password: Senha (hash)
- created_at: Data de cadastro
- last_login: Último acesso
- daily_study_time: Tempo diário de estudo (minutos)

### Concurso
- id: Identificador único
- nome: Nome do concurso
- descricao: Descrição
- data_prova: Data da prova
- ativo: Status de ativação

### Disciplina
- id: Identificador único
- concurso_id: Referência ao concurso
- nome: Nome da disciplina
- descricao: Descrição
- peso: Peso/importância (1-5)
- bloco: Bloco do edital

### Conteudo
- id: Identificador único
- disciplina_id: Referência à disciplina
- titulo: Título do conteúdo
- descricao: Descrição
- prioridade: Prioridade (1-5)
- tempo_estimado: Tempo estimado (minutos)

### Cronograma
- id: Identificador único
- user_id: Referência ao usuário
- concurso_id: Referência ao concurso
- data_inicio: Data de início
- data_fim: Data de término
- tempo_diario: Tempo diário (minutos)
- ativo: Status de ativação

### CronogramaItem
- id: Identificador único
- cronograma_id: Referência ao cronograma
- conteudo_id: Referência ao conteúdo
- data: Data programada
- tempo_alocado: Tempo alocado (minutos)
- concluido: Status de conclusão
- nota_desempenho: Nota opcional (1-5)

## Instruções de Instalação e Execução

### Requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)
- Navegador web moderno

### Instalação Local
1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/concurso-pf-site.git
   cd concurso-pf-site
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

4. Execute a aplicação:
   ```
   python src/main.py
   ```

5. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

## Guia de Uso

### Cadastro e Login
1. Acesse a página inicial
2. Clique em "Cadastrar" para criar uma nova conta
3. Preencha seus dados e clique em "Cadastrar"
4. Faça login com seu email e senha

### Configuração do Cronograma
1. Após o login, acesse seu perfil
2. Defina o tempo diário de estudo
3. Selecione o concurso (Agente PF)
4. Defina a data da prova
5. Selecione os dias da semana para estudo
6. Clique em "Atualizar Cronograma"

### Uso do Dashboard
1. Visualize seu progresso geral
2. Acompanhe as estatísticas de estudo
3. Veja o progresso por disciplina
4. Consulte as tarefas do dia

### Uso do Cronograma
1. Navegue pelo calendário mensal ou semanal
2. Visualize as disciplinas programadas para cada dia
3. Marque as tarefas como concluídas
4. Use o botão "Marcar Todos como Concluídos" para finalizar o dia

## Expansão Futura
- Adição de outros concursos
- Sistema de simulados
- Comunidade e recursos compartilhados
- Integração com materiais de estudo
- Personalização por IA
- Gamificação
- Análise avançada de dados
- Modo offline (app)
- Integração com calendários externos
- Assistente virtual de estudos

## Suporte
Para suporte ou dúvidas, entre em contato através do email: suporte@concursoprep.com.br
