import discord
from discord.ext import commands
import logging
import pandas as pd
import asyncio
import random
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

FEEDBACK_CHANNEL_ID = 'Colocar o ID do seu canal de FeedBack'
SUGGESTIONS_CHANNEL_ID = 'Colocar o ID do seu canal de Sugestões'
PATCH_NOTE_CHANNEL_ID = 'Colocar o ID do canal de Patch Notes/Notas de Atualizações'
DEFAULT_UPDATE_DESCRIPTION = "Descrição padrão da atualização." 
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
intents.voice_states = True
client = commands.Bot(command_prefix='!', intents=intents)
##################################################################################################################################################
async def add_reaction_with_retry(message, emoji):
    for _ in range(5): 
        try:
            await message.add_reaction(emoji)
            return
        except discord.HTTPException as e:
            if e.status == 429:  
                retry_after = int(e.headers.get('Retry-After', 1)) 
                await asyncio.sleep(retry_after)
            else:
                raise  

async def vote_winning_team(ctx, team1_ids, team2_ids):
    embed = create_embed("Votação", "Clique na reação correspondente ao time vencedor! \n🔵 para o Time 1 \n🔴 para o Time 2.")
    message = await ctx.send(embed=embed)

    await add_reaction_with_retry(message, '🔵')
    await add_reaction_with_retry(message, '🔴')

    def check_reaction(reaction, user):
        return user != client.user and reaction.message.id == message.id and reaction.emoji in ['🔵', '🔴']

    try:
        while True:
            reaction, user = await client.wait_for('reaction_add', check=check_reaction)
            winning_team = team1_ids if reaction.emoji == '🔵' else team2_ids
            losing_team = team2_ids if reaction.emoji == '🔵' else team1_ids

            await ctx.send(embed=create_embed("Resultado", f"O time vencedor é: {'Time 1' if reaction.emoji == '🔵' else 'Time 2'}!"))

            update_stats(winning_team, losing_team)

            break

    except Exception as e:
        await ctx.send(embed=create_embed("Erro", f"Ocorreu um erro: {e}"))

def update_stats(winning_team, losing_team):
    file_path = 'Nome_do_Arquivo.xlsx'

    if os.path.exists(file_path):
        df = pd.read_excel(file_path, engine='openpyxl')
        print("Arquivo carregado com sucesso.")
    else:
        df = pd.DataFrame(columns=['ID', 'name', 'roles', 'Wins', 'Losses', 'player_stats'])
        print("Arquivo não encontrado. Criado novo DataFrame.")

    df['Wins'] = pd.to_numeric(df['Wins'], errors='coerce').fillna(0).astype(int)
    df['Losses'] = pd.to_numeric(df['Losses'], errors='coerce').fillna(0).astype(int)

    print(f"Atualizando {len(winning_team)} vencedores e {len(losing_team)} perdedores.")

    for player_id in winning_team:
        if player_id in df['ID'].values:
            df.loc[df['ID'] == player_id, 'Wins'] += 1
        else:
            new_record = {
                'ID': player_id,
                'name': players[player_id]['name'],
                'roles': players[player_id]['roles'],
                'Wins': 1,
                'Losses': 0,
                'player_stats': '1 Win, 0 Loss'
            }
            df = df.append(new_record, ignore_index=True)
##################################################################################################################################################
##################################################################################################################################################
players = {}

