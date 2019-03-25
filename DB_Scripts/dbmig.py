import psycopg2, csv, datetime
from dateutil.parser import parse

try:
    connection = psycopg2.connect(user = "django", password = "password", host="127.0.0.1", port="5432", database = "iott7")
    cursor = connection.cursor()
    with open('all_readings.csv') as readings:
        csv_reader = csv.reader(readings, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count = line_count + 1
            index = row[0]
            created_time = parse(row[1])
            updated_time = parse(row[2])
            pir_val = 1
            if row[3] == 'f':
                pir_val = 0
            temp = int(row[4])
            light = int(row[5])
            ultra = float(row[6])
            facility_id = int(row[7])
            print(created_time)
            cursor.execute('INSERT INTO iot_facility_reading2 (id, created_at, updated_at, reading_type, value, facility_id) VALUES (%s, %s, %s, %s, %s, %s)', (line_count, created_time, updated_time, "ultra", ultra, 1))
            line_count = line_count + 1
            cursor.execute('INSERT INTO iot_facility_reading2 (id, created_at, updated_at, reading_type, value, facility_id) VALUES (%s, %s, %s, %s, %s, %s)', (line_count, created_time, updated_time, "pir", float(pir_val), 1))
            line_count = line_count + 1
            cursor.execute('INSERT INTO iot_facility_reading2 (id, created_at, updated_at, reading_type, value, facility_id) VALUES (%s, %s, %s, %s, %s, %s)', (line_count, created_time, updated_time, "temp", float(temp), 1))
            line_count = line_count + 1
            cursor.execute('INSERT INTO iot_facility_reading2 (id, created_at, updated_at, reading_type, value, facility_id) VALUES (%s, %s, %s, %s, %s, %s)', (line_count, created_time, updated_time, "light", float(light), 1))
        connection.commit()
except(Exception, psycopg2.Error) as error :
    print("error while connecting ", error)

