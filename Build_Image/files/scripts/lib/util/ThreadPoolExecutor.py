from concurrent.futures import ThreadPoolExecutor as ConcurrentThreadPoolExecutor


class ThreadPoolExecutor:
    __instance = None  # type: ThreadPoolExecutor

    __executor = None  # type: ThreadPoolExecutor

    def __init__(self) -> None:
        if ThreadPoolExecutor.__instance is not None:
            raise Exception("ThreadPool is a Singleton, use get_instance method to get an instance!")

        ThreadPoolExecutor.__executor = ConcurrentThreadPoolExecutor()

        ThreadPoolExecutor.__instance = self

    @staticmethod
    def get_instance() -> ConcurrentThreadPoolExecutor:
        """
        Returns an instance of this class (Singleton)
        """
        if ThreadPoolExecutor.__instance is None:
            ThreadPoolExecutor()
        return ThreadPoolExecutor.__executor

    def __del__(self):
        ThreadPoolExecutor.__executor.shutdown()