def load_players():
    global players
    try:
        df = pd.read_excel('Nome_do_Arquivo.xlsx', engine='openpyxl')

        players = {
            row['ID']: {
                'name': row['name'],
                'mono_champion': row['Mono Champion'],
                'role_1': row['Role 1'],
                'role_2': row['Role 2'],
                'Wins': row['Wins'],
                'Losses': row['Losses']
            } for index, row in df.iterrows()
        }

    except FileNotFoundError:
        players = {}
        print("Arquivo de dados não encontrado. Inicializando lista vazia de jogadores.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
##################################################################################################################################################
##################################################################################################################################################
players_df = pd.read_excel('C:\\Caminho\\Para\\Nome_do_Arquivo.xlsx')
async def load_players_data():
    global players_df
    players_df = pd.read_excel('C:\\Caminho\\Para\\Nome_do_Arquivo.xlsx')    



    logging.info("Colunas disponíveis no DataFrame: %s", players_df.columns.tolist())

    required_columns = ['ID', 'name', 'Mono Champion', 'Role 1', 'Role 2', 'Losses', 'Wins', 'Total']
    missing_columns = [col for col in required_columns if col not in players_df.columns]

    if missing_columns:
        raise ValueError(f"O arquivo Excel deve conter as colunas {', '.join(required_columns)}. Colunas faltantes: {', '.join(missing_columns)}.")

    player_count = len(players_df)
    logging.info("O código foi carregado. Existem %d jogadores disponíveis na tabela.", player_count)
##################################################################################################################################################
@client.event
async def on_ready():
    logging.info(f'Bot conectado como {client.user.name} ({client.user.id})')
    await load_players_data()
    await check_patch_notes()  

async def check_patch_notes():
    response = input("Bom dia, Boa Tarde ou Boa Noite, iremos ter atualização para ser enviado sobre o Bot hoje? (s/n): ")
    
    if response.lower() == 's':
        num_lines = input("Quantas linhas iremos ter? (máximo de 5): ")
        
        if not num_lines.isdigit() or not (1 <= int(num_lines) <= 5):
            print("Número inválido. Por favor, forneça um número entre 1 e 5.")
            return
        
        lines = []
        for i in range(int(num_lines)):
            line = input(f"Digite a linha {i + 1} da atualização: ")
            lines.append(line)

        await send_patch_notes(lines)

async def send_patch_notes(lines):
    channel = client.get_channel(PATCH_NOTE_CHANNEL_ID)
    if channel:
        embed_patch_notes = discord.Embed(
            title="🔧 Atualização do Bot",
            description="Aqui estão as últimas atualizações:",
            color=discord.Color.blue()
        )
        
        for line in lines:
            embed_patch_notes.add_field(name="Atualização", value=line, inline=False)

        await channel.send(embed=embed_patch_notes)
        logging.info("Patch notes enviados com sucesso para o canal de patch notes.")
    else:
        logging.error("Canal de patch notes não encontrado.")
        print("Canal de patch notes não encontrado.")

def create_embed(title, description):
    return discord.Embed(title=title, description=description, color=discord.Color.blue())

players_df = pd.DataFrame()
selected_ids = []
command_messages = {}

@client.command(name='jogadores')
async def jogadores(ctx):
    if players_df.empty:
        await ctx.send(embed=create_embed("Jogadores", "Nenhum jogador disponível no momento."))
        return

    player_list = players_df.to_dict('records')
    num_players = len(player_list)
    max_per_column = 6
    num_columns = 3
    num_rows = num_columns * max_per_column

    num_embeds = (num_players + num_rows - 1) // num_rows
    
    def format_roles(role1, role2):
        roles = [role for role in [role1, role2] if pd.notna(role)]
        return ', '.join(f'`{role.strip()}`' for role in roles) if roles else "Nenhuma lane definida"

    def format_column(players):
        description = ""
        for player in players:
            mono = player['Mono Champion'] if pd.notna(player['Mono Champion']) else "Nenhum Mono Champion definido"
            description += (f"**ID:** {player['ID']}\n"
                            f"**Nome:** {player['name']}\n"
                            f"**Lanes:** [{format_roles(player['Role 1'], player['Role 2'])}]\n"
                            f"**Mono Champion:** {mono}\n\n")
        return description

    for i in range(num_embeds):
        start_index = i * num_rows
        end_index = min((i + 1) * num_rows, num_players)
        players_for_this_embed = player_list[start_index:end_index]
        
        columns = [players_for_this_embed[i:i + max_per_column] for i in range(0, len(players_for_this_embed), max_per_column)]
        
        embed = discord.Embed(title="Lista de Jogadores", color=discord.Color.blue())
        
        for j in range(num_columns):
            if j < len(columns):
                column_description = format_column(columns[j])
                column_title = f"Coluna {j + 1}"
            else:
                column_description = "Nenhum jogador nesta coluna"
                column_title = f"Coluna {j + 1}"
            
            embed.add_field(name=column_title, value=column_description, inline=True)

        await ctx.send(embed=embed)
#######################################################################################################################################
@client.command()
@commands.has_permissions(administrator=True)
async def beforeiforget(ctx, member: discord.Member):
    def is_member_message(m):
        return m.author == member

    try:
        await ctx.send(embed=create_blue_embed("Ação em Andamento", f"Apagando todas as mensagens de {member.mention}..."))
        await ctx.channel.purge(check=is_member_message)
    except discord.Forbidden:
        await ctx.send(embed=create_blue_embed("Erro", "Eu não tenho permissão para apagar mensagens neste canal."))
    except discord.HTTPException as e:
        await ctx.send(embed=create_blue_embed("Erro", f"Ocorreu um erro ao tentar apagar mensagens: {e}"))
    except Exception as e:
        await ctx.send(embed=create_blue_embed("Erro", f"Ocorreu um erro inesperado: {e}"))

@beforeiforget.error
async def beforeiforget_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=create_blue_embed("Erro", "Sinto muito, você não tem permissões suficientes para executar este comando."))

