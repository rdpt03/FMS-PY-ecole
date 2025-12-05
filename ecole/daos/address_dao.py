from typing import Optional

from daos.dao import Dao
from models.address import Address


class AddressDAO(Dao[Address]):
    def create(self, address: Address) -> int:
        """Crée l'entité en BD correspondant à l'objet address

        :param address: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        with Dao.connection.cursor() as cursor:
            sql = ("INSERT INTO address (street, city, postal_code) "
                   "VALUES "
                   "(%s, %s, %s);")
            cursor.execute(sql, (address.street, address.city, address.postal_code,))
            address.id = cursor.lastrowid
        Dao.connection.commit()
        return address.id


    def read(self, id_entity: int) -> Optional[Address]:
        """Renvoit l'objet correspondant à l'entité dont l'id est id_entity
           (ou None s'il n'a pu être trouvé)"""
        address: Optional[Address]

        with Dao.connection.cursor() as cursor:
            sql = "SELECT * FROM address WHERE id_address=%s"
            cursor.execute(sql, (id_entity,))
            record = cursor.fetchone()
        if record is not None:
            address = Address(record['street'], record['city'], record['postal_code'])
            address.id = record['id_address']
        else:
            address = None

        return address


    def update(self, address: Address) -> bool:
        """Met à jour en BD l'entité correspondant à address, pour y correspondre

        :param address: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        # connect and request
        with Dao.connection.cursor() as cursor:
            sql = "UPDATE address SET street = %s, city = %s, postal_code = %s WHERE id_address = %s;"
            cursor.execute(sql, (address.street, address.city, address.postal_code, address.id,))

        Dao.connection.commit()
        return cursor.rowcount > 0


    def delete(self, address: Address) -> bool:
        """Supprime en BD l'entité correspondant à obj

        :param address: objet dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        # connect and request
        with Dao.connection.cursor() as cursor:
            sql = "DELETE FROM address WHERE id_address = %s;"
            cursor.execute(sql, (address.id,))

        Dao.connection.commit()
        return cursor.rowcount > 0