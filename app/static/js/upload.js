$(document).ready(function() {
    $('#uploadForm').on('submit', function(event) {
        // Limpa mensagens de erro anteriores
        $('#error-message').text('');
        
        // Obtém o arquivo do input
        var fileInput = $('#fileInput')[0];
        var file = fileInput.files[0];
        
        // Verifica se um arquivo foi selecionado
        if (!file) {
            alert('Por favor, selecione um arquivo.'); 
            event.preventDefault();
            return;
        }
        
        // Valida o tamanho do arquivo (100 MB)
        var maxSize = 100 * 1024 * 1024;
        if (file.size > maxSize) {
            alert('O arquivo não pode exceder 100 MB.');
            event.preventDefault();
            return;
        }
        
        // Valida as extensões permitidas
        var validExtensions = ['zip', 'rar'];
        var fileExtension = file.name.split('.').pop().toLowerCase();
        
        if (!validExtensions.includes(fileExtension)) {
            alert('Tipo de arquivo não permitido. Apenas arquivos ZIP, RAR são aceitos.');
            event.preventDefault();
            return;
        }
        
        // Se passar todas as validações, ajusta a URL de ação
        const hostId = $('#hostSelect').val();
        const commandId = $('#commandSelect').val();
        
        // Verifica se os IDs são válidos
        if (hostId === "" || commandId === "") {
            alert('Por favor, selecione um host e um comando válidos.');
            event.preventDefault();
            return;
        }

        this.action = "{% url 'uploader' 0 0 %}".replace('/0/0/', '/' + hostId + '/' + commandId + '/');

        // Mostra o spinner e oculta o formulário
        $('#loadingSpinner').removeClass('d-none');
        this.style.display = 'none';
    });
});