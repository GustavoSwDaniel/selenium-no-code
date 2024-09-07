

from datetime import datetime
from typing import Dict
from core.repository.image_tests_repository import ImageTestsRepository
from core.repository.tests_repository import TestsRepository
from domain.use_case.iexecute_test_use_case import IExecuteTesteUseCase
from infrastructure.s3.s3_client import S3Client
from infrastructure.webdrive.webdrive_selenium import WebDriveSelenium
from paginate import paginate


class GetTestsUseCase(IExecuteTesteUseCase):
    def __init__(self, tests_repository: TestsRepository):
        self.tests_repository = tests_repository
    
    async def execute(self, params: Dict) -> Dict:
        results, total = await self.tests_repository.get_all_test_paginated(params)
        return paginate(results, params.get('offset'), total)
        