@client.command()
@commands.has_permissions(administrator=True)
async def blackout(ctx):
    try:
        await ctx.send("Apagando todas as mensagens...")
        await ctx.channel.purge()
    except discord.Forbidden:
        await ctx.send("Eu não tenho permissão para apagar mensagens neste canal.")
    except discord.HTTPException as e:
        await ctx.send(f"Ocorreu um erro ao tentar apagar mensagens: {e}")
    except Exception as e:
        await ctx.send(f"Ocorreu um erro inesperado: {e}")

@blackout.error
async def blackout_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=create_blue_embed("Erro", "Sinto muito, você não tem permissões suficientes para executar este comando."))

@client.command()
@commands.has_permissions(administrator=True)
async def blackops(ctx, limit: int):
    if 1 <= limit <= 100:
        try:
            await ctx.send(embed=create_blue_embed("Ação em Andamento", f"Apagando {limit} mensagens..."))
            await ctx.channel.purge(limit=limit)
        except discord.Forbidden:
            await ctx.send(embed=create_blue_embed("Erro", "Eu não tenho permissão para apagar mensagens neste canal."))
        except discord.HTTPException as e:
            await ctx.send(embed=create_blue_embed("Erro", f"Ocorreu um erro ao tentar apagar mensagens: {e}"))
        except Exception as e:
            await ctx.send(embed=create_blue_embed("Erro", f"Ocorreu um erro inesperado: {e}"))
    else:
        await ctx.send(embed=create_blue_embed("Erro", "O número deve estar entre 1 e 100."))

@blackops.error
async def blackops_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=create_blue_embed("Erro", "Sinto muito, você não tem permissões suficientes para executar este comando."))

#######################################################################################################################################
def create_blue_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=0x007bff)
    return embed

def split_text(text, max_length=1024):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

@client.command()
async def ajuda(ctx):
    general_help_text = (
        "**Comandos Gerais:**\n"
        "`!liga_das_ruas` - Permite selecionar 10 IDs de jogadores para criar dois times aleatórios. Os times serão exibidos. BOA SORTE 💀\n\n"
        "`!mono_aram` - Por que não tentar um tipo de jogo diferente. O mono Aram serve para peagar o mono de uma pessoa, e deixar a outra jogar com ele. 😁\n"
        "`!remove_jogador <ID>` - Permite remover um jogador já existente da próoria lista de jogadores. 🥹\n"
        "`!add_jogador` - Inicia o processo de adicionar um jogador com um fluxo interativo. 😎\n"
        "`!edit_jogador` - Se forem mudar o riot nick, lane principal e lane secundaria, podem utilizar este comando para atualizar a tabela. 😊\n"
        "`!jogadores` - Lista todos os jogadores e suas lanes, junto com os campeões mono disponíveis. 😲\n"
        "`!id <nome>` - Mostra a ID e os detalhes de um jogador baseado no nome fornecido. 🤩\n"
        "`!feedback` - Forneça o seu FeedBack em relação com a sua experiência de como está sendo usar o Bot, esperamos que esteja sendo boa 😀\n"
        "`!sugestao` - Por que não dar alguma sugestão para que possamos melhorar o bot? Deixe uma sugestão para a gente poder avaliar. 😀\n"
        "`!caçaoteemo` - Fornecendo os Id's podem jogar um caça ao teemo, onde o qual um teemo de forma aleatroria é escolhido em cada time para os dois lados. ☠️\n"
    )

    admin_help_text = (
        "**Comandos Administrativos:**\n"
        "`!blackout` - Apaga todas as mensagens do canal atual. Somente administradores podem usar este comando. 💣\n"
        "`!blackops` - Apaga um número específico de mensagens do canal atual (de 1 a 100). Somente administradores podem usar este comando. 🚀\n"
        "`!beforeiforget` - Apaga todas as mensagens de um usuário mencionado no canal atual. Somente administradores podem usar este comando. 👾"
    )

    embed = discord.Embed(title="Comandos Disponíveis", description=general_help_text, color=discord.Color.blue())
    
    embed.add_field(name="Comandos Administrativos", value=admin_help_text, inline=False)

    if ctx.author.guild_permissions.administrator:
        dm_channel = await ctx.author.create_dm()
        await dm_channel.send(embed=embed)
        await ctx.send("Enviamos uma mensagem com todos os comandos para sua DM.")
    else:
        await ctx.send(embed=embed)

