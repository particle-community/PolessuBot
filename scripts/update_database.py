import asyncio

from sqlalchemy import delete
from config import sessionmaker
from database import Class
from scraper.polessu_data_scraper import PolessuDataScraper


async def update_group_schedule(group: str):
    group_schedule = PolessuDataScraper.get_group_class_schedule(group)

    async with sessionmaker() as session:
        async with session.begin():
            await session.execute(delete(Class).where(Class.study_group == group))

            for class_data in group_schedule:
                session.add(Class(**class_data))


async def main():
    groups_and_teachers = PolessuDataScraper.get_groups_and_teachers()
    groups = [group for group in groups_and_teachers if group.startswith('23ИТ')]

    for group in groups:
        await update_group_schedule(group)


if __name__ == '__main__':
    asyncio.run(main())
