import variables

class Helper:
    async def get_user_id(socket_id):
        return await variables.userIds[socket_id]

    async def get_socket_id(user_id):
        return await variables.socketIds[user_id]