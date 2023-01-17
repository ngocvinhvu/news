from abc import ABC, abstractmethod
from typing import Any, List, Union, Callable


class Generated(ABC):
    @abstractmethod
    def generate(self) -> Any:
        pass


class AsyncGenerated(ABC):
    @abstractmethod
    async def generate(self) -> Any:
        pass


class ResultSettable(ABC):
    @abstractmethod
    def set_result(self, result: Any):
        pass


class SettableGenerated(Generated, ResultSettable, ABC):
    pass


class AsyncSettableGenerated(AsyncGenerated, ResultSettable, ABC):
    pass


class GeneratedException(Exception):
    pass


class GeneratedContinuesException(GeneratedException):
    pass


class GeneratedTerminatedException(GeneratedException):
    pass


class BaseResultSettable(SettableGenerated):
    def __init__(self, result: Any = None):
        self.__result = result

    def set_result(self, result: Any):
        self.__result = result

    def generate(self) -> Any:
        return self.__result


class ResultSettableService(BaseResultSettable):
    def generate(self) -> Any:
        result = super(ResultSettableService, self).generate()
        if not result:
            raise GeneratedException()

        return result


class ResultGenerated(ABC):
    @abstractmethod
    def generated_result(self, result: Any) -> Any:
        pass


class HandledGenerated(SettableGenerated):
    def __init__(self, generated: ResultGenerated,
                 result: Any = None):
        self.__generated = generated
        self.__settable = BaseResultSettable(result)

    def set_result(self, result: Any):
        self.__settable.set_result(result)

    def generate(self) -> Any:
        return self.__generated.generated_result(self.__settable.generate())


class AsyncResultGenerated(ABC):
    @abstractmethod
    async def generated_result(self, result: Any = None) -> Any:
        pass


class AsyncHandledGenerated(AsyncSettableGenerated):
    def __init__(self, generated: AsyncResultGenerated,
                 result: Any = None):
        self.__generated = generated
        self.__settable = ResultSettableService(result)

    def set_result(self, result: Any):
        self.__settable.set_result(result)

    async def generate(self) -> Any:
        return await self.__generated.generated_result(self.__settable.generate())


class ExecutableGenerated(ABC):
    @abstractmethod
    async def execute_generated(self):
        pass


class GeneratedExecutor(AsyncSettableGenerated):
    def __init__(self, settable_generated_services: List[Union[SettableGenerated, AsyncGenerated]],
                 result=None):
        self.__settable_generated_services = settable_generated_services
        self.__settable = BaseResultSettable(result)

    def set_result(self, result: Any):
        self.__settable.set_result(result)

    async def generate(self) -> Any:
        result = self.__settable.generate()
        for generated in self.__settable_generated_services:
            try:
                generated.set_result(result)
                if isinstance(generated, AsyncGenerated):
                    result = await generated.generate()
                    continue

                result = generated.generate()
            except GeneratedContinuesException:
                continue

            except GeneratedTerminatedException:
                break

        return result


class ExecutableGeneratedService(AsyncGenerated):

    def __init__(self, generated: Union[AsyncGenerated, Generated], executable_generated: ExecutableGenerated,
                 generated_services: List[Union[SettableGenerated, AsyncGenerated]] = None,
                 executable_services: List[Union[SettableGenerated, AsyncGenerated]] = None):

        self.__generated = generated
        self.__executable_generated = executable_generated

        self.__generated_services = generated_services or []
        self.__executable_services = executable_services or []

    async def generate(self) -> Any:
        try:
            if isinstance(self.__generated, AsyncGenerated):
                result = await self.__generated.generate()
            else:
                result = self.__generated.generate()

            result = await GeneratedExecutor(self.__generated_services, result=result).generate()

        except GeneratedException as e:
            result = await self.__executable_generated.execute_generated()
            result = await GeneratedExecutor(self.__executable_services, result=result).generate()

        return result
