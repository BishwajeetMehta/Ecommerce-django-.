def system_data_processor(request):
    system_data = request.session.get('system_data', [])
    categories =request.session.get('categories',[])
    return {'system_data': system_data,'categories':categories} # ta access session data globally