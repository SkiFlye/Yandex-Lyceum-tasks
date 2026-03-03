import datetime
import os
from data import db_session
from data.users import User
from data.jobs import Jobs


def main():
    db_dir = "db"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    db_session.global_init(f"{db_dir}/mars_explorer.db")
    db_sess = db_session.create_session()
    job = Jobs()
    job.team_leader = 1
    job.job = "deployment of residential modules 1 and 2"
    job.work_size = 15
    job.collaborators = "2, 3"
    job.start_date = datetime.datetime.now()
    job.is_finished = False
    db_sess.add(job)
    db_sess.commit()
    jobs = db_sess.query(Jobs).all()
    for job in jobs:
        print(job.team_leader, job.job, job.work_size,
              job.collaborators, job.is_finished)
    db_sess.close()


if __name__ == '__main__':
    main()