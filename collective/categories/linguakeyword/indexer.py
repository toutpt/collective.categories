

def indexer(context):
    field = context.getField('categories')
    if not field:
        return

    values = field.get(context)
    lingua_values = context.getLinguaKeywordsFromValue(values)
    return lingua_values
