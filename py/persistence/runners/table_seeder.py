from persistence.seeders import seed_user_table


# Seeds all tables in db
def seed_fly_dams():
    seed_user_table()


seed_fly_dams()
