from typing import Optional, List

from daos.address_dao import AddressDAO
from daos.dao import Dao
from models.address import Address
from models.course import Course
from models.student import Student


class StudentDAO(Dao[Student]):
    def create(self, student: Student) -> int:
        """Crée l'entité en BD correspondant à l'objet student

        :param student: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql1 = ("INSERT INTO person (first_name, last_name, age) "
                    "VALUES "
                    "(%s, %s, %s);")
            cursor.execute(sql1, (student.first_name, student.last_name, student.age,))

            student_person_id_db = cursor.lastrowid

            sql2 = ("INSERT INTO student (id_person) "
                    "VALUES "
                    "(%s);")
            cursor.execute(sql2, (student_person_id_db,))
            # set id
            student.student_nbr = cursor.lastrowid
        Dao.connection.commit()

        return student.student_nbr


    def read(self, id_entity: int) -> Optional[Student]:
        """Renvoit l'objet correspondant à l'entité dont l'id est id_entity
           (ou None s'il n'a pu être trouvé)"""
        student: Optional[Student] = None
        # open connection
        with Dao.connection.cursor() as cursor:
            # create command, execute and get
            sql = ("SELECT student_nbr, a.id_address, first_name, last_name,age,street,city,postal_code FROM student s "
                   " INNER JOIN person p ON s.id_person = p.id_person"
                   " INNER JOIN address a ON p.id_address = a.id_address"
                   " WHERE student_nbr = %s;")
            cursor.execute(sql,(id_entity,))
            sql_student = cursor.fetchone()

            # transform into oop
        if sql_student:
            #create student oop
            student = Student(sql_student['first_name'], sql_student['last_name'], sql_student['age'])
            #set id
            student.students_nbr = sql_student['student_nbr']
            # add address
            student.address = Address(sql_student['street'], sql_student['city'], sql_student['postal_code'])
            student.address.id = sql_student['id_address']

        return student


    def read_all(self):
        """
        Obtient toute la liste des etudiants
        """
        # create list
        oop_object_list = list()
        #open connection
        with Dao.connection.cursor() as cursor:
            #create command, execute and get
            sql = ("SELECT student_nbr, a.id_address, first_name, last_name,age,street,city,postal_code FROM student s "
                   " INNER JOIN person p ON s.id_person = p.id_person"
                   " INNER JOIN address a ON p.id_address = a.id_address;")
            cursor.execute(sql)
            sql_student_list = cursor.fetchall()

            #transform into oop
            if sql_student_list:
                #for eqch
                for sql_student in sql_student_list:
                    #create the oop
                    oop_student = Student(sql_student['first_name'], sql_student['last_name'], sql_student['age'])
                    #set ids
                    oop_student.students_nbr = sql_student['student_nbr']
                    #add address
                    oop_student.address = Address(sql_student['street'], sql_student['city'], sql_student['postal_code'],)
                    oop_student.address.id = sql_student['id_address']
                    #add to list
                    oop_object_list.append(oop_student)
        return oop_object_list

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'entité correspondant à student, pour y correspondre

        :param student: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        # connect and request
        with Dao.connection.cursor() as cursor:
            # update person
            sql = ("UPDATE person p "
                   "INNER JOIN student s ON p.id_person = t.id_person "
                   "SET first_name = %s, last_name = %s, age = %s "
                   "WHERE s.student_nbr = %s;")
            cursor.execute(sql, (student.first_name, student.last_name, student.age, student.id,))

        Dao.connection.commit()
        return cursor.rowcount > 0

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'entité correspondant à student

        :param student: objet dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            # get person id
            cursor.execute("SELECT id_person FROM student WHERE student_nbr = %s", (student.student_nbr,))
            id_person = cursor.fetchone()['id_person']

            # delete teacher
            cursor.execute("DELETE FROM teacher WHERE student_nbr = %s", (student.student_nbr,))

            # delete person
            cursor.execute("DELETE FROM person WHERE id_person = %s", (id_person,))

        # end
        Dao.connection.commit()
        return cursor.rowcount > 0


    def get_courses(self, student: Student):
        """Renvoit le cours correspondant à l'etudiant envoyé par parametre"""
        courses_result: List

        with Dao.connection.cursor() as cursor:
            sql =   ("SELECT c.id_course FROM course c "
                    "INNER JOIN takes t ON c.id_course = t.id_course "
                    "WHERE t.student_nbr = %s")
            cursor.execute(sql, (student.student_nbr,))
            courses_result = cursor.fetchall()
        return courses_result


    def set_address(self,student:Student, address:Address):
        #get dao
        address_dao = AddressDAO()
        #if address exists
        if address.id is None:
            # create
            address_dao.create(address)
        else:
            #update
            updated = address_dao.update(address)
            if not updated:
                address_dao.create(address)

        #set to student locally
        student.address = address

        #update student
        self.update(student)

