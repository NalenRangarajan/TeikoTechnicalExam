# TeikoTechnicalExam

Instructions:
1. ensure all necessary dependencies rescribed in requirements.txt are installed make setup
2. run make pipeline to build the py files
    python load_data.py and then python main.py
    (can take a bit to finish)
3. run make dashboard to get a localhost dashboard describing the relevant data
    alternatively do python -m http.server 8000 and navigate to "dashboard.html"

Explanation:

For the relational database I decided on a flow design where all data flowed down from the highest level of project. Since all data belongs to a project that made sense to start like that. From there projects have many subjects which have many samples which have many populations. All data is stored at their respective level such that data such as age and sex are stored in the subject table and data such as cell_count is stored in the population table.

Overview:

I opted to go with a load_data.py file to load all the database data into to the schema and a main.py to process this data for the requested output. To be transparent I was out of town without access to a computer for the first 2.5 days of the allotted 3 day window to complete this (git repository creation and commit timestamps can be viewed as evidence of this). As such some shortcuts were taken on efficiency and code reuseability/scalability to be able to get every section of the assignment completed. This means that unfortunately the work is not up to my typical level of quality. With that though many design choices were made for quick rollout, that meant choices like having processing that could normally be optimized repeated and all the processing done in a centralized location in main.py.

Dashboard link: http://localhost:8000/dashboard.html