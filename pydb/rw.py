import pickle

def initialize():
    with open("file.db", 'wb') as db:
        db.seek(0)
        pickle.dump([], db)
        
def readall():
    with open("file.db", 'rb') as db:
        data = pickle.load(db)
        return data
def wdata(data=[], mode=0, offset=0):
    with open("file.db", 'ab') as db:
        db.seek(mode, offset)
        pickle.dump(data, db)

    
def rdata(data=[], mode=0, offset=0):
    with open("file.db", 'rb') as db:
        db.seek(mode, offset)
        data = pickle.load(db)
        return data





# Structure
'''[
['a', 'b'],
[],
[]
]
'''