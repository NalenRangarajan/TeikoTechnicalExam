import sqlite3
import json

database = "cell_count.db"

def get_population_type_size(cursor):
    cursor.execute("SELECT COUNT(*) FROM population_type")
    return cursor.fetchone()[0]

def get_cell_count_from_population(cursor, sample_id, population_type_id):
    cursor.execute(f"SELECT cell_count FROM population WHERE population.sample_id = {sample_id} AND population_type_id = {population_type_id}")
    return cursor.fetchone()[0]

def get_population_type_name_from_population_type_id(cursor, population_type_id):
    cursor.execute(f"SELECT population_type FROM population_type WHERE population_type_id = {population_type_id}")
    return cursor.fetchone()[0]

def total_cell_count(cursor, sample_id, pop_type_cnt):
    cell_count_index = 3
    total_count = 0
    for i in range(1, pop_type_cnt + 1):
        total_count += get_cell_count_from_population(cursor, sample_id, i)

    return total_count

def get_inital_analysis_row_data(cursor, row):
    sample_id = row[0]
    total_count = total_cell_count(cursor, sample_id, get_population_type_size(cursor))
    population_list = list()
    for i in range(1, get_population_type_size(cursor) + 1):
        population_name = get_population_type_name_from_population_type_id(cursor, i)
        population_count = get_cell_count_from_population(cursor, sample_id, i)
        percentage = (population_count / total_count) * 100
        percentage = round(percentage, 2)
        population_list.append({
                            "name": population_name, 
                            "count": population_count, 
                            "percentage": percentage
                        })

    return sample_id, total_count, population_list

def get_part_three_data(cursor):

    
def main():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sample")
        rows = cursor.fetchall()
        data = []
        print("Before Data analysis")
        i = 0
        for row in rows:
            if i <= 100: #FIX ME REMOVER
                row_data = get_inital_analysis_row_data(cursor, row)
                data.append({
                            "sample_id": row_data[0], 
                            "total_count": row_data[1],
                            "population_list": row_data[2]
                            })
            i = i + 1
        print("Writing JSON")
        with open("table_data.json", "w") as file:
            json.dump(data, file, indent=4)
        print("JSON written")

        cursor.execute("SELECT * FROM subject WHERE")
        rows = cursor.fetchall()

if __name__ == "__main__":
    main()