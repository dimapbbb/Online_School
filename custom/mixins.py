class GetOwnerMixin:
    queryset = None
    kwargs = {}

    @property
    def get_owner(self):
        return self.queryset.get(id=self.kwargs.get('pk')).owner