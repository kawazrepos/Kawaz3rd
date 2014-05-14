def get_full_permission_name(perm_codename, model_obj):
    '''
    Returns full permission name by `perm_codename` and `model_obj`
    e.g. perm_codename = 'view', model_obj = Event -> 'events.view_event'
    '''
    app_label = model_obj._meta.app_label
    model_name = model_obj._meta.object_name.lower()
    full_perm_name = '{}.{}_{}'.format(app_label, perm_codename, model_name)
    return full_perm_name