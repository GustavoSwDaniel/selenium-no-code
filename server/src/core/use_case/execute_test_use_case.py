

from datetime import datetime
from typing import Dict
from core.repository.image_tests_repository import ImageTestsRepository
from core.repository.tests_repository import TestsRepository
from domain.use_case.iexecute_test_use_case import IExecuteTesteUseCase
from infrastructure.s3.s3_client import S3Client
from infrastructure.webdrive.webdrive_selenium import WebDriveSelenium


class ExecuteTesteUseCase(IExecuteTesteUseCase):
    def __init__(self, webdriver_selenium: WebDriveSelenium, tests_repository: TestsRepository, 
                 image_tests_repository: ImageTestsRepository, s3_client: S3Client):
        self.webdriver_selenium = webdriver_selenium
        self.tests_repository = tests_repository
        self.s3_client = s3_client
        self.image_tests_repository = image_tests_repository
    
    async def _save_screenshot_in_s3(self):
        urls = []
        for step in self.webdriver_selenium.screenshots:
            url = self.s3_client.upload_screenshot(step['image'], step['step_name'])
            urls.append(url)
        return urls

    async def execute(self, test: dict) -> Dict:
        try:
            for case in test['cases']:
                note = self.webdriver_selenium.execute(test['url'], case['steps'])
                test_saved = await self.tests_repository.create({'case_name': case['name'], 'url': test['url'], 'status': 'success', 'note': note})
                screenshot_list_url = await self._save_screenshot_in_s3()
                for screenshot__url in screenshot_list_url:
                    await self.image_tests_repository.create({'test_id': test_saved.id, 'url': screenshot__url})
            return test['url']
        except Exception as error:
            await self.tests_repository.create({'case_name': case['name'],'url': test['url'], 'status': 'failure', 'message': str(error)})
            raise error
