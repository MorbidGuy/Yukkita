# Bot de Jogo para League of Legends

Este repositório contém um bot em Python desenvolvido para facilitar a organização e interação de jogadores no ambiente de *League of Legends*. O bot permite criar times, gerenciar jogadores e interagir de maneira divertida com a comunidade.

## Funcionalidades

O bot oferece diversos comandos que ajudam na administração e na organização de partidas e jogadores. Veja abaixo os principais comandos:

### **Comandos Gerais:**

- `!liga_das_ruas`: Cria dois times aleatórios com 10 jogadores. Boa sorte! 💀
- `!mono_aram`: Troca o mono de um jogador e deixa o outro jogar com ele. 😁
- `!remove_jogador <ID>`: Remove um jogador da lista. 🥹
- `!add_jogador`: Adiciona um jogador com fluxo interativo. 😎
- `!edit_jogador`: Atualiza o Riot Nick, lane principal ou secundária. 😊
- `!jogadores`: Lista jogadores, lanes e campeões mono disponíveis. 😲
- `!id <nome>`: Mostra a ID e detalhes de um jogador. 🤩
- `!feedback`: Envie seu feedback sobre a experiência com o bot. 😀
- `!sugestao`: Deixe uma sugestão para melhorar o bot. 😀
- `!caçaoteemo`: Jogo de "caça ao Teemo", onde um Teemo aleatório é escolhido para cada time. ☠️

### **Comandos Administrativos:**

- `!blackout`: Apaga todas as mensagens do canal (somente admins). 💣
- `!blackops`: Apaga até 100 mensagens do canal (somente admins). 🚀
- `!beforeiforget`: Apaga todas as mensagens de um usuário no canal (somente admins). 👾

## Como Usar

### 1. **Instalação**

Para rodar o bot, é necessário ter o Python instalado em sua máquina. O bot foi desenvolvido com Python 3.x.

1. **Clone este repositório** para o seu ambiente local:

    ```bash
    git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
    cd SEU_REPOSITORIO
    ```

2. **Instale as dependências necessárias**:

    Antes de executar o bot, instale as bibliotecas que ele depende. Utilize o comando abaixo para instalar todas as dependências do projeto:

    ```bash
    pip install -r requirements.txt
    ```

    Ou, se preferir instalar manualmente as bibliotecas necessárias:

    ```bash
    pip install discord.py pandas openpyxl
    ```

### 2. **Configuração do Bot**

- **Token do Bot**: Para rodar o bot, você precisará de um token do Discord. Siga os passos abaixo para obter o token:

  1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications).
  2. Crie uma nova aplicação.
  3. Vá até a aba "Bot" e gere um token.
  4. Substitua `'SEU_TOKEN_AQUI'` no código pelo token gerado.

- **IDs dos Canais**: O bot interage com canais específicos no Discord. Você precisará configurar as IDs dos canais onde os feedbacks e sugestões serão enviados:

  - **FeedBack Channel ID**: Canal para enviar feedbacks (`FEEDBACK_CHANNEL_ID`)
  - **Suggestions Channel ID**: Canal para sugestões (`SUGGESTIONS_CHANNEL_ID`)
  - **Patch Notes Channel ID**: Canal para atualizações e notas de patches (`PATCH_NOTE_CHANNEL_ID`)

  Para pegar as IDs dos canais:
  1. Ative o modo de desenvolvedor nas configurações do Discord: **Configurações do Usuário > Avançado > Modo de Desenvolvedor**.
  2. Clique com o botão direito do mouse no canal desejado e selecione "Copiar ID".

  **Exemplo de configuração no código**:

  ```python
  FEEDBACK_CHANNEL_ID = 'Coloque_aqui_o_ID_do_canal_de_feedback'
  SUGGESTIONS_CHANNEL_ID = 'Coloque_aqui_o_ID_do_canal_de_sugestoes'
  PATCH_NOTE_CHANNEL_ID = 'Coloque_aqui_o_ID_do_canal_de_patch_notes'
Arquivo Excel (.xlsx): O bot utiliza um arquivo Excel para gerenciar os jogadores e estatísticas. Você precisará de um arquivo .xlsx contendo as seguintes colunas obrigatórias:

ID — ID do jogador.
name — Nome do jogador.
Mono Champion — Campeão mono do jogador.
Role 1 — Primeira role (por exemplo, "Top", "Mid", "Jungle", etc.).
Role 2 — Segunda role (opcional).
Losses — Número de derrotas.
Wins — Número de vitórias.
Total — Total de jogos jogados (opcional).
Caminho do Arquivo Excel: No código, substitua o caminho do arquivo pelo local onde o arquivo .xlsx está armazenado na sua máquina. Exemplo:

python
Copiar
players_df = pd.read_excel('C:\\Caminho\\Para\\Nome_do_Arquivo.xlsx')
Certifique-se de alterar 'C:\\Caminho\\Para\\Nome_do_Arquivo.xlsx' para o caminho correto do arquivo na sua máquina. Se o arquivo não existir, ele será criado automaticamente com a estrutura necessária, mas você precisa garantir que o arquivo Excel tenha as colunas corretas.

3. Executando o Bot
Depois de configurar o bot, basta rodar o arquivo principal para iniciar o bot:

bash
Copiar
python bot.py
O bot irá iniciar e ficará aguardando interações no servidor do Discord.

Dependências
Este bot foi desenvolvido utilizando as seguintes bibliotecas:

discord.py: Para interação com a API do Discord.
pandas: Para gerenciamento de dados de jogadores e estatísticas.
openpyxl: Para leitura e escrita de arquivos Excel.
Você pode instalar essas dependências executando:

bash
Copiar
pip install discord.py pandas openpyxl
Contribuindo
Se você gostaria de contribuir com melhorias ou novos recursos para o bot, fique à vontade para enviar um pull request! Vamos adorar a sua contribuição.

Licença
Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.

markdown
Copiar

### Alterações feitas:
- **Arquivo Excel (`.xlsx`)**: Agora está mais claro que o arquivo Excel precisa ter colunas específicas e um exemplo das colunas obrigatórias foi adicionado.
- **Caminho do arquivo Excel**: Explicitação de que o caminho do arquivo deve ser configurado corretamente no código, com um exemplo de como fazer isso.




