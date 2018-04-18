def marshal(model):
    if isinstance(model, list):
        if not model:
            return []
        return next(iter(model)).schema.dump(model, many=True).data
    return model.schema.dump(model).data
