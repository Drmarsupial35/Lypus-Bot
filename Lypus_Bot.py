import datetime
from datetime import datetime
import discord
from discord.ext import commands
import time

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Message lors du lancement du Bot et sa connexion au serveur
@bot.event
async def on_ready():
    print('*** CONNEXION EN TANT QUE : {0.user}'.format(bot),' ***')
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name='PLAY.LYPUS.FR'))

# Ecrit un message de bienvenue lorsqu'un joueur rejoins le serveur
@bot.event
async def on_member_join(member):
    guild = bot.get_guild(633340885727182859)
    wlc_channel = guild.get_channel(783748707174580234)
    membre_role = guild.get_role(705797996947963927)
    regles_channel = guild.get_channel(775479065414074398)

    embed = discord.Embed(title= member.name, description=f"Bienvenue sur le serveur {member.mention} !\nPour obtenir le grade {membre_role.mention} il faut que tu lises les {regles_channel.mention}", color=0xc83737)
    embed.set_thumbnail(url=member.avatar_url)
    await wlc_channel.send(embed=embed)
    print(f"{getDate()} - Bienvenue : {member.name}")


# Ajoute le role Membre si l'utilisateur coche les règles
@bot.event
async def on_raw_reaction_add(payload):
    guild = bot.get_guild(633340885727182859) # Le serveur Lypus
    rgl_channel = bot.get_channel(payload.channel_id)
    member = guild.get_member(payload.user_id)    # L'utilisateur

    if payload.message_id == 789906282970349598:
        if not (payload.user_id == bot.user.id):
            if payload.emoji.id == 789674441519923220:
                membre = guild.get_role(705797996947963927)   # Le role @Membre
                await member.add_roles(membre)
                print(f"{getDate()} - Ajout du role Membre à {member.name}")
            else:
                if not (payload.user_id == bot.user.id):
                    await msg.remove_reaction(payload.emoji.name, member)


# Supprime le role Membre si l'utilisateur décoche les règles
@bot.event
async def on_raw_reaction_remove(payload):
    guild   = bot.get_guild(633340885727182859) # Le serveur Lypus
    member  = guild.get_member(payload.user_id)

    if payload.message_id == 789906282970349598:
        if payload.emoji.id == 789674441519923220:
            membre = guild.get_role(705797996947963927)   # Le role @Membre
            await member.remove_roles(membre)
            print(f"{getDate()} - Suppression du role Membre de {member.name}")

#Lorsqu'un message est envoyé
@bot.event
async def on_message(message):
    content = message.content
    channel = message.channel
    if content.upper() in ["CC","SALUT","YO","SLT","HEY","BONJOUR"]:
        await message.add_reaction('👋')
    elif content == "ping":
        await channel.send("pong")
    await bot.process_commands(message) # Permet de lancer les autres fonctions à l'envoi d'un message

# Supprime les x derniers messages du channel
@bot.command()
async def purge(ctx, *arg):
    guild = bot.get_guild(633340885727182859)
    staff_role = guild.get_role(782372692706852884)

    channel = ctx.channel
    author  = ctx.author
    if staff_role in author.roles :
        if len(arg) < 1:
            await channel.send(f"{author.mention} La commande {ctx.command} demande 1 argument (le nombre de messages que vous voulez supprimer)")
        else:
            nb = arg[0]
            if nb == "all":
                nb = "10000"
            if nb.isdigit():
                nb = int(nb)+1
                deletedMsg = await channel.purge(limit=int(nb), check=None)
                nb2 = len(deletedMsg) -1
                dm = await author.create_dm()
                await dm.send(f"Vous avez bien supprimé {nb2} messages dans le salon **{channel.name}**")
                print(f"{getDate()} - Suppression de {nb2} messages par {author.name}")
            else:
                await channel.send(f"{author.mention} Cette commande demande un nombre comme argument")
    else :
        await channel.send(f"{author.mention} Vous n'avez pas la permission d'utiliser cette commande !")


