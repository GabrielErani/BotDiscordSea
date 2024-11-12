import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import os  # Importar os para acessar variáveis de ambiente

intents = discord.Intents.default()
intents.message_content = True  # Permite ler o conteúdo das mensagens
intents.members = True  # Necessário para acessar guild.owner e member permissions
bot = commands.Bot(command_prefix='!', intents=intents)

bot.cancel_update = False  # Flag para cancelar o processo de atualização

@bot.event
async def on_ready():
    print(f'🤖 Bot conectado como {bot.user}')

# Evento para adicionar a role 'Não Verificado' aos novos membros
@bot.event
async def on_member_join(member):
    role = get(member.guild.roles, name='🚫 Não Verificado')
    if role:
        await member.add_roles(role)
        print(f"🚫 Role 'Não Verificado' adicionada a {member.name}")

# Função para configurar roles
async def setup_roles(guild, ctx):
    try:
        # Criar roles estilizadas, se não existirem
        roles_to_create = {
            '👑 Dono da ClownGuild': {},
            '🚫 Não Verificado': {},
            '✅ Verificado': {},
            '🪐 Membro da ClownGuild': {},
            '🌊 Aventureiro': {}
        }
        existing_roles = {role.name: role for role in guild.roles}
        for role_name, role_params in roles_to_create.items():
            if bot.cancel_update:
                await ctx.send("🛑 Atualização cancelada durante a configuração das roles.")
                return
            if role_name not in existing_roles:
                new_role = await guild.create_role(name=role_name, **role_params)
                existing_roles[role_name] = new_role
                await ctx.send(f"Role '{role_name}' criada.")
            else:
                await ctx.send(f"Role '{role_name}' já existe.")

        # Atribuir a você a role de dono da guilda, se ainda não tiver
        owner_role = existing_roles['👑 Dono da ClownGuild']
        if owner_role not in ctx.author.roles:
            await ctx.author.add_roles(owner_role)
            await ctx.send("👑 Role 'Dono da ClownGuild' atribuída a você.")
        else:
            await ctx.send("👑 Você já possui a role 'Dono da ClownGuild'.")

        return existing_roles

    except Exception as e:
        await ctx.send(f"⚠️ Erro durante a configuração das roles: {e}")

