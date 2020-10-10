class BaseFactory:
    @classmethod
    async def create(cls, **kwargs):
        data = {}

        for k, v in cls.__dict__.items():
            if k in ("__doc__", "__module__", "Meta"):
                continue

            if k in kwargs:
                data[k] = kwargs.get(k)
            else:
                if isinstance(v, type):
                    obj = await v.create()
                    data[f"{k}_id"] = obj.id
                else:
                    data[k] = v

        model = cls.Meta.model
        return await model.create(**data)
