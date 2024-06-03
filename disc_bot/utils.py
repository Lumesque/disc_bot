from .server_data import servers

def is_admin(ctx):
    server_admin_list = servers.get_server(ctx.guild.id).get("admin_ids", [])
    roles = ctx.author.roles
    print(roles)
    print(server_admin_list)
    if any(str(role.id) in server_admin_list for role in roles):
        return True
    else:
        return False