# Função para configurar canais e categorias
async def setup_channels(guild, existing_roles, ctx):
    try:
        # Configurar permissões para categorias e canais
        overwrite_default = discord.PermissionOverwrite(read_messages=False)
        overwrite_unverified = discord.PermissionOverwrite(read_messages=False)
        overwrite_verified = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        overwrite_adventurer = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        overwrite_guild_member = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        owner_role = existing_roles['👑 Dono da ClownGuild']
        unverified_role = existing_roles['🚫 Não Verificado']
        verified_role = existing_roles['✅ Verificado']
        guild_member_role = existing_roles['🪐 Membro da ClownGuild']
        adventurer_role = existing_roles['🌊 Aventureiro']

        # Categorias e canais a serem criados
        categories_channels = {
            '🔑 Verificação': {
                'text_channels': [
                    ('🔑-verificação', {
                        'overwrites': {
                            guild.default_role: overwrite_unverified,
                            unverified_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)
                        },
                        'topic': "Digite !verificar para ter acesso ao servidor."
                    })
                ]
            },
            '💬 Bate-Papo Geral': {
                'text_channels': [
                    ('🗣️-geral', {'topic': "Conversas gerais e interações entre membros."}),
                    ('📢-anúncios', {'topic': "Fique por dentro das novidades e anúncios."}),
                    ('📜-regras', {'topic': "Leia as regras do servidor para manter um ambiente saudável."})
                ]
            },
            '🎮 Sea of Thieves': {
                'text_channels': [
                    ('🏴‍☠️-discussões', {'topic': "Discussões sobre Sea of Thieves."}),
                    ('🗺️-dicas', {'topic': "Dicas e estratégias."})
                ]
            },
            '🎙️ Calls Públicas': {
                'voice_channels': [
                    ('🎧 Bate-Papo', {})
                ]
            },
            '🎭 ClownGuild (Privado)': {
                'text_channels': [
                    ('🤫-chat-da-guilda', {
                        'overwrites': {
                            guild.default_role: overwrite_default,
                            guild_member_role: overwrite_guild_member,
                            owner_role: overwrite_verified
                        },
                        'topic': "Canal privado para membros da ClownGuild"
                    })
                ],
                'voice_channels': [
                    ('🎧 Reunião da Guilda', {
                        'overwrites': {
                            guild.default_role: overwrite_default,
                            guild_member_role: overwrite_guild_member,
                            owner_role: overwrite_verified
                        }
                    })
                ]
            },
            '🛥️ Barcos da Guilda': {
                'voice_channels': [
                    ('🛥️ PomboCeifeiro', {
                        'user_limit': 4,
                        'overwrites': {
                            guild.default_role: overwrite_default,
                            guild_member_role: discord.PermissionOverwrite(
                                connect=True,
                                speak=True,
                                mute_members=True,
                                deafen_members=True,
                                move_members=True,
                                manage_channels=True
                            ),
                            owner_role: discord.PermissionOverwrite(
                                connect=True,
                                speak=True,
                                mute_members=True,
                                deafen_members=True,
                                move_members=True,
                                manage_channels=True
                            )
                        }
                    }),
                    ('🛥️ PomboCeifeirinho', {
                        'user_limit': 2,
                        'overwrites': {
                            guild.default_role: overwrite_default,
                            guild_member_role: discord.PermissionOverwrite(
                                connect=True,
                                speak=True,
                                mute_members=True,
                                deafen_members=True,
                                move_members=True,
                                manage_channels=True
                            ),
                            owner_role: discord.PermissionOverwrite(
                                connect=True,
                                speak=True,
                                mute_members=True,
                                deafen_members=True,
                                move_members=True,
                                manage_channels=True
                            )
                        }
                    }),
                    ('🛥️ PomboQuaseAnao', {
                        'user_limit': 3,
                        'overwrites': {
                            guild.default_role: overwrite_default,
                            guild_member_role: discord.PermissionOverwrite(
                                connect=True,
                                speak=True,
                                mute_members=True,
                                deafen_members=True,
                                move_members=True,
                                manage_channels=True
                            ),
                            owner_role: discord.PermissionOverwrite(
                                connect=True,
                                speak=True,
                                mute_members=True,
                                deafen_members=True,
                                move_members=True,
                                manage_channels=True
                            )
                        }
                    })
                ]
            },
            '🛶 Chalupa': {
                'voice_channels': [
                    (f'🛶 Chalupa {i}', {'user_limit': 2}) for i in range(1, 6)
                ]
            },
            '🚤 Bergantim': {
                'voice_channels': [
                    (f'🚤 Bergantim {i}', {'user_limit': 3}) for i in range(1, 6)
                ]
            },
            '🚢 Galeão': {
                'voice_channels': [
                    (f'🚢 Galeão {i}', {'user_limit': 4}) for i in range(1, 6)
                ]
            }
        }

        # Criar categorias e canais
        existing_categories = {category.name: category for category in guild.categories}
        for category_name, channels in categories_channels.items():
            if bot.cancel_update:
                await ctx.send("🛑 Atualização cancelada durante a configuração dos canais.")
                return
            if category_name not in existing_categories:
                category = await guild.create_category(category_name)
                existing_categories[category_name] = category
                await ctx.send(f"Categoria '{category_name}' criada.")
            else:
                category = existing_categories[category_name]
                await ctx.send(f"Categoria '{category_name}' já existe.")

            # Criar canais de texto
            if 'text_channels' in channels:
                for channel_name, params in channels['text_channels']:
                    if bot.cancel_update:
                        await ctx.send("🛑 Atualização cancelada durante a criação de canais de texto.")
                        return
                    existing_channel = get(guild.text_channels, name=channel_name)
                    if not existing_channel:
                        overwrites = params.get('overwrites', {
                            guild.default_role: overwrite_default,
                            verified_role: overwrite_verified,
                            adventurer_role: overwrite_adventurer,
                            guild_member_role: overwrite_guild_member,
                            owner_role: overwrite_verified
                        })
                        topic = params.get('topic', '')
                        await guild.create_text_channel(
                            channel_name,
                            category=category,
                            overwrites=overwrites,
                            topic=topic
                        )
                        await ctx.send(f"Canal de texto '{channel_name}' criado na categoria '{category_name}'.")
                    else:
                        await ctx.send(f"Canal de texto '{channel_name}' já existe.")

            # Criar canais de voz
            if 'voice_channels' in channels:
                for channel_name, params in channels['voice_channels']:
                    if bot.cancel_update:
                        await ctx.send("🛑 Atualização cancelada durante a criação de canais de voz.")
                        return
                    existing_channel = get(guild.voice_channels, name=channel_name)
                    if not existing_channel:
                        user_limit = params.get('user_limit', 0)
                        overwrites = params.get('overwrites', {
                            guild.default_role: overwrite_default,
                            verified_role: overwrite_verified,
                            adventurer_role: overwrite_adventurer,
                            guild_member_role: overwrite_guild_member,
                            owner_role: overwrite_verified
                        })
                        new_channel = await guild.create_voice_channel(
                            channel_name,
                            category=category,
                            user_limit=user_limit,
                            overwrites=overwrites
                        )
                        # Permissões especiais para o dono nas calls de barcos
                        if category_name in ['🛶 Chalupa', '🚤 Bergantim', '🚢 Galeão']:
                            await new_channel.set_permissions(owner_role, connect=True, move_members=True, manage_channels=True)
                        await ctx.send(f"Canal de voz '{channel_name}' criado na categoria '{category_name}'.")
                    else:
                        await ctx.send(f"Canal de voz '{channel_name}' já existe.")

        # Criar canal privado de comandos
        if bot.cancel_update:
            await ctx.send("🛑 Atualização cancelada antes de criar o canal de comandos.")
            return
        private_command_channel_name = '🔒-comandos'
        existing_channel = get(guild.text_channels, name=private_command_channel_name)
        if not existing_channel:
            owner_overwrites_channel = {
                guild.default_role: overwrite_default,
                owner_role: overwrite_verified
            }
            await guild.create_text_channel(private_command_channel_name, overwrites=owner_overwrites_channel)
            await ctx.send("🔒 Canal privado de comandos criado.")
        else:
            await ctx.send("🔒 Canal privado de comandos já existe.")

        # Enviar mensagens automáticas nos canais apropriados
        try:
            # Enviar regras no canal 📜-regras
            regras_channel = get(guild.text_channels, name='📜-regras')
            if regras_channel:
                regras_message = """
🛡️ **Código de Conduta dos Piratas** 🛡️

Ahoy, marujos! Bem-vindos ao nosso porto seguro! Para que todos possam desfrutar das aventuras nos sete mares, sigam nosso código pirata:

1. **Respeito Entre Piratas**: Tratem todos os membros da tripulação com respeito. Não toleramos insultos, ofensas, discriminação ou qualquer comportamento que faça um pirata caminhar na prancha. Vamos manter o rum fluindo e as risadas ecoando!

2. **Nada de Trapaças**: Jogar limpo é a lei dos mares! Qualquer tipo de trapaça, uso de bugs, hacks ou ações que estraguem a diversão dos outros resultará em ser lançado ao Kraken.

3. **Linguagem Apropriada**: Mantenha o linguajar digno de um pirata respeitável. Evite palavrões excessivos, especialmente nos canais públicos. Queremos que todos se sintam em casa na nossa taverna.

4. **Nada de Spam ou Propaganda**: Não encha nossos barris com mensagens repetitivas ou propaganda não autorizada. Seja cauteloso com links externos para evitar armadilhas e emboscadas.

5. **Denúncias e Sugestões**: Se tiver problemas com outro pirata ou ideias para melhorar nosso porto, fale com os oficiais (moderadores). Sua voz será ouvida!

6. **Respeito à Privacidade**: Não invada a cabine de outro pirata (mensagens diretas) sem permissão. A invasão pode resultar em ser deixado numa ilha deserta.

Lembrem-se, estamos aqui para compartilhar histórias, cantar canções e navegar juntos em busca de aventuras e tesouros! Que os ventos estejam sempre a seu favor! ⚓
"""
                await regras_channel.send(regras_message)
                await ctx.send("📜 Mensagem de regras enviada.")
            else:
                await ctx.send("⚠️ Canal 📜-regras não encontrado.")

            # Enviar dicas no canal 🗺️-dicas
            dicas_channel = get(guild.text_channels, name='🗺️-dicas')
            if dicas_channel:
                dicas_message = """
📜 **Dicas e Estratégias de Sea of Thieves** 📜

Se deseja tornar-se o pirata mais temido dos mares, estas dicas são para você:

- **Navegação Estelar**: Consulte sempre seu mapa e use as estrelas como guia! Navegar sem rumo pode levar seu navio direto para os rochedos ou nas garras do Kraken.

- **Tripulação Sincronizada**: O trabalho em equipe é o coração de qualquer tripulação. Divida as funções: enquanto um ajusta as velas, outro mantém um olho nas águas à frente. A comunicação é tão valiosa quanto ouro!

- **Combate Astuto**: Em terra ou no mar, lute com a sagacidade de um verdadeiro pirata. Use o terreno a seu favor, embosque seus inimigos e lembre-se: às vezes, uma retirada estratégica salva seu tesouro.

- **Caça ao Tesouro**: Mantenha suas ferramentas afiadas e seus mapas à mão. Leve sempre uma pá extra e fique atento aos enigmas das pistas. O tesouro não se revela facilmente!

- **Sobrevivência nas Ilhas**: Ao explorar territórios desconhecidos, estoque bananas, cocos e tábuas de reparo. Nunca se sabe quando esqueletos ou criaturas do mar podem atacá-lo.

- **Batalhas Navais**: Reconheça seus inimigos, sejam eles outros bucaneiros ou ameaças do próprio mar. Aprimore suas habilidades de canhoneiro e mantenha a pólvora seca.

Lembre-se, a vida de pirata é cheia de perigos e recompensas. Aventure-se, forme alianças e crie histórias que serão contadas nas tavernas por anos!
"""
                await dicas_channel.send(dicas_message)
                await ctx.send("🗺️ Mensagem de dicas enviada.")
            else:
                await ctx.send("⚠️ Canal 🗺️-dicas não encontrado.")
        except Exception as e:
            await ctx.send(f"⚠️ Erro ao enviar mensagens automáticas: {e}")

    except Exception as e:
        await ctx.send(f"⚠️ Erro durante a configuração dos canais: {e}")

