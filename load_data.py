import sqlite3
import csv

database = 'cell_count.db'
create_table_project = '''CREATE TABLE IF NOT EXISTS project( 
                                project_id INTEGER PRIMARY KEY
                                );'''
create_table_subject = '''CREATE TABLE IF NOT EXISTS subject(
                                subject_id INTEGER PRIMARY KEY,
                                project_id INTEGER,
                                age INTEGER NOT NULL,
                                sex TEXT NOT NULL,
                                treatment TEXT NOT NULL,
                                response TEXT,
                                condition TEXT NOT NULL,
                                FOREIGN KEY(project_id) 
                                    REFERENCES project(project_id)
                                    ON DELETE CASCADE 
                                    ON UPDATE NO ACTION
                                );'''
create_table_sample = '''CREATE TABLE IF NOT EXISTS sample(
                                sample_id INTEGER PRIMARY KEY,
                                subject_id INTEGER,
                                sample_type TEXT NOT NULL,
                                time_from_treatment_start INTEGER,
                                FOREIGN KEY(subject_id) 
                                    REFERENCES subject(subject_id)
                                    ON DELETE CASCADE 
                                    ON UPDATE NO ACTION
                                );'''

create_table_population_type = '''CREATE TABLE IF NOT EXISTS population_type(
                                    population_type_id INTEGER PRIMARY KEY,
                                    population_type TEXT NOT NULL UNIQUE
                                    );'''
create_table_population = '''CREATE TABLE IF NOT EXISTS population(
                                population_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                sample_id INTEGER,
                                population_type_id INTEGER,
                                cell_count INTEGER,
                                FOREIGN KEY(sample_id) 
                                    REFERENCES sample(sample_id)
                                    ON DELETE CASCADE 
                                    ON UPDATE NO ACTION
                                FOREIGN KEY(population_type_id)
                                    REFERENCES population_type(population_type_id)
                                );'''


insert_project_records = '''INSERT INTO project (project_id) 
                            VALUES(?)
                            ON CONFLICT(project_id) DO NOTHING'''

insert_subject_records = '''INSERT INTO subject (
                                subject_id, project_id, age, sex, treatment, response, condition
                            ) 
                            VALUES(?,?,?,?,?,?,?)
                            ON CONFLICT(subject_id) DO NOTHING'''

insert_sample_records = '''INSERT INTO sample (
                                sample_id, subject_id, sample_type, time_from_treatment_start
                            ) 
                            VALUES(?,?,?,?)
                            ON CONFLICT(sample_id) DO NOTHING'''

insert_population_records = '''INSERT INTO population (
                                    sample_id, population_type_id, cell_count
                                ) 
                                VALUES(?,?,?)'''

project_index = 0
subject_index = 1
condition_index = 2
age_index = 3
sex_index = 4
treatment_index = 5
response_index = 6
sample_index = 7
sample_type_index = 8
time_from_treatment_start_index = 9
b_cell_index = 10
cd8_t_cell_index = 11
cd4_t_cell_index = 12
nk_cell_index = 13
monocyte_index = 14

try: 
    with sqlite3.connect(database) as conn:
        print(f"Opened Sqlite cell count database with version {sqlite3.sqlite_version} successfully.")
        cursor = conn.cursor()

        #execute various table creations
        cursor.execute(create_table_project)
        cursor.execute(create_table_subject)
        cursor.execute(create_table_sample)
        cursor.execute(create_table_population_type)
        cursor.execute(create_table_population)
        print("Created all 5 tables")

        #fill enum tables
        cursor.execute("SELECT COUNT(*) FROM population_type")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany('INSERT INTO population_type (population_type) VALUES (?)',
                            [
                                ('b_cell',),
                                ('cd8_t_cell',),
                                ('cd4_t_cell',),
                                ('nk_cell',),
                                ('monocyte',),
                            ])

        #read in database data
        file = open('cell-count.csv')
        file_contents = csv.reader(file)

        #skip header row
        next(file_contents)

        for row in file_contents:
            project_id = int(row[project_index][3:])
            subject_id = int(row[subject_index][3:])
            sample_id = int(row[sample_index][6:])

            #insert project data
            cursor.execute(insert_project_records, (project_id,))

            #insert subject data
            age = row[age_index]
            sex = row[sex_index]
            treatment = row[treatment_index]
            response = row[response_index]
            condition = row[condition_index]
            cursor.execute(insert_subject_records, (subject_id, project_id, age, sex, treatment, response, condition))

            #insert sample data
            sample_type = row[sample_type_index]
            time_from_treatment_start = int(row[time_from_treatment_start_index])
            cursor.execute(insert_sample_records, (sample_id, subject_id, sample_type, time_from_treatment_start))

            #insert population data
            b_cell = row[b_cell_index]
            cd8_t_cell = row[cd8_t_cell_index]
            cd4_t_cell = row[cd4_t_cell_index]
            nk_cell = row[nk_cell_index]
            monocyte = row[monocyte_index]

            cursor.execute(insert_population_records, (sample_id, 1, b_cell))
            cursor.execute(insert_population_records, (sample_id, 2, cd8_t_cell))
            cursor.execute(insert_population_records, (sample_id, 3, cd4_t_cell))
            cursor.execute(insert_population_records, (sample_id, 4, nk_cell))
            cursor.execute(insert_population_records, (sample_id, 5, monocyte))
        
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)



conn.close()