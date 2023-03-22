db = [
    {"title":"abcd","content":1234},
    {"title":"bcde","content":1234},
    {"title":"cdef","content":1234},
]
keyword = "bc"
print(list(filter(lambda x:keyword in x["title"],db)))