# Comando para configurar o servidor com categorias, canais e roles
@bot.command()
@commands.has_permissions(administrator=True)
async def run(ctx):
    guild = ctx.guild

    await ctx.send("🚀 Iniciando a configuração do servidor...")

    existing_roles = await setup_roles(guild, ctx)
    await setup_channels(guild, existing_roles, ctx)

    await ctx.send("✅ Configuração completa do servidor.")

# Comando para atualizar a configuração do servidor
@bot.command()
@commands.has_permissions(administrator=True)
async def update(ctx):
    guild = ctx.guild

    await ctx.send("🔄 Iniciando a atualização da configuração do servidor...")

    bot.cancel_update = False  # Reinicia a flag de cancelamento

    existing_roles = await setup_roles(guild, ctx)
    if bot.cancel_update:
        await ctx.send("🛑 Atualização cancelada.")
        return
    await setup_channels(guild, existing_roles, ctx)
    if bot.cancel_update:
        await ctx.send("🛑 Atualização cancelada.")
        return

    await ctx.send("✅ Atualização completa do servidor.")

# Comando para cancelar o update
@bot.command()
@commands.has_permissions(administrator=True)
async def stop(ctx):
    if bot.cancel_update:
        await ctx.send("⚠️ Nenhuma atualização em andamento para ser cancelada.")
    else:
        bot.cancel_update = True
        await ctx.send("🛑 Atualização cancelada pelo usuário.")

