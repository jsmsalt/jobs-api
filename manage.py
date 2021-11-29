import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Migration management tool')

    parser.add_argument(
        '-mm',
        '--makemigrations',
        type=str,
        dest='makemigrations',
        nargs='?',
        const='unnamed',
        default=None,
        help='Make migration script'
    )

    parser.add_argument(
        '-m',
        '--migrate',
        type=bool,
        dest='migrate',
        nargs='?',
        const=True,
        default=False,
        help='Apply migration scripts'
    )

    parser.add_argument(
        '-d',
        '--downgrade',
        type=str,
        dest='downgrade',
        nargs='?',
        const=-1,
        default=None,
        help='Downgrade to a specific revision'
    )

    args = parser.parse_args()
    makemigrations = args.makemigrations
    migrate = args.migrate
    downgrade = args.downgrade

    if migrate:
        print('Migrating...')
        os.system('alembic upgrade head')
    elif makemigrations is not None:
        print(f"Making migration script '{makemigrations}'...")
        os.system(f"alembic revision --autogenerate -m '{makemigrations}'")
    elif downgrade is not None:
        print(f"Downgrading to revision {downgrade}...")
        os.system(f"alembic downgrade {downgrade}")


if __name__ == '__main__':
    main()
