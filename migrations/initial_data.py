from settings import Settings
from helpers.password import hash_password

# ################
#  ALEMBIC SCRIPT
# ################
#
# from migrations.initial_data import tables
#
# def upgrade():
#     meta = sa.MetaData(bind=op.get_bind())
#     for table_name, rows in tables.items():
#         table = sa.Table(table_name, meta, autoload=True)
#         op.bulk_insert(table, rows)
#
# def downgrade():
#     meta = sa.MetaData(bind=op.get_bind())
#     meta.drop_all(bind=op.get_bind())

settings = Settings()

tables = {
    'roles': [
        {'name': 'admin'},  # 01
        {'name': 'user'},  # 02
    ],
    'permissions': [
        {'name': 'user.write'},  # 01
        {'name': 'user.read'},  # 02
        {'name': 'user.update'},  # 03
        {'name': 'user.delete'},  # 04
        {'name': 'user.link'},  # 05
        {'name': 'user.*'},  # 06

        {'name': 'job.write'},  # 07
        {'name': 'job.read'},  # 08
        {'name': 'job.update'},  # 09
        {'name': 'job.delete'},  # 10
        {'name': 'job.link'},  # 11
        {'name': 'job.*'},  # 12

        {'name': 'session.write'},  # 13
        {'name': 'session.read'},  # 14
        {'name': 'session.update'},  # 15
        {'name': 'session.delete'},  # 16
        {'name': 'session.link'},  # 17
        {'name': 'session.*'},  # 18

        {'name': 'role.write'},  # 19
        {'name': 'role.read'},  # 20
        {'name': 'role.update'},  # 21
        {'name': 'role.delete'},  # 22
        {'name': 'role.link'},  # 23
        {'name': 'role.*'},  # 24

        {'name': 'permission.write'},  # 25
        {'name': 'permission.read'},  # 26
        {'name': 'permission.update'},  # 27
        {'name': 'permission.delete'},  # 28
        {'name': 'permission.link'},  # 29
        {'name': 'permission.*'},  # 30
    ],
    'permission_role_link': [
        # Admin
        {'role_id': 1, 'permission_id': 6},
        {'role_id': 1, 'permission_id': 12},
        {'role_id': 1, 'permission_id': 18},
        {'role_id': 1, 'permission_id': 24},
        {'role_id': 1, 'permission_id': 30},

        # User
        {'role_id': 2, 'permission_id': 12},
    ],
    'users': [
        {
            'username': 'admin',
            'email': 'jsmsalt@outlook.com',
            'password': hash_password(settings.admin_password),
            'role_id': 1
        },
    ]
}
