from vendor.db import Db

# res = Db('class') \
#     .where('id', 999) \
#     .value('exam_core')
# print(res)
# res = Db('class') \
#     .find('id', 999)
# print(res)
# res = Db('class') \
#     .where('id', 999) \
#     .select()
# print(res)
res = Db('class') \
    .whereOr('exam_id', '1111') \
    .where('exam_id', '1233') \
    .save({'exam_id': '1111', 'exam_core': '500'})
    # .save({'id': 1308, 'exam_id': '66666'})
# print(res)

# res = Db('class') \
#     .where('exam_id', '1111') \
#     .update({'id': 1308, 'exam_id': '66666', 'exam_core': '88888'})
# .save({'exam_id': '1111', 'exam_core': '500'})
print(res)
exit(1)

res = Db('class').where()

a = db.get_one('select version()')
print(db)