# Comando de verificação para adicionar a role 'Verificado' e atribuir role apropriada
@bot.command()
async def verificar(ctx):
    unverified_role = get(ctx.guild.roles, name='🚫 Não Verificado')
    verified_role = get(ctx.guild.roles, name='✅ Verificado')
    adventurer_role = get(ctx.guild.roles, name='🌊 Aventureiro')
    if verified_role and unverified_role and adventurer_role:
        await ctx.author.add_roles(verified_role, adventurer_role)
        await ctx.author.remove_roles(unverified_role)
        await ctx.send(f'{ctx.author.mention}, você foi verificado e agora tem acesso ao servidor! 🎉')

        # Enviar mensagem de boas-vindas
        welcome_channel = get(ctx.guild.text_channels, name='🗣️-geral')
        if welcome_channel:
            welcome_message = f"""
🎉 **Bem-vindo ao Porto dos Ladrões!** 🎉

Ahoy, {ctx.author.mention}! Seja bem-vindo ao nosso porto seguro dos sete mares! Aqui, encontrarás uma tripulação destemida pronta para navegar, batalhar e descobrir tesouros inimagináveis!

🌊 **Como Navegar pelo Porto** 🌊

- **📜-regras**: O código dos piratas! Leia para conhecer as leis que regem nosso porto.
- **🗺️-dicas**: Um verdadeiro mapa do tesouro com dicas para aprimorar suas habilidades.
- **🗣️-geral**: Junte-se à taverna e compartilhe histórias, canções e aventuras com outros piratas.
- **🏴‍☠️-discussões**: Planeje expedições, forme alianças e prepare-se para enfrentar o desconhecido.

Estamos empolgados em tê-lo a bordo! Levante âncora, ajuste as velas e vamos juntos em busca de glória e riquezas. Que os ventos soprem a seu favor e que o rum nunca acabe! Arrr! 🏴‍☠️
"""
            await welcome_channel.send(welcome_message)
        else:
            await ctx.send("⚠️ Canal de boas-vindas não encontrado.")
    else:
        await ctx.send('⚠️ Roles necessárias não encontradas.')

