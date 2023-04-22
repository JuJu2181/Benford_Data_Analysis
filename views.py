from pyramid.view import view_config 
from pyramid.response import Response, FileResponse
from utils import *
import json
import tempfile

@view_config(route_name='home',renderer='templates/index.html')
def home_view(request):
    context = {'title':'Home'}
    return context

@view_config(route_name="benford",renderer="json")
def benford(request):
    csv_file = request.POST['csvInput'].file
    filename = request.POST['csvInput'].filename 
    name, ext = filename.split('.')
    if not ext == 'csv':
        return {"Error": "Invalid File Input! Please upload CSV file"}
    else:
        # save in local directory uploads
        filepath = f"uploads/{filename}"
        with open(filepath,"wb") as f:
            f.write(csv_file.read())
        
        data_distribution = get_data_distribution(filepath)    
        if check_benford_law(filepath) == True:
            message = "Given data follows Benford's law"
        else:
            message = "Given data doesn't follow Benford's law"
            
        result =  {
            "Message": message,
            "Distribution": data_distribution
            }
        
        json_data = json.dumps(result)
        
        # save json file locally
        with open(f"output/{name}.json","w") as f:
            f.write(json_data)
        
    # For downloading the file
    # Maybe we can add another endpoint for download option anyways for later
    # Create a temporary file to store the JSON data
    # with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    #     f.write(json_data)
    #     temp_filename = f.name
    # response = FileResponse(temp_filename, request=request, content_type='application/json')
    # response.headers['Content-Disposition'] = 'attachment; filename="benford.json"'
    # return response
    return result
    