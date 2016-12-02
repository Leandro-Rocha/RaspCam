import json
import os
from subprocess import check_output

import gps

GPS_LOG = "../../data/gps_history.txt"


def main():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    f = open(GPS_LOG, 'a', 0)

    while True:
        try:
            report = session.next()

            if report['class'] == 'TPV':
                json_str = json.dumps(
                    {'time': report.time,
                     'lat': report.lat,
                     'lon': report.lon,
                     # 'climb': report.climb,
                     # 'alt': report.a321lt,
                     'speed': report.speed},
                    separators=(',', ':'))

                f.write(json_str + "\n")
        except KeyboardInterrupt:
            break
        except:
            pass


def get_last_entry():
    return json.loads(check_output(['tail', '-1', GPS_LOG]))


if __name__ == '__main__':
    main()
