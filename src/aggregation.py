import asyncio
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


class Aggregation:
    def __init__(self):
        self.__client = MongoClient(os.getenv('URI'))
        self.__db = self.__client['sampleDB']
        self.__collection = self.__db['sample_collection']

    async def convert_datetime(self,
                               input_data: Dict) -> Tuple[datetime, datetime]:
        """Конвертирует дату и время из формата ISO в datetime."""
        return (datetime.fromisoformat(input_data.get('dt_from')),
                datetime.fromisoformat(input_data.get('dt_upto')))

    async def find_data(self,
                        dt_from: datetime,
                        dt_upto: datetime) -> List[Dict[int, datetime]]:
        """Поиск данных в БД в указанном диапазоне дат."""
        query = {
            'dt': {
                '$gte': dt_from,
                '$lt': dt_upto
            }
        }
        projection = {
            '_id': 0,
            'value': 1,
            'dt': 1
        }
        return list(self.__collection.find(query, projection))

    async def aggregate_month(self,
                              data: List,
                              dt_from: datetime,
                              dt_upto: datetime) -> Tuple[List, List]:
        """Агрегирует данные по месяцам в указанном диапазоне дат."""
        dataset = []
        labels = []
        month_amount = ((dt_upto.year - dt_from.year) * 12 +
                        dt_upto.month - dt_from.month)
        for i in range(month_amount + 1):
            curr_month = datetime(
                dt_from.year + ((dt_from.month + i - 1) // 12),
                ((dt_from.month + i - 1) % 12) + 1, 1)
            dataset.append(sum((item.get('value') for item in data if
                               item.get('dt').year == curr_month.year and
                               item.get('dt').month == curr_month.month)))
            labels.append(curr_month.isoformat())
        return dataset, labels

    async def aggregate_day(self,
                            data: List,
                            dt_from: datetime,
                            dt_upto: datetime) -> Tuple[List, List]:
        """Агрегирует данные по дням в указанном диапазоне дат."""
        dataset = []
        labels = []
        day_amount = (dt_upto - dt_from).days
        for i in range(day_amount + 1):
            curr_day = dt_from + timedelta(days=i)
            dataset.append(sum((item.get('value') for item in data if
                                item.get('dt').year == curr_day.year and
                                item.get('dt').month == curr_day.month and
                                item.get('dt').day == curr_day.day)))
            labels.append(curr_day.isoformat())
        return dataset, labels

    async def aggregate_hour(self,
                             data: List,
                             dt_from: datetime,
                             dt_upto: datetime) -> Tuple[List, List]:
        """Агрегирует данные по часам в указанном диапазоне дат."""
        dataset = []
        labels = []
        hour_amount = int((dt_upto - dt_from).total_seconds() / 3600)
        for i in range(hour_amount + 1):
            curr_hour = dt_from + timedelta(hours=i)
            dataset.append(sum((item.get('value') for item in data if
                                item.get('dt').year == curr_hour.year and
                                item.get('dt').month == curr_hour.month and
                                item.get('dt').day == curr_hour.day and
                                item.get('dt').hour == curr_hour.hour)))
            labels.append(curr_hour.isoformat())
        return dataset, labels

    async def get_result(self, input_data: Dict) -> Dict:
        """
        Основная функция класса для агрегации данных по заданным параметрам
        (месяцам, дням, часам).
        """
        try:
            dt_from, dt_upto = await self.convert_datetime(input_data)
            data = await self.find_data(dt_from, dt_upto)
            group_type = input_data.get('group_type')
            dataset = []
            labels = []

            if group_type == 'month':
                dataset, labels = await self.aggregate_month(data,
                                                             dt_from, dt_upto)
            elif group_type == 'day':
                dataset, labels = await self.aggregate_day(data,
                                                           dt_from, dt_upto)
            elif group_type == 'hour':
                dataset, labels = await self.aggregate_hour(data,
                                                            dt_from, dt_upto)
            else:
                return 'Невалидный запрос. Пример запроса:\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'  # noqa: E501
            return {'dataset': dataset, 'labels': labels}
        except Exception:
            return 'Невалидный запрос. Пример запроса:\n{"dt_from": "2022-09-01T00:00:00", "dt_upto": "2022-12-31T23:59:00", "group_type": "month"}'  # noqa: E501

    def conn_close(self) -> None:
        """Закрывает соединение с БД."""
        if self.__client:
            self.__client.close()
            self.__client = None


if __name__ == '__main__':
    data = [
        {
            'dt_from': '2022-09-01T00:00:00',
            'dt_upto': '2022-12-31T23:59:00',
            'group_type': 'month'
        },
        {
            'dt_from': '2022-10-01T00:00:00',
            'dt_upto': '2022-11-30T23:59:00',
            'group_type': 'day'
        },
        {
            'dt_from': '2022-02-01T00:00:00',
            'dt_upto': '2022-02-02T00:00:00',
            'group_type': 'hour'
        }
    ]

    aggregation = Aggregation()

    async def main():
        for item in data:
            result = await aggregation.get_result(item)
            print(result, '\n')
        aggregation.conn_close()

    asyncio.run(main())
