class GetOwnerMixin:

    @property
    def get_owner(self):
        return self.queryset.get(id=self.kwargs.get('pk')).owner