from .server_data import servers


def is_admin(ctx):
    server_admin_list = servers.get_server(ctx.guild.id).get("admin_ids", [])
    roles = ctx.author.roles
    return ctx.author == ctx.author.guild.owner or any(role.id in server_admin_list for role in roles)


def is_blacklisted(ctx):
    server_blacklisted_list = servers.get_server(ctx.guild.id).get("blacklisted_channels", [])
    channel_id = ctx.channel.id
    return channel_id not in server_blacklisted_list


def startup_check(ctx): # noqa ARG001
    return False
