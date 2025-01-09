
# Telegram DoS Bot

## Descrição
Este é um bot para o Telegram projetado para realizar **testes de segurança** (pentest) em sistemas controlados. Ele simula um ataque DoS (Denial of Service) e permite a personalização do tipo de ataque, número de requisições, threads, uso de agentes falsos, e mais. O bot foi criado com a ajuda de **inteligência artificial** para facilitar o desenvolvimento e otimizar a lógica do ataque.

⚠️ **Importante**: O uso deste bot em sistemas sem permissão é **ilegal** e pode acarretar em punições legais. Use **apenas** em ambientes onde você tem permissão explícita para realizar testes de segurança.

## Funcionalidades
- **Ataque DoS**: Realiza um ataque de negação de serviço simulando múltiplas requisições.
- **Customização de Ataque**: Defina o **IP ou URL** de um alvo, o **tipo de requisição** (GET ou POST), número de **requisições**, **threads** e até se deseja usar **usuários falsos** para ocultar a origem do ataque.
- **Duração do Ataque**: O bot permite definir a duração do ataque (padrão de 60 segundos) e fornece um relatório ao final do processo.
- **Feedback do Ataque**: O bot retorna um feedback do status do alvo após o ataque.

## Funcionalidades Detalhadas
1. **Início do Ataque**: Ao rodar o bot, o usuário é guiado a fornecer o IP ou URL do alvo.
2. **Configurações**: O bot permite configurar o número de requisições, tipo de requisição (GET/POST), número de threads e se usuários falsos devem ser usados.
3. **Resultado do Ataque**: Após o tempo de ataque, o bot retorna uma taxa de sucesso e um aviso se o alvo pode estar offline.

## Licença
Este projeto está licenciado sob a **Apache License 2.0**. Para mais detalhes, consulte o arquivo [LICENSE](LICENSE).
