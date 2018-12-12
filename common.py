class Record:
    def __init__(self):
        self.group_id = ''
        self.time = ''
        self.longtitude = 0.0
        self.latitude = 0.0


class Sunspot:
    def __init__(self):
        self.records = []


def getSunspotsFromRecords(records):
    sunspotById = dict()
    for record in records:
        if record.group_id == '':
            continue

        if not record.group_id in sunspotById:
            sunspotById[record.group_id] = Sunspot()
        sunspotById[record.group_id].records.append(record)

    return list(sunspotById.values())
