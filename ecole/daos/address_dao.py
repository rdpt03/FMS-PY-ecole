from typing import Optional

from daos.dao import Dao
from models.address import Address


class AddressDAO(Dao[Address]):
    def create(self, obj: Address) -> int:
        """Crée l'entité en BD correspondant à l'objet obj

        :param obj: à créer sous forme d'entité en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        ...


    def read(self, id_entity: int) -> Optional[Address]:
        """Renvoit l'objet correspondant à l'entité dont l'id est id_entity
           (ou None s'il n'a pu être trouvé)"""
        ...


    def update(self, obj: Address) -> bool:
        """Met à jour en BD l'entité correspondant à obj, pour y correspondre

        :param obj: objet déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        ...


    def delete(self, obj: Address) -> bool:
        """Supprime en BD l'entité correspondant à obj

        :param obj: objet dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        ...