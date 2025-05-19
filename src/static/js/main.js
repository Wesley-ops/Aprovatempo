// Funções para o dashboard e cronograma
document.addEventListener('DOMContentLoaded', function() {
    // Manipulação de checkboxes de tarefas
    const taskCheckboxes = document.querySelectorAll('.task-checkbox');
    if (taskCheckboxes.length > 0) {
        taskCheckboxes.forEach(checkbox => {
            checkbox.addEventListener('change', function() {
                const taskId = this.id.replace('task', '');
                const isCompleted = this.checked;
                
                // Atualizar visualmente
                const taskItem = this.closest('.task-item');
                if (isCompleted) {
                    taskItem.style.opacity = '0.6';
                } else {
                    taskItem.style.opacity = '1';
                }
                
                // Enviar para o servidor via AJAX
                updateTaskStatus(taskId, isCompleted);
            });
            
            // Aplicar estilo inicial baseado no estado do checkbox
            if (checkbox.checked) {
                checkbox.closest('.task-item').style.opacity = '0.6';
            }
        });
    }
    
    // Botão para marcar todas as tarefas como concluídas
    const completeAllBtn = document.querySelector('.btn-success');
    if (completeAllBtn) {
        completeAllBtn.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.task-checkbox:not(:checked)');
            checkboxes.forEach(checkbox => {
                checkbox.checked = true;
                checkbox.closest('.task-item').style.opacity = '0.6';
                
                const taskId = checkbox.id.replace('task', '');
                updateTaskStatus(taskId, true);
            });
        });
    }
    
    // Navegação do calendário
    const calendarNavBtns = document.querySelectorAll('.calendar-nav button');
    if (calendarNavBtns.length > 0) {
        calendarNavBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const isNext = this.querySelector('.fa-chevron-right') !== null;
                navigateCalendar(isNext);
            });
        });
    }
    
    // Alternar visualização do calendário (semana/mês)
    const calendarViewBtns = document.querySelectorAll('.card-header .btn-outline, .card-header .btn-primary');
    if (calendarViewBtns.length > 0) {
        calendarViewBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                if (!this.classList.contains('btn-primary')) {
                    document.querySelector('.card-header .btn-primary').classList.remove('btn-primary');
                    document.querySelector('.card-header .btn-primary').classList.add('btn-outline');
                    this.classList.remove('btn-outline');
                    this.classList.add('btn-primary');
                    
                    const isWeekView = this.textContent.trim() === 'Semana';
                    toggleCalendarView(isWeekView);
                }
            });
        });
    }
    
    // Inicializar gráficos se existirem
    if (typeof Chart !== 'undefined' && document.getElementById('progressChart')) {
        initializeCharts();
    }
});

// Função para atualizar o status da tarefa no servidor
function updateTaskStatus(taskId, isCompleted) {
    fetch('/atualizar-tarefa', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            task_id: taskId,
            completed: isCompleted
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualizar estatísticas na página se necessário
            updateProgressStats();
        } else {
            console.error('Erro ao atualizar tarefa:', data.error);
            // Reverter checkbox se houver erro
            const checkbox = document.getElementById('task' + taskId);
            if (checkbox) {
                checkbox.checked = !isCompleted;
                checkbox.closest('.task-item').style.opacity = isCompleted ? '1' : '0.6';
            }
        }
    })
    .catch(error => {
        console.error('Erro na requisição:', error);
    });
}

// Função para navegar no calendário
function navigateCalendar(isNext) {
    const currentMonth = document.querySelector('.calendar-title').textContent;
    
    fetch('/navegar-calendario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            current_month: currentMonth,
            direction: isNext ? 'next' : 'prev'
        })
    })
    .then(response => response.text())
    .then(html => {
        // Substituir o conteúdo do calendário
        document.querySelector('.calendar').outerHTML = html;
        
        // Reattach event listeners
        const newNavBtns = document.querySelectorAll('.calendar-nav button');
        newNavBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const isNext = this.querySelector('.fa-chevron-right') !== null;
                navigateCalendar(isNext);
            });
        });
    })
    .catch(error => {
        console.error('Erro ao navegar no calendário:', error);
    });
}

// Função para alternar visualização do calendário
function toggleCalendarView(isWeekView) {
    fetch('/alternar-visualizacao-calendario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            view_type: isWeekView ? 'week' : 'month'
        })
    })
    .then(response => response.text())
    .then(html => {
        // Substituir o conteúdo do calendário
        document.querySelector('.calendar').outerHTML = html;
        
        // Reattach event listeners
        const newNavBtns = document.querySelectorAll('.calendar-nav button');
        newNavBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const isNext = this.querySelector('.fa-chevron-right') !== null;
                navigateCalendar(isNext);
            });
        });
    })
    .catch(error => {
        console.error('Erro ao alternar visualização do calendário:', error);
    });
}

// Função para atualizar estatísticas de progresso
function updateProgressStats() {
    fetch('/estatisticas-progresso')
    .then(response => response.json())
    .then(data => {
        // Atualizar progresso geral
        const progressFill = document.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.width = data.progresso_geral + '%';
            document.querySelector('.progress-text span:first-child').textContent = data.progresso_geral + '% concluído';
        }
        
        // Atualizar estatísticas
        const statValues = document.querySelectorAll('.stat-value');
        if (statValues.length >= 4) {
            statValues[0].textContent = data.dias_estudo;
            statValues[1].textContent = data.horas_estudadas;
            statValues[2].textContent = data.disciplinas;
            statValues[3].textContent = data.topicos_concluidos;
        }
        
        // Atualizar progresso por disciplina
        const disciplinaProgressos = document.querySelectorAll('.progress-container h4');
        disciplinaProgressos.forEach((elem, index) => {
            const disciplinaNome = elem.textContent.trim();
            const disciplina = data.disciplinas.find(d => d.nome === disciplinaNome);
            
            if (disciplina) {
                const progressBar = elem.nextElementSibling.querySelector('.progress-fill');
                const progressText = elem.nextElementSibling.nextElementSibling.querySelector('span');
                
                progressBar.style.width = disciplina.progresso + '%';
                progressText.textContent = disciplina.progresso + '%';
            }
        });
        
        // Atualizar gráficos se existirem
        if (typeof Chart !== 'undefined' && window.progressChart) {
            updateCharts(data);
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar estatísticas:', error);
    });
}

// Função para inicializar gráficos
function initializeCharts() {
    const ctx = document.getElementById('progressChart').getContext('2d');
    window.progressChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [], // Será preenchido com nomes das disciplinas
            datasets: [{
                label: 'Progresso por Disciplina (%)',
                data: [], // Será preenchido com percentuais de progresso
                backgroundColor: 'rgba(26, 35, 126, 0.7)',
                borderColor: 'rgba(26, 35, 126, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
    
    // Carregar dados iniciais
    updateProgressStats();
}

// Função para atualizar gráficos
function updateCharts(data) {
    if (window.progressChart) {
        window.progressChart.data.labels = data.disciplinas.map(d => d.nome);
        window.progressChart.data.datasets[0].data = data.disciplinas.map(d => d.progresso);
        window.progressChart.update();
    }
}

// Função para obter token CSRF
function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}
