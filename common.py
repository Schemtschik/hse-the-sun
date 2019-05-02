class Record:
    def __init__(self):
        self.group_id = 0
        self.time = ''
        self.longtitude = 0.0
        self.latitude = 0.0
        self.area = 0
        self.old = False
        self.previous_id = 0


class Sunspot:
    def __init__(self):
        self.id = 0
        self.records = []
        self.area = 0
        self.filtered = False
        self.old = False
        self.previous_id = 0

def getSunspotsFromRecords(records):
    sunspotById = dict()
    for record in records:
        if not record.group_id in sunspotById:
            sunspotById[record.group_id] = Sunspot()
            sunspotById[record.group_id].id = record.group_id

        sunspotById[record.group_id].records.append(record)

        sunspotById[record.group_id].area = max(x.area for x in sunspotById[record.group_id].records)

        if (record.old):
            sunspotById[record.group_id].old = True
            sunspotById[record.group_id].previous_id = record.previous_id

    return list(sunspotById.values())
