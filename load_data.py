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
                                subject_id INTEGER
                                sample_type TEXT NOT NULL,
                                time_from_treatment_start INTEGER,
                                FOREIGN KEY(subject_id) 
                                    REFERENCES subject(subject_id)
                                    ON DELETE CASCADE 
                                    ON UPDATE NO ACTION
                                );'''
create_table_population = '''CREATE TABLE IF NOT EXISTS population(
                                population_id INTEGER PRIMARY KEY,
                                sample_id INTEGER,
                                cell_count INTEGER,
                                FOREIGN KEY(sample_id) 
                                    REFERENCES sample(sample_id)
                                    ON DELETE CASCADE 
                                    ON UPDATE NO ACTION
                                );'''

try: 
    with sqlite3.connect(database) as conn:
        print(f"Opened Sqlite cell count database with version {sqlite3.sqlite_version} successfully.")
        cursor = conn.cursor()

        cursor.execute(create_table_project)
        cursor.execute(create_table_subject)
        cursor.execute(create_table_sample)
        cursor.execute(create_table_population)
        print("Created all 4 tables")

        
except sqlite3.OperationalError as e:
    print("Failed to open database:", e)



conn.close()