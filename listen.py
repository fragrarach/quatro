from . import sql


def listen(config, task, else_task=None):
    print(f'Listening to channel {config.LISTEN_CHANNEL}')
    while 1:
        try:
            config.sigm_connection.poll()
        except:
            print('Database cannot be accessed, PostgreSQL service probably rebooting')
            try:
                config.sigm_connection.close()
                config.sigm_connection, config.sigm_db_cursor = sql.sigm_connect(config.LISTEN_CHANNEL)
                if config.log_connection:
                    config.log_connection.close()
                    config.log_connection, config.log_db_cursor = sql.log_connect()
            except:
                pass
            else:
                if else_task:
                    else_task()
        else:
            config.sigm_connection.commit()
            while config.sigm_connection.notifies:
                notify = config.sigm_connection.notifies.pop()
                task(config, notify)