@client.command(name='feedback')
async def feedback(ctx, *, message: str):
    channel = client.get_channel(FEEDBACK_CHANNEL_ID)
    if channel:
        embed_feedback = discord.Embed(
            title="Novo Feedback Recebido",
            description=f"**Usuário:** {ctx.author.name}\n**Mensagem:** {message}",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed_feedback)
        await ctx.send(embed=create_embed("Feedback Enviado", "Seu feedback foi enviado com sucesso!"))
    else:
        await ctx.send(embed=create_embed("Erro", "Canal de feedback não encontrado."))

@client.command(name='sugestao')
async def sugestao(ctx, *, message: str):
    channel = client.get_channel(SUGGESTIONS_CHANNEL_ID)
    if channel:
        embed_sugestao = discord.Embed(
            title="Nova Sugestão Recebida",
            description=f"**Usuário:** {ctx.author.name}\n**Mensagem:** {message}",
            color=discord.Color.blue()
        )
        await channel.send(embed=embed_sugestao)
        await ctx.send(embed=create_embed("Sugestão Enviada", "Sua sugestão foi enviada com sucesso!"))
    else:
        await ctx.send(embed=create_embed("Erro", "Canal de sugestões não encontrado."))

@client.command(name='add_jogador')
async def add_jogador(ctx):
    await ctx.send(embed=create_blue_embed("Adicionar Jogador", "Vamos adicionar um novo jogador! Por favor, forneça as seguintes informações:"))

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        # Solicitar nome do jogador
        await ctx.send(embed=create_blue_embed("Nome do Jogador", "Digite o nome do jogador:"))
        name_msg = await client.wait_for('message', check=check)
        name = name_msg.content

        # Gerar próximo ID
        next_id = len(players_df) + 1

        # Solicitar Mono Champion
        await ctx.send(embed=create_blue_embed("Mono Champion", "Digite o Mono Champion do jogador:"))
        mono_msg = await client.wait_for('message', check=check)
        mono_champion = mono_msg.content

        # Solicitar Role 1
        await ctx.send(embed=create_blue_embed("Role 1", "Digite o Lane Principal do jogador:"))
        role1_msg = await client.wait_for('message', check=check)
        role1 = role1_msg.content

        # Solicitar Role 2 (opcional)
        await ctx.send(embed=create_blue_embed("Role 2", "Digite o Lane Secundaria do jogador (ou deixe em branco):"))
        role2_msg = await client.wait_for('message', check=check)
        role2 = role2_msg.content or None

        # Criar novo registro
        new_row = {
            'ID': next_id,
            'name': name,
            'Mono Champion': mono_champion,
            'Role 1': role1,
            'Role 2': role2,
            'Losses': 0,
            'Wins': 0,
            'Total': 0
        }

        # Adicionar ao DataFrame
        global players_df
        players_df = pd.concat([players_df, pd.DataFrame([new_row])], ignore_index=True)

        # Salvar no Excel
        players_df.to_excel('C:\\Caminho\\Para\\Nome_doArquivo.xlsx', index=False)

        # Enviar confirmação
        embed = create_blue_embed("Jogador Adicionado", f"O jogador **{name}** foi adicionado com sucesso!")
        embed.add_field(name="ID", value=str(next_id))
        embed.add_field(name="Mono Champion", value=mono_champion)
        embed.add_field(name="Role 1", value=role1)
        embed.add_field(name="Role 2", value=role2 if role2 else "Nenhum")
        embed.add_field(name="Derrotas", value="0")
        embed.add_field(name="Vitórias", value="0")
        embed.add_field(name="Total", value="0")

        await ctx.send(embed=embed)
        logging.info(f"Jogador {name} adicionado com sucesso.")
    except Exception as e:
        await ctx.send(embed=create_blue_embed("Erro", f"Ocorreu um erro: {e}"))
        logging.error(f"Erro ao adicionar jogador: {e}")

