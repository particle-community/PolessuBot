import re
from datetime import datetime, timedelta

from scraper.html_document_manager import HtmlDocumentManager


class PolessuDataScraper:
    __MAIN_ADDRESS = "https://www.polessu.by/ruz/"

    @staticmethod
    def get_groups_and_teachers() -> list[str]:
        document = HtmlDocumentManager.get_document(PolessuDataScraper.__MAIN_ADDRESS)

        script_tag_content = document.select('body script:last-child')[0].text

        match = re.search(r'query\s*=\s*\[([\s\S]*?)]', script_tag_content)

        return [item.strip(" \'") for item in match.group(1).split(',')] if match else []

    @staticmethod
    def get_group_class_schedule(study_group: str) -> list[dict]:
        classes = []

        documents = HtmlDocumentManager.get_documents([
            f"{PolessuDataScraper.__MAIN_ADDRESS}?f=1&q={study_group}",
            f"{PolessuDataScraper.__MAIN_ADDRESS}?f=2&q={study_group}",
            f"{PolessuDataScraper.__MAIN_ADDRESS}/term2?f=1&q={study_group}",
            f"{PolessuDataScraper.__MAIN_ADDRESS}/term2?f=2&q={study_group}"
        ])

        day_of_week = {
            "Понедельник": 0,
            "Вторник": 1,
            "Среда": 2,
            "Четверг": 3,
            "Пятница": 4,
            "Суббота": 5
        }

        for document in documents:
            table_rows = document.select("#weeks-filter tr")
            if not table_rows:
                continue

            day_number = 0

            for table_row in table_rows:
                if "wa" in table_row.get("class"):
                    day_number = day_of_week[table_row.find("th").text]
                    continue

                week_numbers = (int(week_number[1:]) for week_number in table_row.get("class")[:-1])  # example 'w0 w15'

                row_cells = table_row.find_all("td")

                start_time_string = row_cells[0].text.split('-')[0].split(':')

                subject_content = row_cells[1].text  # '(week_numbers) subject_name'
                subject_name = subject_content[subject_content.index(")") + 2:]  # 'subject_name'

                room = row_cells[2].text
                teacher = row_cells[3].text
                subgroup = row_cells[4].text

                # [Hack start]
                week_button_text = document.select(".btn-group .btn-primary")[1].text.split()[1]  # '1-20' or '21-24'
                week_page = int(week_button_text[0]) - 1  # 0 or 1

                term_button_text = document.select(".btn-group .btn-primary")[0].text[0] # 1 or 2
                term_page = int(term_button_text) - 1 # 0 or 1
                # [Hack end]

                for week_number in week_numbers:
                    start_time = PolessuDataScraper.get_start_date() + timedelta(
                        weeks=week_number + 20 * week_page + 23 * term_page,
                        days=day_number,
                        hours=int(start_time_string[0]),
                        minutes=int(start_time_string[1]),
                        seconds=0
                    )

                    classes.append({
                        "study_group": study_group,
                        "start_time": start_time,
                        "subject_name": subject_name,
                        "room": room or None,
                        "teacher": teacher or None,
                        "subgroup": subgroup or None
                    })

        return classes

    @staticmethod
    def get_start_date() -> datetime:
        return datetime(year=2023, month=9, day=4)
