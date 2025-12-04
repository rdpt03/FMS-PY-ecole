from typing import Optional

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
            sql = ("SELECT * FROM teacher t"
                    "INNER JOIN person p ON t.id_person = p.id_person;")
            cursor.execute(sql)
            sql_student_list = cursor.fetchall()

            #transform into oop
            if sql_student_list:
                #for each
                for student in sql_student_list:
                    #create the oop
                    oop_student = Teacher(student['first_name'], student['last_name'], student['age'])
                    #add address
                    oop_student.address = Address(student['street'], student['city'], student['postal_code'],)
                    #add to list
                    oop_object_list.append(oop_student)
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