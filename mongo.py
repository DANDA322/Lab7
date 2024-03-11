import pymongo
from bson import Code

client = pymongo.MongoClient("mongodb://mongo:secret@localhost:27017")
db = client["db"]

print("1. Все певцы")


def get_all_singers():
    singers = db.singers.find()
    for singer in singers:
        print(singer)


get_all_singers()

print("2.Все концерты где Stadium_ID: 1")
concerts_in_stadium = db.concerts.find({"Stadium_ID": "1"})
for concert in concerts_in_stadium:
    print(concert)

print("3. Добавление нового певца")
new_singer = {"Singer_ID": 7, "Name": "test", "Country": "Russia", "Song_Name": "test", "Song_release_year": "2024",
              "Age": 22, "Is_male": "T"}
result = db.singers.insert_one(new_singer)
print(result)

get_all_singers()

print("4. Обновить поле")
result_update = db.singers.update_one({"Singer_ID": 7}, {"$set": {"Name": "new name"}})
print(result_update)
get_all_singers()

print("5. Удалить документ")
result = db.singers.delete_one({"Singer_ID": 7})
print(result)
get_all_singers()

print("6. Подсчитать количество певцов по полу")
singers = db.singers.aggregate([
    {"$group": {"_id": "$Is_male", "count": {"$sum": 1}}}
])
for result in singers:
    print(result)

print("7. Найти средний возраст всех певцов")
age = db.singers.aggregate([
    {"$group": {"_id": None, "average_age": {"$avg": "$Age"}}}
])
for result in age:
    print(result)

print("8. Изменение типа поля")
result = db.concerts.update_many(
    {},  # Фильтр для выбора всех документов в коллекции
    [{"$set": {"Stadium_ID": {"$toInt": "$Stadium_ID"}}}]  # Изменение типа поля
)
print(result)

print("9. Найти концерты в стадионе с вместимостью более 10000")
stadiums = db.stadiums.aggregate([
    {"$match": {"Capacity": {"$gt": 10000}}},
    {"$lookup": {
        "from": "concerts",
        "localField": "Stadium_ID",
        "foreignField": "Stadium_ID",
        "as": "concerts_info"
    }}
])
for result in stadiums:
    print(result)

print("10. Cреднее количество зрителей на концертах для каждого стадиона")
pipeline = [
    {
        "$lookup": {
            "from": "stadiums",  # Коллекция для объединения
            "localField": "Stadium_ID",  # Поле в текущей коллекции
            "foreignField": "Stadium_ID",  # Поле в коллекции для объединения
            "as": "stadium_info"  # Название нового поля с результатами объединения
        }
    },
    {
        "$unwind": "$stadium_info"  # Развертывание массива stadium_info
    },
    {
        "$group": {
            "_id": "$stadium_info.Name",  # Группировка по имени стадиона
            "averageVisitors": {"$avg": "$stadium_info.Average"}  # Расчет среднего количества зрителей
        }
    },
    {
        "$sort": {"averageVisitors": -1}  # Сортировка по убыванию среднего количества зрителей
    }
]

results = db.concerts.aggregate(pipeline)
for result in results:
    print(result)

# print("Количество концертов по стадионам")
# map = """
# function() {
#   emit(this.Stadium_ID, 1);
# }
# """
#
# reduce = """
# function(key, values) {
#   return Array.sum(values);
# }
# """
#
# result = db.concerts.map_reduce(map, reduce, "concert_counts_by_stadium")
# for doc in result.find():
#   print(doc)
