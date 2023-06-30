import datetime


def get_time():
    """以字符串默认格式返回"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_interval(datetime_start,datetime_end):
    """计算时间间隔，以时分秒展示"""
    interval=datetime_end - datetime_start
    hours, remainder = divmod(interval.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    formatted_time_delta = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return formatted_time_delta


class Timer:
    """计时工具"""

    def __init__(self) -> None:
        self.records=[datetime.datetime.now()]

    def check(self):
        """记录一次时间，并且返回与上一次时间的间隔，以及总时间，以字符串形式表达"""
        self.records.append(datetime.datetime.now())
        interval=get_interval(self.records[-2],self.records[-1])

        result=[
            "开始时间: "+self.records[-2].strftime("%Y-%m-%d %H:%M:%S"),
            "结束时间: "+self.records[-1].strftime("%Y-%m-%d %H:%M:%S"),
            "持续时间: "+interval
        ]

        return "\n".join(result)+"\n"

    def get_records(self):
        """返回文记录的时间，以字符串内容返回"""
        return [i.strftime("%Y-%m-%d %H:%M:%S") for i in self.records]