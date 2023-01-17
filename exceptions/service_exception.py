class ServiceException(Exception):
    def __init__(self, *args, **kwargs):
        self.__response_code = kwargs.get('code')
        super(ServiceException, self).__init__(*args)

    def get_code(self):
        return self.__response_code
