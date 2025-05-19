# Estrutura e Funcionalidades do Site de Estudos para Concursos

## Visão Geral
O site será uma plataforma responsiva para auxiliar candidatos a concursos públicos, com foco inicial no concurso para Agente da Polícia Federal. A plataforma permitirá que os usuários criem cronogramas de estudo personalizados com base no tempo disponível e nas disciplinas prioritárias do edital.

## Tecnologias Escolhidas
- **Framework Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap para responsividade
- **Banco de Dados**: SQLite para desenvolvimento, MySQL para produção
- **Hospedagem**: GitHub Pages para frontend, com backend hospedado em serviço adequado
- **Controle de Versão**: Git/GitHub

## Estrutura do Banco de Dados

### Tabelas Principais:
1. **Usuários**
   - id (PK)
   - nome
   - email
   - senha (hash)
   - data_cadastro
   - ultimo_acesso
   - tempo_estudo_diario (minutos)

2. **Concursos**
   - id (PK)
   - nome
   - descricao
   - data_prova
   - ativo (boolean)

3. **Disciplinas**
   - id (PK)
   - concurso_id (FK)
   - nome
   - descricao
   - peso
   - bloco

4. **Conteúdos**
   - id (PK)
   - disciplina_id (FK)
   - titulo
   - descricao
   - prioridade (1-5)
   - tempo_estimado (minutos)

5. **Cronogramas**
   - id (PK)
   - usuario_id (FK)
   - concurso_id (FK)
   - data_inicio
   - data_fim
   - tempo_diario (minutos)
   - ativo (boolean)

6. **CronogramaItens**
   - id (PK)
   - cronograma_id (FK)
   - conteudo_id (FK)
   - data
   - tempo_alocado (minutos)
   - concluido (boolean)
   - nota_desempenho (opcional)

## Funcionalidades Principais

### 1. Sistema de Autenticação
- Cadastro de novos usuários
- Login/logout
- Recuperação de senha
- Perfil do usuário com configurações pessoais

### 2. Configuração de Estudo
- Seleção do concurso (inicialmente apenas Agente PF, com estrutura para expansão)
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

### 5. Recursos Adicionais
- Exportação do cronograma em PDF/CSV
- Notificações por email (opcional para futuro)
- Compartilhamento de cronograma (opcional para futuro)

## Expansibilidade

### Preparação para Outros Concursos
- Estrutura de banco de dados já preparada para múltiplos concursos
- Interface administrativa para adicionar novos concursos (futuro)
- Sistema de importação de editais (futuro)

### Potencial para Aplicativo Móvel
- API RESTful para comunicação com futuro aplicativo
- Design responsivo como base para interface móvel
- Armazenamento de dados críticos para funcionamento offline

## Sugestões de Funcionalidades Futuras

1. **Sistema de Simulados**
   - Banco de questões por disciplina
   - Geração de simulados personalizados
   - Análise de desempenho por área

2. **Comunidade e Recursos Compartilhados**
   - Fórum de discussão por disciplina
   - Compartilhamento de materiais de estudo
   - Grupos de estudo virtuais

3. **Integração com Materiais de Estudo**
   - Recomendação de livros e cursos
   - Links para videoaulas por tópico
   - Resumos colaborativos

4. **Inteligência Artificial para Personalização**
   - Ajuste automático do cronograma baseado no desempenho
   - Recomendações personalizadas de estudo
   - Previsão de desempenho

5. **Gamificação**
   - Sistema de pontos e recompensas
   - Conquistas por metas atingidas
   - Competições amigáveis entre usuários

6. **Análise Avançada de Dados**
   - Estatísticas detalhadas de desempenho
   - Identificação de pontos fracos
   - Relatórios periódicos de progresso

7. **Modo Offline Completo (App)**
   - Sincronização automática quando online
   - Acesso a todos os recursos sem conexão
   - Notificações push para lembretes

8. **Integração com Calendários Externos**
   - Google Calendar, Outlook, etc.
   - Sincronização bidirecional de eventos

9. **Assistente Virtual de Estudos**
   - Chatbot para dúvidas sobre o cronograma
   - Lembretes e motivação personalizada
   - Sugestões de técnicas de estudo

10. **Monitoramento de Editais e Notícias**
    - Alertas sobre alterações em editais
    - Notícias relevantes sobre o concurso
    - Atualizações automáticas de conteúdo
