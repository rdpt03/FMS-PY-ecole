from typing import Optional, List

from daos.dao import Dao
from models.address import Address
from models.course import Course
from models.teacher import Teacher


class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        """Crée l'entité en BD correspondant à l'objet teacher

        :param teacher: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql1 = ("INSERT INTO person (first_name, last_name, age) "
                   "VALUES "
                   "(%s, %s, %s);")
            cursor.execute(sql1, (teacher.first_name, teacher.last_name, teacher.age,))

            teacher_person_id_db = cursor.lastrowid

            sql2 = ("INSERT INTO teacher (hiring_date, id_person) "
                   "VALUES "
                   "(%s, %s);")
            cursor.execute(sql2, (teacher.hiring_date, teacher_person_id_db,))
            #set id
            teacher.id = cursor.lastrowid
        Dao.connection.commit()

        return teacher.id

    def read(self, id_entity: int) -> Optional[Teacher]:
        """Renvoit l'objet correspondant à l'entité dont l'id est id_entity
           (ou None s'il n'a pu être trouvé)"""
        teacher: Optional[Teacher] = None

        with Dao.connection.cursor() as cursor:
            sql = "SELECT id_teacher, hiring_date, first_name, last_name, age FROM teacher t INNER JOIN person p ON t.id_person = p.id_person WHERE id_teacher = %s;"
            cursor.execute(sql, (id_entity,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(record['first_name'], record['last_name'], record['age'], record['hiring_date'])
            teacher.id = record['id_teacher']
            teacher.courses_teached = self.get_courses(teacher)

        return teacher


    def read_all(self):
        """
        Obtient toute la liste de professeurs
        """
        # create list
        oop_object_list = list()
        #open connection
        with Dao.connection.cursor() as cursor:
            #create command, execute and get
            sql = ("SELECT id_teacher, first_name, last_name, age, hiring_date FROM teacher t INNER JOIN person p ON t.id_person = p.id_person;")
            cursor.execute(sql)
            sql_teacher_list = cursor.fetchall()

            #transform into oop
            if sql_teacher_list:
                #for each
                for teacher in sql_teacher_list:
                    #create the oop
                    oop_teacher = Teacher(teacher['first_name'], teacher['last_name'], teacher['age'], teacher['hiring_date'])
                    oop_teacher.id = teacher['id_teacher']
                    #add to list
                    oop_object_list.append(oop_teacher)
        return oop_object_list


    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité correspondant à teacher, pour y correspondre

        :param teacher: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        # connect and request
        with Dao.connection.cursor() as cursor:
            # update person
            sql = ("UPDATE person p "
                   "INNER JOIN teacher t ON p.id_person = t.id_person "
                   "SET first_name = %s, last_name = %s, age = %s "
                   "WHERE t.id_teacher = %s;")
            cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, teacher.id,))

            # update teacher
            sql = ("UPDATE teacher t "
                   "SET hiring_date = %s "
                   "WHERE t.id_teacher = %s;")
            cursor.execute(sql, (teacher.hiring_date, teacher.id,))

        Dao.connection.commit()
        return cursor.rowcount > 0


    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité correspondant à teacher

        :param teacher: objet dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            #get person id
            cursor.execute("SELECT id_person FROM teacher WHERE id_teacher = %s", (teacher.id,))
            id_person = cursor.fetchone()['id_person']

            #delete teacher
            cursor.execute("DELETE FROM teacher WHERE id_teacher = %s", (teacher.id,))

            #delete person
            cursor.execute("DELETE FROM person WHERE id_person = %s", (id_person,))

        #end
        Dao.connection.commit()
        return cursor.rowcount > 0

    def get_courses(self, teacher: Teacher):
        """Renvoit le cours correspondant au professeur envoyé par parametre"""
        courses_result_oop: List = list()

        with Dao.connection.cursor() as cursor:
            sql =   "SELECT id_course,name,start_date,end_date FROM course c WHERE c.id_teacher = %s"
            cursor.execute(sql, (teacher.id,))
            courses_result_sql = cursor.fetchall()

            #for each founded course
            for course_line in courses_result_sql:
                #transform into oop
                course_oop = Course(course_line['name'], course_line['start_date'], course_line['end_date'])
                course_oop.id = course_line['id_course']
                #add to list
                courses_result_oop.append(course_oop)

        return courses_result_oop