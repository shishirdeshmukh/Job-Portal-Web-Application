from sqlalchemy import create_engine, text

db_connection_string = 'mysql+pymysql://1aabylr2peqpidlkvkiu:pscale_pw_Dt8AeuyulrgqsmdiOaXh7UhS5AvMMSi6HLz5V0FUMJt@aws.connect.psdb.cloud/qwerty?charset=utf8mb4'

engine = create_engine(
    db_connection_string,
    connect_args={"ssl": {"ssl_ca": "/etc/ssl/certs/ca-certificates.crt"}}
)


def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = []
        for row in result.all():
            jobs.append(dict(row._asdict()))  # Convert row to dictionary
        return jobs


def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs WHERE id = :val"), val=id)
        rows = result.all()
        if len(rows) == 0:
            return None
        else:
            return dict(rows[0]._asdict())  # Convert row to dictionary


def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text(
            "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"
        )

        conn.execute(
            query,
            job_id=job_id,
            full_name=data['full_name'],
            email=data['email'],
            linkedin_url=data['linkedin_url'],
            education=data['education'],
            work_experience=data['work_experience'],
            resume_url=data['resume_url']
        )