@bot.command()
async def poll(ctx, *arg):
    guild = bot.get_guild(633340885727182859)
    staff_role = guild.get_role(782372692706852884)
    mbr_role = guild.get_role(705797996947963927)

    channel = ctx.channel
    author  = ctx.author
    message = ctx.message
    if staff_role in author.roles :
        if len(arg) < 1:
            await channel.send(f"{author.mention} Il faut un texte pour créer un sondage !")
        else:
            await message.delete()
            txt = mbr_role.mention + "\n" + ' '.join(arg)
            poll = await channel.send(txt)
            await poll.add_reaction(bot.get_emoji(789674441519923220))
            await poll.add_reaction(bot.get_emoji(789674658944253972))
            print(f"{getDate()} - Création d'un sondage par {author.name}")
    else :
        await channel.send(f"{author.mention} Vous n'avez pas la permission d'utiliser cette commande !")

@bot.command()
async def warn(ctx, *arg):
    guild = bot.get_guild(633340885727182859)
    staff_role = guild.get_role(782372692706852884)

    channel = ctx.channel
    author  = ctx.author

    if staff_role in author.roles :
        if len(arg) < 1:
            await channel.send(f"{author.mention} Il faut un pseudo pour pouvoir warn quelqu'un !")
        elif len(arg) < 2:
            await channel.send(f"{author.mention} Il faut une raison pour warn quelqu'un !")
        else:
            try:
                member = guild.get_member(int(((arg[0].split("!"))[1].split(">"))[0]))
                warn = guild.get_role(805134899845267466)
                if warn in member.roles :
                    await channel.send(f"{author.mention} Ce joueur a déjà été warn !")
                else:
                    dm_member = await member.create_dm()
                    dm_author = await author.create_dm()
                    raison = ' '.join(arg[1:])

                    await member.add_roles(warn)
                    await dm_member.send(f"Vous avez été warn par **{author.name}** pour la raison suivante :\n*{raison}*")
                    await dm_author.send(f"Vous avez bien warn **{member.name}** pour la raison suivante :\n*{raison}*")

                    print(f"{getDate()} - Le joueur {member.name} a été warn par {author.name}")

            except IndexError:
                await channel.send(f"{author.mention} Le premier argument doit être la mention d'un joueur !")
    else :
        await channel.send(f"{author.mention} Vous n'avez pas la permission d'utiliser cette commande !")

@bot.command()
async def unwarn(ctx, *arg):
    guild = bot.get_guild(633340885727182859)
    staff_role = guild.get_role(782372692706852884)

    channel = ctx.channel
    author  = ctx.author

    if staff_role in author.roles :
        if len(arg) < 1:
            await channel.send(f"{author.mention} Il faut un pseudo pour pouvoir unwarn quelqu'un !")
        else:
            try:
                warn = guild.get_role(805134899845267466)
                member = guild.get_member(int(((arg[0].split("!"))[1].split(">"))[0]))

                if warn not in member.roles:
                    await channel.send(f"{author.mention} Ce joueur n'a jamais été warn !")
                else :
                    dm_member = await member.create_dm()
                    dm_author = await author.create_dm()

                    await member.remove_roles(warn)
                    await dm_member.send(f"Vous avez été unwarn par **{author.name}**")
                    await dm_author.send(f"Vous avez bien unwarn **{member.name}**")

                    print(f"{getDate()} - Le joueur {member.name} a été unwarn par {author.name}")

            except IndexError:
                await channel.send(f"{author.mention} Vous devez mentionnez quelqu'un !")
    else:
        await channel.send(f"{author.mention} Vous n'avez pas la permission d'utiliser cette commande !")


def getDate():
    date = datetime.today()
    day = str(date.day)
    month = str(date.month)
    hour = str(date.hour)
    minute = str(date.minute)

    if len(day) == 1:
        day = "0" + day
    if len(month) == 1:
        month = "0" + month
    if len(hour) == 1:
        hour = "0" + hour
    if len(minute) == 1:
        minute = "0" + minute

    date = f"{day}/{month} {hour}h{minute}"
    return date


bot.run('BOT TOKEN HERE')
