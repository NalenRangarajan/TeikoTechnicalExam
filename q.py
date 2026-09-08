import sqlite3

database = "cell_count.db"

with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(population.cell_count)
            FROM population
            JOIN sample
                ON population.sample_id = sample.sample_id
            JOIN subject
                ON sample.subject_id = subject.subject_id
            JOIN population_type
                ON population.population_type_id = population_type.population_type_id
            WHERE subject.condition = ?
            AND subject.sex = ?
            AND subject.response = ?
            AND sample.time_from_treatment_start = ?
            AND population_type.population_type = ?
        """, ("melanoma", "M", "yes", 0, "b_cell"))

        average = cursor.fetchone()[0]

        print(average)