

def indexer(context):
    field = context.getField('categories')
    if not field:
        return

    values = field.get(context)
    return values