@client.command(name='remove_jogador')
async def remove_jogador(ctx, player_id: int):
    global players_df

    if player_id not in players_df['ID'].values:
        await ctx.send(embed=create_blue_embed("Erro", f"Jogador com ID {player_id} não encontrado."))
        return

    players_df = players_df[players_df['ID'] != player_id].reset_index(drop=True)

    players_df.to_excel('C:\\Caminho\\Para\\Nome_doArquivo.xlsx', index=False)

    await ctx.send(embed=create_blue_embed("Jogador Removido", f"O jogador com ID **{player_id}** foi removido com sucesso!"))
    logging.info(f"Jogador com ID {player_id} removido com sucesso.")

@client.command(name='id')
async def show_player_id(ctx, *, player_name: str):
    global players_df

    player_row = players_df[players_df['name'].str.lower() == player_name.lower()]

    if player_row.empty:
        await ctx.send(embed=create_blue_embed("Erro", f"Nenhum jogador encontrado com o nome **{player_name}**."))
        return

    player_data = player_row.iloc[0]

    embed = discord.Embed(
        title=f"Detalhes do Jogador: {player_data['name']}",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="**ID**", value=f"**{player_data['ID']}**", inline=True)
    embed.add_field(name="**Mono Champion**", value=f"**{player_data['Mono Champion']}**", inline=True)
    embed.add_field(name="**Role 1**", value=f"**{player_data['Role 1']}**", inline=True)
    embed.add_field(name="**Role 2**", value=f"**{player_data['Role 2'] if pd.notna(player_data['Role 2']) else 'Nenhuma'}**", inline=True)
    embed.add_field(name="**Derrotas**", value=f"**{player_data['Losses'] if pd.notna(player_data['Losses']) else '0'}**", inline=True)
    embed.add_field(name="**Vitórias**", value=f"**{player_data['Wins'] if pd.notna(player_data['Wins']) else '0'}**", inline=True)
    embed.add_field(name="**Total**", value=f"**{player_data['Total'] if pd.notna(player_data['Total']) else '0'}**", inline=True)

    await ctx.send(embed=embed)

##################################################################################################################################################
##################################################################################################################################################
@client.command()
async def liga_das_ruas(ctx):
    if not players:
        await ctx.send("Erro: Dados dos jogadores não carregados.")
        return

    await ctx.send(embed=create_embed("Seleção de IDs", "Por favor, forneça 10 IDs dos jogadores (1 a 18), separados por espaço."))

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and all(x.isdigit() for x in msg.content.split())

    try:
        ids_message = await client.wait_for('message', timeout=300.0, check=check)
        ids = list(map(int, ids_message.content.split()))
        if len(ids) != 10:
            await ctx.send(embed=create_embed("Erro", "Você deve fornecer exatamente 10 IDs válidos, separados por espaço."))
            return

        valid_ids = [id for id in ids if id in players]
        if len(valid_ids) < 10:
            await ctx.send(embed=create_embed("Aviso", f"Apenas {len(valid_ids)} IDs válidos foram fornecidos. Continuando com os IDs válidos."))

        random.shuffle(valid_ids)  
        team1_ids = valid_ids[:5]
        team2_ids = valid_ids[5:]

        team1_info = [f"{players[id]['name']} - {players[id]['role_1']}, {players[id]['role_2']}" for id in team1_ids]
        team2_info = [f"{players[id]['name']} - {players[id]['role_1']}, {players[id]['role_2']}" for id in team2_ids]

        embed = create_embed("Times da Liga das Ruas", "")
        embed.add_field(name="Time 1", value="\n".join(team1_info), inline=False)
        embed.add_field(name="Time 2", value="\n".join(team2_info), inline=False)

        await ctx.send(embed=embed)

        await vote_winning_team(ctx, team1_ids, team2_ids)
    except asyncio.TimeoutError:
        await ctx.send(embed=create_embed("Tempo Esgotado", "Tempo esgotado. Por favor, tente novamente."))
load_players()
##################################################################################################################################################


