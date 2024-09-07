


from infrastructure.database.entities.image_tests import ImageTests
from infrastructure.database.repositories.repository import SqlRepository


class ImageTestsRepository(SqlRepository):
    model = ImageTests


