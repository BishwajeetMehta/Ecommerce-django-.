from .models import System_setting,Categories

def system_data_processor(request):
    system_data =System_setting.objects.first()
    
    categories =Categories.objects.filter(status=True)
    # request.session.get('categories',[])
    return {'system_data': system_data,'categories':categories} # ta access session data globally