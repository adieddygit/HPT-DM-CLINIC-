from sqlalchemy import insert

def insert_data(engine, table, **kwargs):
    with engine.connect()as connection:
        connection.execute(insert(table.__table__).values(**kwargs).prefix_with('IGNORE'))
        connection.commit()