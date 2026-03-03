import os
from data import db_session
from data.users import User


def main():
    db_dir = "db"
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    db_session.global_init(f"{db_dir}/mars_explorer.db")
    db_sess = db_session.create_session()

    captain = User()
    captain.surname = "Scott"
    captain.name = "Ridley"
    captain.age = 21
    captain.position = "captain"
    captain.speciality = "research engineer"
    captain.address = "module_1"
    captain.email = "scott_chief@mars.org"
    captain.set_password("cap")

    db_sess.add(captain)

    colonist1 = User()
    colonist1.surname = "Smith"
    colonist1.name = "John"
    colonist1.age = 30
    colonist1.position = "engineer"
    colonist1.speciality = "mechanical engineer"
    colonist1.address = "module_2"
    colonist1.email = "smith@mars.org"
    colonist1.set_password("123")
    colonist2 = User()
    colonist2.surname = "Johnson"
    colonist2.name = "Alice"
    colonist2.age = 28
    colonist2.position = "doctor"
    colonist2.speciality = "surgeon"
    colonist2.address = "module_3"
    colonist2.email = "johnson@mars.org"
    colonist2.set_password("456")
    colonist3 = User()
    colonist3.surname = "Williams"
    colonist3.name = "Bob"
    colonist3.age = 35
    colonist3.position = "scientist"
    colonist3.speciality = "astrobiologist"
    colonist3.address = "module_2"
    colonist3.email = "williams@mars.org"
    colonist3.set_password("789")
    db_sess.add(colonist1)
    db_sess.add(colonist2)
    db_sess.add(colonist3)
    db_sess.commit()
    users = db_sess.query(User).all()
    for user in users:
        print(user.surname, user.name, user.age, user.position,
              user.speciality, user.address, user.email)
    db_sess.close()


if __name__ == '__main__':
    main()