# Comando para resetar o servidor, removendo todas as categorias, canais e roles criados
@bot.command()
@commands.has_permissions(administrator=True)
async def reset(ctx):
    await ctx.send("⚠️ Iniciando o processo de reset completo do servidor...")

    try:
        # Nome do canal privado de comandos que não deve ser deletado
        private_command_channel_name = '🔒-comandos'

        # Perguntar ao usuário se ele quer deletar o canal privado de comandos também
        await ctx.send(f"Deseja deletar o canal privado de comandos `{private_command_channel_name}`? Responda com `sim` ou `não`.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ['sim', 'não', 'nao']

        try:
            confirm_message = await bot.wait_for('message', timeout=30.0, check=check)
            if confirm_message.content.lower() == 'sim':
                delete_private_channel = True
                await ctx.send(f"🔒 O canal `{private_command_channel_name}` será deletado.")
            else:
                delete_private_channel = False
                await ctx.send(f"🔒 O canal `{private_command_channel_name}` será mantido.")
        except asyncio.TimeoutError:
            delete_private_channel = False
            await ctx.send("⏰ Tempo esgotado. O canal privado de comandos será mantido por padrão.")

        # Apagar todos os canais e categorias do servidor, exceto o canal privado de comandos (se não for deletado)
        for channel in ctx.guild.channels:
            if channel.name == private_command_channel_name and not delete_private_channel:
                continue
            try:
                await channel.delete()
            except Exception as e:
                await ctx.send(f"Não foi possível deletar o canal {channel.name}: {e}")
        if delete_private_channel:
            await ctx.send("🧹 Todos os canais e categorias foram removidos.")
        else:
            await ctx.send("🧹 Todos os canais e categorias (exceto o canal privado de comandos) foram removidos.")

        # Apagar todas as roles (exceto @everyone)
        for role in ctx.guild.roles:
            if role != ctx.guild.default_role:
                try:
                    await role.delete()
                    await ctx.send(f"Role '{role.name}' removida.")
                except Exception as e:
                    await ctx.send(f"Não foi possível remover a role '{role.name}': {e}")

        await ctx.send("🚫 Reset completo do servidor concluído. Pronto para configurar novamente com `!run`.")

    except Exception as e:
        await ctx.send(f"⚠️ Erro durante o reset: {e}")

# Anti-raid: bloquear envio de mensagens para não verificados e anti-spam de imagens
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Verifica se o usuário é o dono da ClownGuild ou tem permissão de administrador
    if '👑 Dono da ClownGuild' in [role.name for role in message.author.roles] or message.author.guild_permissions.administrator:
        await bot.process_commands(message)
        return

    # Se o usuário não tiver a role '✅ Verificado', bloquear mensagens fora do canal de verificação
    if '✅ Verificado' not in [role.name for role in message.author.roles]:
        if message.channel.name != '🔑-verificação':
            await message.delete()
            return

    # Anti-spam de imagens
    if len(message.attachments) > 5:
        await message.delete()
        await message.author.send('⚠️ Por favor, não envie tantas imagens de uma vez.')

    await bot.process_commands(message)

# Executar o bot usando o token a partir da variável de ambiente
bot.run(os.getenv('DISCORD_TOKEN'))
