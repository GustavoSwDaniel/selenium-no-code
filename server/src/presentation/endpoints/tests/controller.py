from fastapi import APIRouter, Depends, FastAPI, Request
from dependency_injector.wiring import inject, Provide


from core.use_case.execute_test_use_case import ExecuteTesteUseCase
from core.use_case.get_test_use_case import GetTestUseCase
from core.use_case.get_tests_use_case import GetTestsUseCase
from infrastructure.container import Container
from presentation.schemas.tests import PaginateTestReponseSchema, Test, TestReponseSchema


router = APIRouter(tags=['Logs'])


@router.post("/tests")
@inject
async def execute_test(request: Request, tests: Test, execute_test_use_case: ExecuteTesteUseCase = Depends(Provide[Container.execute_test_use_case])):
    url = await execute_test_use_case.execute(tests.model_dump())
    return {"url": url}


@router.get("/tests", response_model=PaginateTestReponseSchema)
@inject
async def get_test(request: Request, limit: int = 12, offset: int = 0,
                   get_tests_use_case: GetTestsUseCase = Depends(Provide[Container.get_tests_use_case])):
    tests = await get_tests_use_case.execute({'limit': limit, 'offset': offset})
    return tests


@router.get("/tests/{id}", response_model=TestReponseSchema)
@inject
async def get_test(request: Request, id: int,
                   get_test_use_case: GetTestUseCase = Depends(Provide[Container.get_test_use_case])):
    tests = await get_test_use_case.execute(id)
    return tests

def configure(app: FastAPI):
    app.include_router(router)