##################################################################################################################################################
@client.command()
async def caçaoteemo(ctx):
    embed_inicial = discord.Embed(
        title="Início da Partida",
        description="Digite os IDs dos jogadores separados por espaço:",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed_inicial)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await client.wait_for('message', check=check, timeout=300)  

        ids = list(map(int, msg.content.split()))

        valid_ids = [id for id in ids if id in players_df['ID'].values]

        if len(valid_ids) < 2:
            await ctx.send("É preciso de pelo menos 2 jogadores para iniciar a partida.")
            return

        team1_ids, team2_ids = formar_times(valid_ids)

        teemo1 = random.choice(team1_ids)
        teemo2 = random.choice(team2_ids)
        teemo1_name = players_df[players_df['ID'] == teemo1]['name'].values[0]
        teemo2_name = players_df[players_df['ID'] == teemo2]['name'].values[0]

        embed_confirmação = discord.Embed(
            title="Confirmação dos Teemos",
            description=f"Os Teemos são {teemo1_name} e {teemo2_name}? Digite 'sim' para confirmar ou o ID do verdadeiro Teemo.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed_confirmação)

        msg = await client.wait_for('message', check=check)
        confirm_teemo1 = msg.content.lower() == 'sim' 
        if not confirm_teemo1:
            try:
                teemo = int(msg.content)
                confirm_teemo1 = teemo in valid_ids
            except ValueError:
                await ctx.send("ID inválido.")
                return

        embed = discord.Embed(title="Times da Caça ao Teemo", color=discord.Color.blue())
        embed.add_field(name="Time 1", value=", ".join(players_df[players_df['ID'].isin(team1_ids)]['name']), inline=False)
        embed.add_field(name="Time 2", value=", ".join(players_df[players_df['ID'].isin(team2_ids)]['name']), inline=False)
        
        embed.add_field(name="Teemo 1", value=teemo1_name if confirm_teemo1 else "Ainda não revelado", inline=False)
        embed.add_field(name="Teemo 2", value=teemo2_name, inline=False)

        await ctx.send(embed=embed)

    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")
    except ValueError:
        await ctx.send("Os IDs devem ser números inteiros.")

def formar_times(ids):
    """
    Divide os jogadores em dois times aleatoriamente.

    Args:
        ids: Uma lista de IDs dos jogadores.

    Returns:
        Uma tupla contendo duas listas, representando os IDs dos jogadores dos times 1 e 2.
    """
    random.shuffle(ids)
    team1_ids = ids[:len(ids) // 2]
    team2_ids = ids[len(ids) // 2:]
    return team1_ids, team2_ids      
##################################################################################################################################################


##################################################################################################################################################
@client.command()
async def edit_jogador(ctx, player_id: int = None):
    if player_id is None:
        await ctx.send("Por favor, forneça o ID do jogador que deseja editar.")
        return

    try:
        df = pd.read_excel('C:\\Caminho\\Para\\Nome_doArquivo.xlsx')
        await ctx.send("Tabela carregada com sucesso.")
    except Exception as e:
        await ctx.send(f"Erro ao carregar a tabela: {e}")
        return

    player = df[df['ID'] == player_id]
    if player.empty:
        await ctx.send("Jogador não encontrado.")
        return

    embed = discord.Embed(title="Editar Jogador", color=discord.Color.blue())
    embed.add_field(name="ID", value=player_id, inline=True)
    embed.add_field(name="Nome", value=player['name'].values[0], inline=True)
    embed.add_field(name="Mono Champion", value=player['Mono Champion'].values[0], inline=True)
    embed.add_field(name="Role 1", value=player['Role 1'].values[0], inline=True)
    embed.add_field(name="Role 2", value=player['Role 2'].values[0], inline=True)

    await ctx.send(embed=embed)

    await ctx.send("O que você gostaria de editar? (name, mono champion, role 1, role 2)")
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        response = await client.wait_for('message', check=check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.send("Tempo esgotado. Tente novamente.")
        return

    field_to_edit = response.content.lower()

    if field_to_edit in ['name', 'mono champion', 'role 1', 'role 2']:
        await ctx.send(f"Insira o novo valor para {field_to_edit}:")
        
        try:
            new_value = await client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            await ctx.send("Tempo esgotado. Tente novamente.")
            return
        
        df.loc[df['ID'] == player_id, field_to_edit] = new_value.content
        print(f"Atualizando {field_to_edit} para {new_value.content} no jogador ID {player_id}")

        try:
            df.to_excel('C:\\Caminho\\Para\\Nome_doArquivo.xlsx', index=False)
            await ctx.send(f"Jogador {field_to_edit} atualizado com sucesso para '{new_value.content}'!")
        except Exception as e:
            await ctx.send(f"Ocorreu um erro ao salvar as alterações: {e}")

    else:
        await ctx.send("Opção inválida. Tente novamente.")
##################################################################################################################################################

df = pd.read_excel('Nome_do_Arquivo.xlsx')  

@client.command()
async def mono_aram(ctx):
    embed = discord.Embed(title="Boas vindas ao Mono Aram!", color=discord.Color.blue())
    embed.add_field(name="Quantos jogadores irão se ter no presente momento?", value="Por favor, insira apenas números pares (máximo de 10 jogadores). Ex: 6", inline=False)
    
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        msg = await client.wait_for('message', check=check)
        num_players = int(msg.content)

        if num_players % 2 != 0 or num_players > 10:
            await ctx.send("Por favor, insira um número par e não maior que 10!")
            return
        
        embed = discord.Embed(title="Perfeito!", description=f"Serão então um {num_players//2}v{num_players//2}?", color=discord.Color.blue())
        embed.add_field(name="Coloque um C para confirmar, ou E para Editar", value="🅲 / 🅴", inline=False)
        
        await ctx.send(embed=embed)

        msg = await client.wait_for('message', check=check)
        
        if msg.content.lower() != 'c':
            await ctx.send("Você escolheu editar. Tente novamente.")
            return
        
        embed = discord.Embed(title="Quais são os IDs dos jogadores, por favor?", color=discord.Color.blue())
        await ctx.send(embed=embed)

        msg = await client.wait_for('message', check=check)
        player_ids = list(map(int, msg.content.split()))

        if len(player_ids) != num_players:
            await ctx.send("O número de IDs não coincide com o número de jogadores!")
            return

        filtered_df = df[df['ID'].isin(player_ids)]

        random.shuffle(player_ids)
        team_blue = player_ids[:num_players//2]
        team_red = player_ids[num_players//2:]

        blue_team_info = []
        red_team_info = []

        available_monos = {row['ID']: row['Mono Champion'] for _, row in filtered_df.iterrows()}
        
        used_monos = set()

        for player_id in team_blue:
            player_name = filtered_df[filtered_df['ID'] == player_id]['name'].values[0]
            other_players = [pid for pid in player_ids if pid != player_id]
            selected_player_id = random.choice(other_players)
            selected_mono = available_monos[selected_player_id]

            while selected_mono in used_monos or selected_player_id == player_id:
                selected_player_id = random.choice(other_players)
                selected_mono = available_monos[selected_player_id]

            used_monos.add(selected_mono)  
            
            blue_team_info.append(f"**{player_name}** (ID: {player_id})\nMono: **{selected_mono}** de **{filtered_df[filtered_df['ID'] == selected_player_id]['name'].values[0]}**")

        for player_id in team_red:
            player_name = filtered_df[filtered_df['ID'] == player_id]['name'].values[0]
            other_players = [pid for pid in player_ids if pid != player_id]
            selected_player_id = random.choice(other_players)
            selected_mono = available_monos[selected_player_id]

            while selected_mono in used_monos or selected_player_id == player_id:
                selected_player_id = random.choice(other_players)
                selected_mono = available_monos[selected_player_id]

            used_monos.add(selected_mono)  
            
            red_team_info.append(f"**{player_name}** (ID: {player_id})\nMono: **{selected_mono}** de **{filtered_df[filtered_df['ID'] == selected_player_id]['name'].values[0]}**")

        embed = discord.Embed(title="Aqui estão os times e seus Monos devidos:", color=discord.Color.blue())
        embed.add_field(name="**Time Azul**", value="\n".join(blue_team_info), inline=True)
        embed.add_field(name="**Time Vermelho**", value="\n".join(red_team_info), inline=True)
        
        embed.set_footer(text="Tenham um bom jogo e que vença o melhor! 🎮")
        
        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send("Ocorreu um erro. Por favor, tente novamente.")
        print(e)

client.run('TOKEN_YOUR_BOT')