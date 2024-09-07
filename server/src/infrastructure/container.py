from dependency_injector import containers, providers
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from config import Config
from core.repository.image_tests_repository import ImageTestsRepository
from core.repository.tests_repository import TestsRepository
from core.use_case.execute_test_use_case import ExecuteTesteUseCase
from core.use_case.get_test_use_case import GetTestUseCase
from core.use_case.get_tests_use_case import GetTestsUseCase
from infrastructure.database.database import PostgresDatabase
from infrastructure.s3.s3_client import S3Client
from infrastructure.webdrive.webdrive_selenium import WebDriveSelenium


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    postgres_db = providers.Singleton(PostgresDatabase, database_url=Config.DATABASE_URL)
    chrome_service = providers.Factory(ChromeService, executable_path=ChromeDriverManager().install())
    driver = providers.Factory(webdriver.Chrome, service=chrome_service)
    webdriver_selenium = providers.Factory(WebDriveSelenium, webdriver=driver, url_test=Config.URL_TEST)

    s3_client = providers.Factory(S3Client, s3_bucket_name=Config.S3_BUCKET_NAME,
                              aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                              aws_region_name=Config.AWS_REGION_NAME)

    tests_repository = providers.Factory(TestsRepository, session_factory=postgres_db.provided.session)
    image_tests_repository = providers.Factory(ImageTestsRepository, session_factory=postgres_db.provided.session)


    execute_test_use_case = providers.Factory(ExecuteTesteUseCase, 
                                              webdriver_selenium=webdriver_selenium,
                                              tests_repository=tests_repository,
                                              s3_client=s3_client,
                                              image_tests_repository=image_tests_repository)


    get_tests_use_case = providers.Factory(GetTestsUseCase, 
                                              tests_repository=tests_repository)
    get_test_use_case = providers.Factory(GetTestUseCase, 
                                              tests_repository=tests_repository)