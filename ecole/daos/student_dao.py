from typing import Optional

from daos.dao import Dao
from models.address import Address
from models.student import Student


class StudentDAO(Dao[Student]):
    def create(self, obj: Student) -> int:
        """Crée l'entité en BD correspondant à l'objet obj

        :param obj: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...


    def read(self, id_entity: int) -> Optional[Student]:
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
            sql = ("SELECT first_name, last_name,age,street,city,postal_code FROM student s "
                   " INNER JOIN person p ON s.id_person = p.id_person"
                   " INNER JOIN address a ON p.id_address = a.id_address;")
            cursor.execute(sql)
            sql_student_list = cursor.fetchall()

            #transform into oop
            if sql_student_list:
                #for eqch
                for student in sql_student_list:
                    #create the oop
                    oop_student = Student(student['first_name'], student['last_name'], student['age'])
                    #add address
                    oop_student.address = Address(student['street'], student['city'], student['postal_code'],)
                    #add to list
                    oop_object_list.append(oop_student)
        return oop_object_list

    def update(self, obj: Student) -> bool:
        """Met à jour en BD l'entité correspondant à obj, pour y correspondre

        :param obj: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...


    def delete(self, obj: Student) -> bool:
        """Supprime en BD l'entité correspondant à obj

        :param obj: objet dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...