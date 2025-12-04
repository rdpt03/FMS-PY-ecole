from typing import Optional, List

from daos.dao import Dao
from models.address import Address
from models.teacher import Teacher


class TeacherDao(Dao[Teacher]):
    def create(self, obj: Teacher) -> int:
        """Crée l'entité en BD correspondant à l'objet obj

        :param obj: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...


    def read(self, id_entity: int) -> Optional[Teacher]:
        """Renvoit l'objet correspondant à l'entité dont l'id est id_entity
           (ou None s'il n'a pu être trouvé)"""
        ...


    def read_all(self):
        """
        Obtient toute la liste des etudiants
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

    def update(self, obj: Teacher) -> bool:
        """Met à jour en BD l'entité correspondant à obj, pour y correspondre

        :param obj: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...


    def delete(self, obj: Teacher) -> bool:
        """Supprime en BD l'entité correspondant à obj

        :param obj: objet dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...

    def get_courses(self, teacher: Teacher):
        """Renvoit le cours correspondant au professeur envoyé par parametre"""
        courses_result: List

        with Dao.connection.cursor() as cursor:
            sql =   "SELECT id_course FROM course c WHERE c.id_teacher = %s"
            cursor.execute(sql, (teacher.id,))
            courses_result = cursor.fetchall()
        return courses_result