# This file contains views for the application according to Pyramid framework
from pyramid.view import view_config 
from pyramid.response import Response, FileResponse
from utils import *
import json
import tempfile

# home view
@view_config(route_name='home',renderer='templates/index.html')
def home_view(request):
    context = {'title':'Home'}
    return context

# to render the json result as output
@view_config(route_name="benford",renderer="json")
def benford(request):
    # get the input from form
    csv_file = request.POST['csvInput'].file
    filename = request.POST['csvInput'].filename 
    # check if input files is CSV or not
    name, ext = filename.split('.')
    if not ext == 'csv':
        return {"Error": "Invalid File Input! Please upload CSV file"}
    else:
        # if it is CSV
        # save in local directory uploads
        filepath = f"uploads/{filename}"
        with open(filepath,"wb") as f:
            f.write(csv_file.read())
        # get data distribution for the input file
        data_distribution = get_data_distribution(filepath) 
        # check if the distribution follows benford's law or not   
        if check_benford_law(filepath) == True:
            message = "Given data follows Benford's law"
        else:
            message = "Given data doesn't follow Benford's law"
        # create a json file with the result
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

# analyse view
@view_config(route_name="analyse",renderer="templates/result.html")
def analyse(request):
    # input from form
    csv_file = request.POST['csvInput'].file
    filename = request.POST['csvInput'].filename 
    # check for valid input
    name, ext = filename.split('.')
    if not ext == 'csv':
        return {"Error": "Invalid File Input! Please upload CSV file"}
    else:
        # save in local directory uploads
        filepath = f"uploads/{filename}"
        with open(filepath,"wb") as f:
            f.write(csv_file.read())
        
        # get observed data distribution
        data_distribution = get_data_distribution(filepath) 
        # get benford data distribution
        benford_distribution = {str(k): np.log10(1+(1/k)) for k in range(1,10)}   
        # get differences 
        differences = {}
        for k in benford_distribution.keys():
            differences[k] = abs(benford_distribution[k] - data_distribution[k])
        # check if the distribution follows benford's law or not
        if check_benford_law(filepath) == True:
            message = "Given data follows Benford's law"
        else:
            message = "Given data doesn't follow Benford's law"
        # create result
        result =  {
            "Message": message,
            "Distribution": data_distribution,
            "Benford": benford_distribution,
            "Differences": differences,
            "title": "Results"
            }
    # return result to html template
    return result