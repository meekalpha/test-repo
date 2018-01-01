class TimeSlot:
    def __init__(self, startTime, duration, available):
        self.startTime = startTime
        self.duration = duration
        self.available = available
        self.room_id = "200012227"

    def __str__(self):
        return '{} {} {} {}'.format(self.startTime, self.duration, self.available, self.room_id)
