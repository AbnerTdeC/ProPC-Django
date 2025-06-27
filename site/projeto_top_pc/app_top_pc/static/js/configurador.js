function filtrarProdutos(categoria, termoPesquisa) {
    const select = document.querySelector(`select[data-categoria="${categoria}"]`);
    const options = select.querySelectorAll('option');
    
    termoPesquisa = termoPesquisa.toLowerCase().trim();
    
    let opcoesVisiveis = [];
    let primeiraOpcaoVisivel = null;
    
    options.forEach(option => {
        if (option.value === '') {
            option.style.display = ''; // Sempre mostra "Selecione um..."
            return;
        }
        
        const texto = option.textContent.toLowerCase();
        if (termoPesquisa === '' || texto.includes(termoPesquisa)) {
            option.style.display = '';
            opcoesVisiveis.push(option);
            if (!primeiraOpcaoVisivel) {
                primeiraOpcaoVisivel = option;
            }
        } else {
            option.style.display = 'none';
        }
    });
    
    // Se houver apenas uma opção visível e há termo de pesquisa, seleciona automaticamente
    if (termoPesquisa !== '' && opcoesVisiveis.length === 1) {
        select.value = primeiraOpcaoVisivel.value;
        // Dispara evento de mudança para atualizar a interface
        select.dispatchEvent(new Event('change'));
    }
    
    // Se não há termo de pesquisa, limpa a seleção
    if (termoPesquisa === '') {
        select.value = '';
    }
    
    // Atualiza o contador de produtos visíveis
    atualizarContador(categoria, opcoesVisiveis.length);
}

function atualizarContador(categoria, quantidade) {
    const label = document.querySelector(`label[for*="${categoria}"]`);
    if (label) {
        const span = label.querySelector('span');
        if (span) {
            span.textContent = `(${quantidade} produtos ${quantidade === 1 ? 'encontrado' : 'encontrados'})`;
        }
    }
}

// Adiciona funcionalidade de seleção rápida com Enter
function adicionarEventosRapidos() {
    const inputs = document.querySelectorAll('input[id^="pesquisa_"]');
    
    inputs.forEach(input => {
        const categoria = input.id.replace('pesquisa_', '');
        const select = document.querySelector(`select[data-categoria="${categoria}"]`);
        
input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        
        // Encontra a primeira opção visível que não seja "Selecione um..."
        const opcoesVisiveis = Array.from(select.querySelectorAll('option'))
            .filter(option => option.value !== '' && option.style.display !== 'none');
        
        if (opcoesVisiveis.length > 0) {
            select.value = opcoesVisiveis[0].value;
            select.dispatchEvent(new Event('input')); // Dispara evento input para atualizar UI
            select.dispatchEvent(new Event('change')); // Dispara evento change para backend
            
            // Limpa o campo de pesquisa e mostra todas as opções
            input.value = '';
            filtrarProdutos(categoria, '');
        }
    }
    
    if (e.key === 'Escape') {
        // Limpa a pesquisa
        input.value = '';
        filtrarProdutos(categoria, '');
    }
});
        
        // Adiciona placeholder dinâmico
        input.addEventListener('focus', function() {
            this.placeholder = `Digite para pesquisar ou pressione Enter para selecionar...`;
        });
        
        input.addEventListener('blur', function() {
            this.placeholder = `Pesquisar ${categoria.charAt(0).toUpperCase() + categoria.slice(1)}...`;
        });
    });
}

// Adiciona estilo para melhorar a aparência
document.addEventListener('DOMContentLoaded', function() {
    const style = document.createElement('style');
    style.textContent = `
        option[style*="display: none"] {
            display: none !important;
        }
        
        input[id^="pesquisa_"]:focus {
            border-color: #3498db;
            box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
        }
        
        select[data-categoria] {
            transition: border-color 0.3s ease;
        }
        
        select[data-categoria]:focus {
            border-color: #3498db;
            box-shadow: 0 0 5px rgba(52, 152, 219, 0.3);
        }
    `;
    document.head.appendChild(style);
    
    // Inicializa eventos rápidos
    adicionarEventosRapidos();
});
