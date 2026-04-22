lst = [{"Asian":"Exterior - Ace,Apex","id":1},{"Asian":"Interior - Tractor,Premimium,Royale","id":2}]
def find_details(id):
    for items in lst:
        if items["id"]==id:
            print(items)
find_details(lst)