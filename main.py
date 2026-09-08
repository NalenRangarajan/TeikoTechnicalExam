import sqlite3
import json
import scipy.stats as stats

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

def get_sample_row_data(cursor, row):
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
    
def main():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        #Part 2 querying
        cursor.execute("SELECT * FROM sample")
        rows = cursor.fetchall()
        data = []
        print("Before Data analysis")
        i = 0
        for row in rows:
            if i <= 100: #FIX ME REMOVER
                row_data = get_sample_row_data(cursor, row)
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

        #Part 3 querying
        condition = "melanoma"
        treatment = "miraclib"
        response = "no"
        sample_type = "PBMC"

        cursor.execute("SELECT subject_id FROM subject WHERE treatment = ? AND condition = ? AND response = ?", (treatment, condition, response))
        no_rows = cursor.fetchall()

        response = "yes"
        cursor.execute("SELECT subject_id FROM subject WHERE treatment = ? AND condition = ? AND response = ?", (treatment, condition, response))
        yes_rows = cursor.fetchall()

        b_cell_list_no = []
        cd8_t_cell_list_no = []
        cd4_t_cell_list_no = []
        nk_cell_list_no = []
        monocyte_list_no = []
        b_cell_list_yes = []
        cd8_t_cell_list_yes = []
        cd4_t_cell_list_yes = []
        nk_cell_list_yes = []
        monocyte_list_yes = []
        
        all_samples = []
        no_subject_ids = [row[0] for row in no_rows]
        no_samples = []
        if no_subject_ids:
            ids = ",".join("?" * len(no_subject_ids))
            cursor.execute(
                f"SELECT * FROM sample WHERE subject_id IN ({ids}) AND sample_type = ?", 
                (*no_subject_ids, sample_type)
            )
            no_samples = cursor.fetchall()
            i = 0
            for sample in no_samples:
                if i <= 100: #fix me remover
                    sample_data = get_sample_row_data(cursor, sample)
                    all_samples.append(
                        {
                            "sample_id": sample_data[0],
                            "response": "no",
                            "population_list": sample_data[2]
                        }
                    )
                    b_cell_list_no.append(sample_data[2][0]["percentage"])
                    cd8_t_cell_list_no.append(sample_data[2][1]["percentage"])
                    cd4_t_cell_list_no.append(sample_data[2][2]["percentage"])
                    nk_cell_list_no.append(sample_data[2][3]["percentage"])
                    monocyte_list_no.append(sample_data[2][4]["percentage"])
                i = i + 1
                    

        yes_subject_ids = [row[0] for row in yes_rows]
        yes_samples = []
        if yes_subject_ids:
            ids = ",".join("?" * len(yes_subject_ids))
            cursor.execute(
                f"SELECT * FROM sample WHERE subject_id IN ({ids}) AND sample_type = ?", 
                (*yes_subject_ids, sample_type)
            )
            yes_samples = cursor.fetchall()
            i = 0
            for sample in yes_samples:
                if i <= 100: #fix me remover
                    sample_data = get_sample_row_data(cursor, sample)
                    all_samples.append(
                        {
                            "sample_id": sample_data[0],
                            "response": "yes",
                            "population_list": sample_data[2]
                        }
                    )
                    b_cell_list_yes.append(sample_data[2][0]["percentage"])
                    cd8_t_cell_list_yes.append(sample_data[2][1]["percentage"])
                    cd4_t_cell_list_yes.append(sample_data[2][2]["percentage"])
                    nk_cell_list_yes.append(sample_data[2][3]["percentage"])
                    monocyte_list_yes.append(sample_data[2][4]["percentage"])
                i = i + 1
        with open("pbmc_data.json", "w") as file:
            json.dump(all_samples, file, indent=4)

        
        boxplot_data = {
            "b_cell": {
                "no": b_cell_list_no,
                "yes": b_cell_list_yes
            },
            "cd8_t_cell": {
                "no": cd8_t_cell_list_no,
                "yes": cd8_t_cell_list_yes
            },
            "cd4_t_cell": {
                "no": cd4_t_cell_list_no,
                "yes": cd4_t_cell_list_yes
            },
            "nk_cell": {
                "no": nk_cell_list_no,
                "yes": nk_cell_list_yes
            },
            "monocyte": {
                "no": monocyte_list_no,
                "yes": monocyte_list_yes
            }
        }

        with open("boxplot_data.json", "w") as file:
            json.dump(boxplot_data, file, indent=4)   

        u_statistic_b_cell, p_value_b_cell = stats.mannwhitneyu(b_cell_list_no, b_cell_list_yes)
        u_statistic_cd8_t_cell, p_value_cd8_t_cell = stats.mannwhitneyu(cd8_t_cell_list_no, cd8_t_cell_list_yes)
        u_statistic_cd4_t_cell, p_value_cd4_t_cell = stats.mannwhitneyu(cd4_t_cell_list_no, cd4_t_cell_list_yes)
        u_statistic_nk_cell, p_value_nk_cell = stats.mannwhitneyu(nk_cell_list_no, nk_cell_list_yes)
        u_statistic_monocyte, p_value_monocyte = stats.mannwhitneyu(monocyte_list_no, monocyte_list_yes)
        significant_difference = "Reject the null hypothesis: The two distributions are significantly difference with a p value of: "
        no_significant_difference = "Fail to reject the null hypothesis: The two distributions are not significantly difference with a p value of: "
        p_value_b_cell = round(p_value_b_cell, 4)
        p_value_cd8_t_cell = round(p_value_cd8_t_cell, 4)
        p_value_cd4_t_cell = round(p_value_cd4_t_cell, 4)
        p_value_nk_cell = round(p_value_nk_cell, 4)
        p_value_monocyte = round(p_value_monocyte, 4)

        stats_data = {
            "b_cell": {
                "u": u_statistic_b_cell,
                "p": p_value_b_cell,
                "msg": significant_difference if p_value_b_cell < 0.05 else no_significant_difference
            },
            "cd8_t_cell": {
                "u": u_statistic_cd8_t_cell,
                "p": p_value_cd8_t_cell,
                "msg": significant_difference if p_value_cd8_t_cell < 0.05 else no_significant_difference        
            },
            "cd4_t_cell": {
                "u": u_statistic_cd4_t_cell,
                "p": p_value_cd4_t_cell,
                "msg": significant_difference if p_value_cd4_t_cell < 0.05 else no_significant_difference
            },
            "nk_cell": {
                "u": u_statistic_nk_cell,
                "p": p_value_nk_cell,
                "msg": significant_difference if p_value_nk_cell < 0.05 else no_significant_difference
            },
            "monocyte": {
                "u": u_statistic_monocyte,
                "p": p_value_monocyte,
                "msg": significant_difference if p_value_monocyte < 0.05 else no_significant_difference
            }
        }

        with open("stats.json", "w") as file:
            json.dump(stats_data, file, indent=4) 
        

if __name__ == "__main__":
    main()